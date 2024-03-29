# Changelog

The format for this changelog is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to (mostly) [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
All dates listed follow the ISO standard of yyyy-mm-dd.


## [0.1.9] - 2023-04-10
### Added

### Fixed
 - Change requirements from sklearn to scikit-learn as sklearn has now been deprecated for pip installs
### Changed

### Removed


## [0.1.8] - 2022-07-22
### Added
 - Implement lf.data.rx.scattered_ellipse [Nikhil Pailoor <npailoor3@gatech.edu>]
### Fixed
 - lf.data.rx.load_rx_data had a bug introduced by either scipy changing how it loaded the ascii text into a numpy array. This has now been fixed [Thomas Holder <tholder7@gatech.edu]
### Changed

### Removed


## [0.1.7] - 2022-05-23
### Added
 - Implement lf.data.rx.rotate_vectors function [David Richardson <drichardson42@gatech.edu>]
    - Allows rotations of arbitrary length vectors of N/S, E/W to radial, azimuth
 - Implement lf.data.rx.rotate_vectors_ellipse function [Nikhil Pailoor <npailoor3@gatech.edu>]
    - Allows rotations of arbitrary length vectors of radial, azimuth to parameters of elliptically polarized wave
 - Implement lf.utils.rot_tilt function [Nikhil Pailoor <npailoor3@gatech.edu>]
    - Generates rotation matrix used in lf.data.rx.rotate_vectors_ellipse
 - Implement lf.data.rx.rotate_polar [Nikhil Pailoor <npailoor3@gatech.edu>]
    - Uses lf.data.rx.rotate_vectors_ellipse to generate polarization ellipse parameters for the data field
### Changed
 - Modify lf.data.rx.data.rotate_data to use lf.data.rx.rotate_vector function [David Richardson <drichardson42@gatech.edu>]
### Removed



## [0.1.6] - 2021-01-06
### Added
 - Implement join_days to enable joining of multiple consecutive LFData objects [David Richardson <drichardson42@gatech.edu>]
    - This allows an arbitrarily long sequence of data to be stored in a single object
 - Implement LFData.trim to allow trimming the data to a desired time range [David Richardson <drichardson42@gatech.edu>]
    - This allows the LFData class to store only the data that is of interest
### Changed
 - Fixed a few incorrect docstrings about the number of mat files/data dictionaries required for the LFData class [David Richardson <drichardson42@gatech.edu>]
 - Fixed how eval_day handles an incorrect mat file [David Richardson <drichardson42@gatech.edu>]
### Removed


## [0.1.5] - 2020-12-03
### Added
### Changed
 - Improve rules for daytime quality assessment [David Richardson <drichardson42@gatech.edu>]
    - Particularly focused on improving Arecibo's quality rules
    - Also reduces inconsistency caused by phase wrapping when determining noise
### Removed


## [0.1.4] - 2020-08-24
### Added
 - Documentation is now complete under docs [David Richardson <drichardson42@gatech.edu>]
### Changed
 - Improve in-code documentation [David Richardson <drichardson42@gatech.edu>]

### Removed


## [0.1.3] - 2020-04-20
### Added
- LFTable now includes the list_paths and get_path_data methods [David Richardson <drichardson42@gatech.edu>]
    - These methods should make working with the table easier when attempting to maintain a specific order of paths
- LFTable now has a trim_data method to adjust the time range of the table [David Richardson <drichardson42@gatech.edu>]
    - This addition allows for easily selecting portions of the data to work with
- LFTable now has a plot method [David Richardson <drichardson42@gatech.edu>]
    - Plot can now be used to verify filtering, unwrapping, etc. operations
- LFTable now has unwrap_phase method [David Richardson <drichardson42@gatech.edu>]
    - Unwrapping the phase is useful for determining true signal characteristics
- LFTable now has filt_data [David Richardson <drichardson42@gatech.edu>]
    - Apply a median filter to the data

### Changed
- Fixed dictionary key issue in rxquality.eval_day [David Richardson <drichardson42@gatech.edu>]
    - eval_day was attempting to access paths[day] when it should have been paths[tx]

### Removed


## [0.1.2] - 2020-04-06
### Added
- Added Calibration class to lf.calibration [David Richardson <drichardson42@gatech.edu>]
    - Allows creation of a table of calibration values
- Added cal_lut to calibration_lut.py [David Richardson <drichardson42@gatech.edu>]
    - Provides a look up table of receiver calibration dates and directory names
- Added LFData.calibrate method [David Richardson <drichardson42@gatech.edu>]
    - If a cal_table is passed to LFData, it can now calibrate its data
- lf.data.rxquality.eval_day() function [David Richardson <drichardson42@gatech.edu>]
    - Allows evaluating the paths available for a single day
- lf.data.table.LFTable class [David Richardson <drichardson42@gatech.edu>]
    - LFTable() allows saving a days worth of data with specified paths in a single object

### Changed
- Fixed Arecibo's callsign (AR->AO) [David Richardson <drichardson42@gatech.edu>]
- LFData no longer automatically rotates or calibrates the input data [David Richardson <drichardson42@gatech.edu>]
    - rotate_data and calibrate are now manual calls to improve extensibility
- Crawler.locate_mat was moved to data.rx.locate_mat [David Richardson <drichardson42@gatech.edu>]
    - locate_mat is related to data loading more than crawling through data
- Crawler.crawl was refactored to introduce lf.data.rxquality.eval_day() [David Richardson <drichardson42@gatech.edu>]
    - Improves the extensibility of the module

### Removed


## [0.1.1] - 2020-03-11
### Changed
-  Added matplotlib dependency [David Richardson <drichardson42@gatech.edu>]


## [0.1.0] - 2020-03-11
### Added
- Crawler.crawl() method [David Richardson <drichardson42@gatech.edu>]
    - Implement ability to crawl through all lf data to locate "good" data
- DateRange iterator [David Richardson <drichardson42@gatech.edu>]
    - Iterate through dates similar to how the built-in range iterator functions
- LFData.plot() method [David Richardson <drichardson42@gatech.edu>]
    - Plot amplitude and phase data
- DataQuality.get_quality() method [David Richardson <drichardson42@gatech.edu>]
    - Returns whether the data is "good" according to some rules
- DataQuality now contains significantly more quality metrics [David Richardson
  <drichardson42@gatech.edu>]
    - Noise metrics
    - Daytime specific metrics
- tx_rx_midpoint to lf.utils [David Richardson <drichardson42@gatech.edu>]
    - Calculates the latitude and longitude at the midpoint between a receiver
      and transmitter
- solar_max_time to lf.utils [David Richardson <drichardson42@gatech.edu>]
    - Calculates the time at which the sun is most overhead a lat, lon point

### Changed
- LFData.load_mats now requires 4 mat files (amplitude/phase for both N/S and
  E/W channels) [David Richardson <drichardson42@gatech.edu>]
    - Allow the LFData class to manage all of the data measured by a receiver
- LFData.load_dicts now requires 4 dictionaries (amplitude/phase for both N/S
  and E/W channels) [David Richardson <drichardson42@gatech.edu>]
    - Allow the LFData class to manage all of the data measured by a receiver

### Removed
- LFData.to_amp_phase [David Richardson <drichardson42@gatech.edu>]
    - With the changes to multi-channel this function no longer makes sense
- LFData.to_real_imag [David Richardson <drichardson42@gatech.edu>]
    - With the changes to multi-channel this function no longer makes sense
- LFData.to_db [David Richardson <drichardson42@gatech.edu>]
    - With the changes to multi-channel this function no longer makes sense
- LFData.to_lin [David Richardson <drichardson42@gatech.edu>]
    - With the changes to multi-channel this function no longer makes sense
- LFData.to_rad [David Richardson <drichardson42@gatech.edu>]
    - With the changes to multi-channel this function no longer makes sense
- LFData.to_deg [David Richardson <drichardson42@gatech.edu>]
    - With the changes to multi-channel this function no longer makes sense


## [0.0.5] - 2020-02-17
Note: v0.0.4 was skipped due to a packaging error that prevented the 0.0.4
upload to pypi. v0.0.5 is what v0.0.4 would have been.
### Added
- LFData class [David Richardson <drichardson42@gatech.edu>]
    - Main class for interacting with an Rx-Tx path's data
- LFData.load_mats method to lf.data.rx.rx [David Richardson <drichardson42@gatech.edu>]
    - Load two .mat files into the LFData class
- LFData.load_dicts method to lf.data.rx [David Richardson <drichardson42@gatech.edu>]
    - Load two dictionaries from load_rx_data into the LFData class
- LFData.combine_data method to lf.data.rx [David Richardson <drichardson42@gatech.edu>]
    - Combine two dictionaries, one amplitude and one phase, into a set of LFData class attributes
- LFData.to_amp_phase method to lf.data.rx [David Richardson <drichardson42@gatech.edu>]
    - Convert loaded data to amplitude and phase (default)
- LFData.to_real_imag method to lf.data.rx [David Richardson <drichardson42@gatech.edu>]
    - Convert loaded data to real and imaginary components
- LFData.to_db method to lf.data.rx [David Richardson <drichardson42@gatech.edu>]
    - Convert loaded amplitude data to decibels
- LFData.to_lin method to lf.data.rx [David Richardson <drichardson42@gatech.edu>]
    - Convert loaded amplitude data to linear scale (default)
- LFData.to_rad method to lf.data.rx [David Richardson <drichardson42@gatech.edu>]
    - Convert loaded phase data to radians
- LFData.to_deg method to lf.data.rx [David Richardson <drichardson42@gatech.edu>]
    - Convert loaded phase data to degress (default)
- DataQuality class to lf.data.rxquality [David Richardson <drichardson42@gatech.edu>]
    - Track data quality metrics
- EvalLF class to lf.data.rxquality [David Richardson <drichardson42@gatech.edu>]
    - Various methods for evaluating LF data quality
- EvalLF.load_config to lf.data.rxquality [David Richardson <drichardson42@gatech.edu>]
    - Loads configuration file for evaluation parameters
- EvalLF.eval_receiver to lf.data.rxquality [David Richardson
  <drichardson42@gatech.edu>]
    - Evaluate the functionality of the receiver
- EvalLF.eval_amp to lf.data.rxquality [David Richardson <drichardson42@gatech.edu>]
    - Evaluate the quality of the amplitude data
- EvalLF.eval_phase to lf.data.rxquality [David Richardson <drichardson42@gatech.edu>]
    - Evaluate the quality of the phase data
- findNans to lf.utils [David Richardson <drichardson42@gatech.edu>]
    - Function for finding the location of nans in an array
- repeatedNans to lf.utils [David Richardson <drichardson42@gatech.edu>]
    - Function for finding consecutive nans in an array

### Changed
- Adjust shape of all data arrays (amp_lin, amp_db, phase_deg, phase_rad,
  data_cx, data_real, data_imag) to (N, ) instead of (N,1) [David Richardson
  <drichardson42@gatech.edu>]
    - Improves ability to iterate through data
- Modules have been adjusted to fit into the lf package. [David Richardson
  <drichardson42@gatech.edu>]
    - To import, now use lf.data.rx, lf.data.rxquality, lf.utils

### Removed
- As noted in the changed section, the lfdata module has been removed in favor
  of the more modular lf.x scheme [David Richardson <drichardson42@gatech.edu>]
    - The previous lfdata module is now available as lf.data.rx


## [0.0.3] - 2020-02-12
### Changed
 - Fixed README to correctly indicate data_loader->load_rx_data rename [David Richardson <drichardson42@gatech.edu>>]


## [0.0.2] - 2020-02-12
### Changed
 - Renamed data_loader function to load_rx_data [David Richardson <drichardson42@gatech.edu>]
     - See removal note

### Removed
 - data_loader function is no longer available [David Richardson <drichardson42@gatech.edu>]
     - data_loader was replaced by load_rx_data to reduce name confusion with DataLoaders used in pytorch

## [0.0.1] - 2020-02-12
### Added
 - data_loader function [David Richardson <drichardson42@gatech.edu>]
     - Loads LF .mat file into a dictionary
     - Formats the dictionary to improve usability
