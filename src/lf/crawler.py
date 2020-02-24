""" Provides locate_mat function

locate_mat determines the file paths for the .mat files correesponding to a
single path on a single day.
"""

import os
import lf.txrx
class DateRange:

    """ Iterator that increments dates"""

    def __init__(self, start, stop=datetime.today(), step=timedelta(days=1)):
        """ Iterate from start date to stop date with time step delta

        Parameters
        ----------
        start : datetime
            Oldest time of interest
        stop : datetime, optional
            Newest time of interest (inclusive)
        step : timedelta, optional
            How much to increment in each loop

        """

        self._date = start
        self._stop = stop
        self._step = step

    def __iter__(self):
        """ Iterator
        Returns
        -------
        DateRange
            returns itself

        """
        return self

    def __next__(self):
        """ Calculate next date

        Returns
        -------
        datetime
            Current time plus step

        """
        date = self._date
        self._date += self._step
        if date > self._stop:
            raise StopIteration
        else:
            return date


def locate_mat(data_path, date, tx, rx, resolution):
    """ Determine the two mat_files associated with the provided Tx-Rx Path

    Parameters
    ----------
    data_path : str
        Path to the data directory containing folders for each receiver
    date : datetime
        Date of interest
    tx : {"NAA", "NLK", "NML"}
        Transmitter of interest
    rx : str
        Receiver of interest
    resolution : {"high", "low"}
        high resolution = 60 Hz, low resolution = 1 Hz

    Returns
    -------
    list of str
        list containig the amplitude and phase .mat files of interest

    """
    if resolution.lower() == "low":
        amp, phase = "A", "B"
    elif resolution.lower() == "high":
        amp, phase = "C", "D"
    else:
        raise ValueError("Resolution must be high or low!")
    receiver = lf.txrx.site_mapping[rx.upper()]
    date_str = date.strftime("%Y_%m_%d")
    filenames = [
        os.path.join(
            data_path,
            receiver,
            date_str,
            "".join(
                [
                    rx.upper(),
                    date.strftime("%y%m%d%H%M%S"),
                    tx.upper(),
                    "_10",
                    str(ch),
                    amp_phase,
                ]
            ),
        )
        for ch in [0, 1]
        for amp_phase in [amp, phase]
    ]
    for filename in filenames:
        if not os.path.exists(filename):
            print(
                f"Data missing from {tx}-{rx} on {date.strftime('%b %d, %Y')}"
            )
            return None
    return filenames
