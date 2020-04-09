import pickle
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
        with open(path, "wb") as f:
            pickle.dump(self.table, f)

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
            self.table = pickle.load(f)
