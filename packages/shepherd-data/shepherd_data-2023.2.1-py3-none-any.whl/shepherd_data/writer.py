"""
Writer that inherits from Reader-Baseclass
"""
import logging
import math
from itertools import product
from pathlib import Path
from typing import NoReturn
from typing import Optional
from typing import Union

import h5py
import numpy as np
import yaml

from .calibration import cal_default
from .calibration import si_to_raw
from .reader import Reader


def unique_path(base_path: Union[str, Path], suffix: str) -> Path:
    """finds an unused filename in case it already exists

    :param base_path: file-path to test
    :param suffix: file-suffix
    :return: new non-existing path
    """
    counter = 0
    while True:
        path = base_path.with_suffix(f".{counter}{suffix}")
        if not path.exists():
            return path
        counter += 1


class Writer(Reader):
    """Stores data for Shepherd in HDF5 format

    Args:
        file_path: (Path) Name of the HDF5 file that data will be written to
        mode: (str) Indicates if this is data from harvester or emulator
        datatype: (str) choose type: ivsample (most common), ivcurve or isc_voc
        window_samples: (int) windows size for the datatype ivcurve
        cal_data: (CalibrationData) Data is written as raw ADC
            values. We need calibration data in order to convert to physical
            units later.
        modify_existing: (bool) explicitly enable modifying existing file
            otherwise a unique name will be found
        compression: (str) use either None, lzf or "1" (gzips compression level)
        verbose: (bool) provides more info instead of just warnings / errors
    """

    # choose lossless compression filter
    # - lzf:  low to moderate compression, VERY fast, no options
    #         -> 20 % cpu overhead for half the filesize
    # - gzip: good compression, moderate speed, select level from 1-9, default is 4
    #         -> lower levels seem fine
    #         -> _algo=number instead of "gzip" is read as compression level for gzip
    # -> comparison / benchmarks https://www.h5py.org/lzf/
    comp_default = 1
    mode_default: str = "harvester"
    datatype_default: str = "ivsample"

    _chunk_shape: tuple = (Reader.samples_per_buffer,)

    _logger: logging.Logger = logging.getLogger("SHPData.Writer")

    def __init__(
        self,
        file_path: Path,
        mode: str = None,
        datatype: str = None,
        window_samples: int = None,
        cal_data: dict = None,
        modify_existing: bool = False,
        compression: Union[None, str, int] = "default",
        verbose: Optional[bool] = True,
    ):
        super().__init__(file_path=None, verbose=verbose)

        file_path = Path(file_path)
        self._modify = modify_existing

        if verbose is not None:
            self._logger.setLevel(logging.INFO if verbose else logging.WARNING)

        if self._modify or not file_path.exists():
            self._file_path = file_path
            self._logger.info("Storing data to   '%s'", self._file_path)
        else:
            base_dir = file_path.resolve().parents[0]
            self._file_path = unique_path(base_dir / file_path.stem, file_path.suffix)
            self._logger.warning(
                "File %s already exists -> " "storing under %s instead",
                file_path,
                self._file_path.name,
            )

        if not isinstance(mode, (str, type(None))):
            raise TypeError(f"can not handle type '{type(mode)}' for mode")
        if isinstance(mode, str) and mode not in self.mode_dtype_dict:
            raise ValueError(f"can not handle mode '{mode}'")

        if not isinstance(datatype, (str, type(None))):
            raise TypeError(f"can not handle type '{type(datatype)}' for datatype")
        if (
            isinstance(datatype, str)
            and datatype
            not in self.mode_dtype_dict[self.mode_default if (mode is None) else mode]
        ):
            raise ValueError(f"can not handle datatype '{datatype}'")

        if self._modify:
            self._mode = mode
            self._cal = cal_data
            self._datatype = datatype
            self._window_samples = window_samples
        else:
            self._mode = self.mode_default if (mode is None) else mode
            self._cal = cal_default if (cal_data is None) else cal_data
            self._datatype = self.datatype_default if (datatype is None) else datatype
            self._window_samples = 0 if (window_samples is None) else window_samples

        if compression in [None, "lzf", 1]:  # order of recommendation
            self._compression_algo = compression
        else:
            self._compression_algo = self.comp_default

    def __enter__(self):
        """Initializes the structure of the HDF5 file

        HDF5 is hierarchically structured and before writing data, we have to
        setup this structure, i.e. creating the right groups with corresponding
        data types. We will store 3 types of data in a database: The
        actual IV samples recorded either from the harvester (during recording)
        or the target (during emulation). Any log messages, that can be used to
        store relevant events or tag some parts of the recorded data.

        """
        if self._modify:
            self.h5file = h5py.File(self._file_path, "r+")
        else:
            self.h5file = h5py.File(self._file_path, "w")

            # Store voltage and current samples in the data group,
            # both are stored as 4 Byte unsigned int
            gp_data = self.h5file.create_group("data")
            # the size of window_samples-attribute in harvest-data indicates ivcurves as input
            # -> emulator uses virtual-harvester, field will be adjusted by .embed_config()
            gp_data.attrs["window_samples"] = 0

            gp_data.create_dataset(
                "time",
                (0,),
                dtype="u8",
                maxshape=(None,),
                chunks=self._chunk_shape,
                compression=self._compression_algo,
            )
            gp_data["time"].attrs["unit"] = "ns"
            gp_data["time"].attrs["description"] = "system time [ns]"

            gp_data.create_dataset(
                "current",
                (0,),
                dtype="u4",
                maxshape=(None,),
                chunks=self._chunk_shape,
                compression=self._compression_algo,
            )
            gp_data["current"].attrs["unit"] = "A"
            gp_data["current"].attrs[
                "description"
            ] = "current [A] = value * gain + offset"

            gp_data.create_dataset(
                "voltage",
                (0,),
                dtype="u4",
                maxshape=(None,),
                chunks=self._chunk_shape,
                compression=self._compression_algo,
            )
            gp_data["voltage"].attrs["unit"] = "V"
            gp_data["voltage"].attrs[
                "description"
            ] = "voltage [V] = value * gain + offset"

        # Store the mode in order to allow user to differentiate harvesting vs emulation data
        if isinstance(self._mode, str) and self._mode in self.mode_dtype_dict:
            self.h5file.attrs["mode"] = self._mode

        if (
            isinstance(self._datatype, str)
            and self._datatype in self.mode_dtype_dict[self.get_mode()]
        ):
            self.h5file["data"].attrs["datatype"] = self._datatype
        elif not self._modify:
            self._logger.error("datatype invalid? '%s' not written", self._datatype)

        if isinstance(self._window_samples, int):
            self.h5file["data"].attrs["window_samples"] = self._window_samples

        if self._cal is not None:
            for channel, parameter in product(
                ["current", "voltage"], ["gain", "offset"]
            ):
                self.h5file["data"][channel].attrs[parameter] = self._cal[channel][
                    parameter
                ]

        super().__enter__()
        return self

    def __exit__(self, *exc):
        self._align()
        self._refresh_file_stats()
        self._logger.info(
            "closing hdf5 file, %s s iv-data, size = %s MiB, rate = %s KiB/s",
            self.runtime_s,
            round(self.file_size / 2**20, 3),
            round(self.data_rate / 2**10),
        )
        self.is_valid()
        self.h5file.close()

    def append_iv_data_raw(
        self,
        timestamp_ns: Union[np.ndarray, float, int],
        voltage: np.ndarray,
        current: np.ndarray,
    ) -> NoReturn:
        """Writes raw data to database

        Args:
            timestamp_ns: just start of buffer or whole ndarray
            voltage: ndarray as raw unsigned integers
            current: ndarray as raw unsigned integers
        """
        len_new = min(voltage.size, current.size)

        if isinstance(timestamp_ns, float):
            timestamp_ns = int(timestamp_ns)
        if isinstance(timestamp_ns, int):
            time_series_ns = self.sample_interval_ns * np.arange(len_new).astype("u8")
            timestamp_ns = timestamp_ns + time_series_ns
        if isinstance(timestamp_ns, np.ndarray):
            len_new = min(len_new, timestamp_ns.size)
        else:
            self._logger.error("timestamp-data was not usable")
            return

        len_old = self.ds_time.shape[0]

        # resize dataset
        self.ds_time.resize((len_old + len_new,))
        self.ds_voltage.resize((len_old + len_new,))
        self.ds_current.resize((len_old + len_new,))

        # append new data
        self.ds_time[len_old : len_old + len_new] = timestamp_ns[:len_new]
        self.ds_voltage[len_old : len_old + len_new] = voltage[:len_new]
        self.ds_current[len_old : len_old + len_new] = current[:len_new]

    def append_iv_data_si(
        self,
        timestamp: Union[np.ndarray, float],
        voltage: np.ndarray,
        current: np.array,
    ) -> NoReturn:
        """Writes data (in SI / physical unit) to file, but converts it to raw-data first

        Args:
            timestamp: python timestamp (time.time()) in seconds (si-unit)
                       -> provide start of buffer or whole ndarray
            voltage: ndarray in physical-unit V
            current: ndarray in physical-unit A
        """
        # SI-value [SI-Unit] = raw-value * gain + offset,
        timestamp = timestamp * 10**9
        voltage = si_to_raw(voltage, self._cal["voltage"])
        current = si_to_raw(current, self._cal["current"])
        self.append_iv_data_raw(timestamp, voltage, current)

    def _align(self) -> NoReturn:
        """Align datasets with buffer-size of shepherd"""
        self._refresh_file_stats()
        n_buff = self.ds_time.size / self.samples_per_buffer
        size_new = int(math.floor(n_buff) * self.samples_per_buffer)
        if size_new < self.ds_time.size:
            if self.samplerate_sps < 95_000:
                self._logger.debug("skipped alignment due to altered samplerate")
                return
            self._logger.info(
                "aligning with buffer-size, discarding last %s entries",
                self.ds_time.size - size_new,
            )
            self.ds_time.resize((size_new,))
            self.ds_voltage.resize((size_new,))
            self.ds_current.resize((size_new,))

    def __setitem__(self, key, item):
        """A convenient interface to store relevant key-value data (attribute) if H5-structure"""
        return self.h5file.attrs.__setitem__(key, item)

    def set_config(self, data: dict) -> NoReturn:
        """Important Step to get a self-describing Output-File

        :param data: from virtual harvester or converter / source
        """
        self.h5file["data"].attrs["config"] = yaml.safe_dump(
            data, default_flow_style=False, sort_keys=False
        )
        if "window_samples" in data:
            self.set_window_samples(data["window_samples"])

    def set_window_samples(self, samples: int = 0) -> NoReturn:
        """parameter essential for ivcurves

        :param samples: length of window / voltage sweep
        """
        self.h5file["data"].attrs["window_samples"] = samples

    def set_hostname(self, name: str) -> NoReturn:
        """option to distinguish the host, target or data-source in the testbed
            -> perfect for plotting later

        :param name: something unique, or "artificial" in case of generated content
        """
        self.h5file.attrs["hostname"] = name
