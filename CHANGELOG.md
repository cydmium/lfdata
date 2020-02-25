# Changelog

The format for this changelog is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to (mostly) [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
All dates listed follow the ISO standard of yyyy-mm-dd.

## Unreleased
### Added
- Crawler.crawl() method
    - Implement ability to crawl through all lf data to locate "good" data
- DateRange iterator
    - Iterate through dates similar to how the built-in range iterator functions
- LFData.plot() method
    - Plot amplitude and phase data
- DataQuality.get_quality() method
    - Returns whether the data is "good" according to some rules

### Changed
- LFData.load_mats now requires 4 mat files (amplitude/phase for both N/S and
  E/W channels) [David Richardson <drichardson42@gatech.edu>]
    - Allow the LFData class to manage all of the data measured by a receiver
- LFDate.load_dicts now requires 4 dictionaries (amplitude/phase for both N/S
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
