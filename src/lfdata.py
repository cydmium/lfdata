""" Provides the LFData class and load_rx_data function

LFData holds all data reported by the LF AWESOME receiver and includes several
preprocessing operations.
data_loader provides a quick way of converting the .mat files provided by the
LF AWESOME receiver to a python dictionary.
"""

from datetime import datetime
from scipy.io import loadmat


def load_rx_data(mat_file, variables=None, file_check=True):
    """ Properly format an LF AWESOME receiver's output mat file

    Parameters
    ----------
    mat_file : string
        File path to a specific .mat file
    variables : list of strings, optional
        List of variables to be extracted from the .mat file
    file_check : boolean, optional
        Flag to check whether the input mat_file and variables are valid

    Returns
    -------
    dict
        dictionary containing formatted LF Data

    See Also
    --------
    LFData : Data management class
    """
    if file_check:
        validity = check_mat(mat_file, variables)
        if not validity["mat_file"]:
            raise ValueError("Input .mat file is not a valid data file.")
        elif not validity["variables"]:
            raise ValueError(
                "One or more variables are not contained in the .mat file."
            )
    data = loadmat(mat_file, mat_dtype=True, variable_names=variables)
    for key in data:
        if key in [
            "start_year",
            "start_month",
            "start_day",
            "start_hour",
            "start_minute",
            "start_second",
            "Fs",
            "adc_channel_number",
        ]:
            # Should be integers, but aren't by default
            data[key] = int(data[key][0][0])
        elif key in [
            "latitude",
            "longitude",
            "altitude",
            "gps_quality",
            "adc_sn",
            "adc_type",
            "antenna_bearings",
            "cal_factor",
            "computer_sn",
            "gps_sn",
            "station_description",
        ]:
            # Correct type, but in array
            data[key] = data[key][0][0]
        elif key in ["is_amp", "is_msk"]:
            # Should be boolean
            data[key] = bool(data[key][0][0])
        elif key in [
            "hardware_description",
            "station_name",
            "call_sign",
            "VERSION",
        ]:
            # Should be strings, but are in array of ascii
            data[key] = "".join(chr(char) for char in data[key])
    time_vals = [
        "start_year",
        "start_month",
        "start_day",
        "start_hour",
        "start_minute",
        "start_second",
    ]
    # If all of the time data is loaded, create a datetime object
    if (variables is None) or all(elem in variables for elem in time_vals):
        data["start_time"] = datetime(
            data.pop("start_year"),
            data.pop("start_month"),
            data.pop("start_day"),
            data.pop("start_hour"),
            data.pop("start_minute"),
            data.pop("start_second"),
        )

    return data


def check_mat(mat_file, variables=None):
    """ Check if a .mat file is a valid LF data mat file

    Parameters
    ----------
    mat_file : string
        Path to .mat file
    variables : list of str, optional
        List of variables of interest

    Returns
    -------
    Dict
        Dictionary of booleans for the validity of the mat_file and variables

    """
    data = loadmat(mat_file)
    expected_keys = [
        "latitude",
        "longitude",
        "altitude",
        "Fs",
        "gps_quality",
        "adc_channel_number",
        "adc_sn",
        "adc_type",
        "antenna_bearings",
        "antenna_description",
        "cal_factor",
        "computer_sn",
        "gps_sn",
        "hardware_description",
        "is_broadband",
        "station_description",
        "station_name",
        "VERSION",
        "is_amp",
        "is_msk",
        "Fc",
        "call_sign",
        "filter_taps",
        "data",
        "start_second",
        "start_minute",
        "start_hour",
        "start_day",
        "start_month",
        "start_year",
    ]
    validity = {}
    validity["mat_file"] = True
    validity["variables"] = True
    if set(data.keys()) != set(expected_keys):
        validity["mat_file"] = False
    if variables is not None:
        if not all(elem in expected_keys for elem in variables):
            validity["variables"] = False
    return validity
