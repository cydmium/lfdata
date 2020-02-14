# Changelog

The format for this changelog is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to (mostly) [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
All dates listed follow the ISO standard of yyyy-mm-dd.

## [Unreleased]
### Added
- LFData class [David Richardson <drichardson42@gatech.edu>]
    - Main class for interacting with an Rx-Tx path's data
- LFData.load_mats method [David Richardson <drichardson42@gatech.edu>]
    - Load two .mat files into the LFData class
- LFData.load_dicts method [David Richardson <drichardson42@gatech.edu>]
    - Load two dictionaries from load_rx_data into the LFData class
- LFData.combine_data method [David Richardson <drichardson42@gatech.edu>]
    - Combine two dictionaries, one amplitude and one phase, into a set of LFData class attributes
- LFData.to_amp_phase method [David Richardson <drichardson42@gatech.edu>]
    - Convert loaded data to amplitude and phase (default)
- LFData.to_real_imag method [David Richardson <drichardson42@gatech.edu>]
    - Convert loaded data to real and imaginary components
- LFData.to_db method [David Richardson <drichardson42@gatech.edu>]
    - Convert loaded amplitude data to decibels
- LFData.to_lin method [David Richardson <drichardson42@gatech.edu>]
    - Convert loaded amplitude data to linear scale (default)
- LFData.to_rad method [David Richardson <drichardson42@gatech.edu>]
    - Convert loaded phase data to radians
- LFData.to_deg method [David Richardson <drichardson42@gatech.edu>]
    - Convert loaded phase data to degress (default)

### Changed
- Adjust shape of all data arrays (amp_lin, amp_db, phase_deg, phase_rad,
  data_cx, data_real, data_imag) to (N, ) instead of (N,1)
    - Improves ability to iterate of data


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
