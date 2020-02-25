""" Provides the DataQuality and EvalData class

DataQuality provides a data structure for storing the quality of LF data
EvalData provides a set of evaluation methods for determining the quality of
data stored in an LFData object
"""

from configparser import ConfigParser
import numpy as np
from sklearn.linear_model import LinearRegression
import lf


class DataQuality(object):

    """ Store quality metrics for LF Data"""

    def __init__(self):
        """ Initilize quality metrics to None """
        metrics = [
            "total_time_off",
            "longest_time_off",
            "total_daytime_off" "time_under_threshold",
            "full_day",
            "tx_on",
            "phase_slope",
            "phase_yint",
        ]
        for metric in metrics:
            setattr(self, metric, None)

    def get_quality(self, config=None):
        """ Take the current quality data and determine if that is good enough

        Returns
        -------
        bool:
            True is good enough, False is not

        """
        return True
        if self.total_time_off > 86400:
            return False
        elif self.longest_time_off > 86400:
            return False
        elif self.total_daytime_off > 86400:
            return False
        elif self.time_under_threshold > 86400:
            return False
        elif not self.full_day:
            return False
        elif not self.tx_on:
            return False
        elif self.phase_slope > 0:
            return False
        return True


class EvalLF(object):

    """ Evaluate the quality of LF Data"""

    def __init__(self, lf_data, config=None):
        """ Initiliaze config file if supplied

        Parameters
        ----------
        lf_data : LFData
            Object containing one path of data
        config : str
            Path to config file with quality rules
        """
        self.data = lf_data
        if config is not None:
            self.load_config(config)
        else:
            self.config = None
        self.quality = DataQuality()

    def load_config(self, config):
        """ Load a config into the object

        Parameters
        ----------
        config : str
            Path to config file

        """
        self.config = ConfigParser()
        self.config.read(config)

    def eval_receiver(self):
        """ Determine the quality of the receiver

        Returns
        -------
        None

        """
        amp_data = self.data.data["Az"][0]
        phase_data = self.data.data["Az"][1]
        # Check for 86400 seconds worth of data
        if len(amp_data) != 86400 * self.data.Fs:
            self.quality.full_day = False
        else:
            self.quality.full_day = True
        try:
            off_time_amp = lf.utils.repeatedNans(amp_data) / self.data.Fs
        except TypeError:
            off_time_amp = 0.0
        try:
            off_time_phase = lf.utils.repeatedNans(phase_data) / self.data.Fs
        except TypeError:
            off_time_phase = 0.0
        time = np.linspace(0, 86400, 86400 * self.data.Fs)
        # Define daytime as 9 AM to 5 PM EST = 14-22 UT
        daytime = np.logical_and(time >= 50400, time <= 79200)
        try:
            off_daytime_phase = (
                lf.utils.repeatedNans(phase_data[daytime]) / self.data.Fs
            )
        # Type error if repeatedNans finds no Nans
        except TypeError:
            off_daytime_phase = 0.0
        if np.any(off_time_amp != off_time_phase):
            print("Amplitude and phase data differ in off time. Please Verify")
        else:
            self.quality.total_time_off = np.sum(off_time_phase)
            self.quality.longest_time_off = np.max(off_time_phase)
            self.quality.total_daytime_off = np.sum(off_daytime_phase)

    def eval_amp(self):
        """ Evaluate the amplitude data

        Returns
        -------
        Float
            Time under the desired threshold
        """
        if self.config is not None:
            threshold = float(self.config["EvalInfo"]["AmplitudeThreshold"])
        else:
            threshold = 10.0
        data = 20 * np.log10(self.data.data["Az"][0])
        # Remove Nans
        data = data[np.invert(np.isnan(data))]
        low_signal = data[data < threshold]
        time_under_threshold = len(low_signal) / self.data.Fs
        self.quality.time_under_threshold = time_under_threshold
        if np.isclose([time_under_threshold], [28800], rtol=0, atol=7200)[0]:
            self.quality.tx_on = False
        elif time_under_threshold > 28800:
            self.quality.tx_on = False
        else:
            self.quality.tx_on = True
        return self.quality.time_under_threshold

    def eval_phase(self):
        """ Determine whether the phase is ramping

        Returns
        -------
        tuple
            (slope, intercept) of phase data

        """
        data = np.copy(self.data.data["Az"][1])
        # Replace Nans with value on either side
        idx = lf.utils.findNans(data)
        if idx is not None:
            for start, stop in zip(idx[::2], idx[1::2]):
                # Prefer value before nan string unless at beginning of array
                if start == 0:
                    data[range(start, stop)] = data[stop]
                else:
                    data[range(start, stop)] = data[start - 1]
        # Fit linear model to determine slope
        time = np.linspace(0, 24, len(data)).reshape((-1, 1))
        unwrapped = np.unwrap(data)
        model = LinearRegression().fit(time, unwrapped)
        self.quality.phase_slope = model.coef_[0]
        self.quality.phase_yint = model.intercept_
        return (self.quality.phase_slope, self.quality.phase_yint)
