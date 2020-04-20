import pickle
import numpy as np
import lf


class LFTable(object):

    """ Save one days worth of lf data into an easily managed object"""

    def __init__(self):
        """ Create the layout of the table"""
        self.table = {}

    def populate(self, day, paths, data_dir, cal_table=None, resolution="low"):
        """TODO: Docstring for  populate.

        Parameters
        ----------
        day : datetime.date or datetime.datetime
            Day of interest
        paths : dict
            Dictionary of desired paths
        data_dir : str
            Path to data directory
        cal_table : calibration.Calibration, optional
            Table of calibration information
        resolution : {"low", "high"}, optional
            Resolution of measured data

        Returns
        -------
        None

        """
        self.fs = 1 if resolution == "low" else 60
        self.day = day
        for tx, rxs in paths.items():
            if not rxs:
                # Skip empty transmitters
                continue
            self.table[tx] = {}
            for rx in rxs:
                mats = lf.data.rx.locate_mat(data_dir, day, tx, rx, resolution)
                if not mats:
                    # mats will only be none if data was not recorded
                    raise RuntimeError(f"Data is missing for {tx}-{rx}")
                data = lf.data.rx.LFData(mats)
                if cal_table:
                    data.calibrate(cal_table)
                data.rotate_data()
                self.table[tx][rx] = data.data["Az"]

    def list_paths(self):
        """ Determine which paths contain data

        Returns
        -------
        list:
            sorted list of strings containing the paths present in the table

        """
        path_list = []
        for tx, rxs in self.table.items():
            for rx in rxs.keys():
                path_list.append(f"{tx}-{rx}".upper())
        path_list.sort()
        return path_list

    def get_path_data(self, path):
        """ Locate data from a single path

        Parameters
        ----------
        path : str
            tx-rx of interest

        Returns
        -------
        list
            [amplitude, phase] data for the path

        """
        tx, rx = path.split("-")
        return self.table[tx][rx]

    def trim_data(self, start, stop):
        """ trim data outside start and stop times

        Parameters
        ----------
        start : datetime.time
            start time (needs hr, min, sec) inclusive
        stop : datetime.time
            stop time (needs hr, min, sec) exclusive

        Returns
        -------
        None

        """
        time = np.arange(86400, step=1 / self.fs)
        start_time = start.hour * 3600 + start.minute * 60 + start.second
        stop_time = stop.hour * 3600 + stop.minute * 60 + stop.second
        time_bool = np.logical_and(time >= start_time, time < stop_time)
        for tx, rxs in self.table.items():
            for rx in rxs.keys():
                self.table[tx][rx] = self.table[tx][rx][0][time_bool]
                self.table[tx][rx] = self.table[tx][rx][1][time_bool]

    def save(self, path):
        """ Save the current table to path

        Parameters
        ----------
        path : str
            Path to save location

        Returns
        -------
        None

        """
        save_dict = {"table": self.table, "day": self.day, "fs": self.fs}
        with open(path, "wb") as f:
            pickle.dump(save_dict, f)

    def load(self, path):
        """ Load a previous table

        Parameters
        ----------
        path : str
            Path to existing table

        Returns
        -------
        None

        """
        with open(path, "rb") as f:
            load_dict = pickle.load(f)
        self.table = load_dict["table"]
        self.day = load_dict["day"]
        self.fs = load_dict["fs"]
