.. _Advanced Usage:

Advanced Usage
==============

This page is written to demonstrate all of the features of the LF package as well as provide some understanding of what is happening under the hood.
It is assumed that you have read the :ref:`Quickstart Guide<Quickstart>`, but there may be some duplicate information here.

Locating Data Files
-------------------

The LF Package includes a function for locating the mat files corresponding to a date, transmitter, receiver, and resolution. 
This function requires that your data files are named according to the same naming convention and directory structure used on `Waldo World`_.
For example, the low resolution data measured at Baxley on January 6, 2016 from the NAA transmitter must be stored in::

<path of your choice>/Baxley/2016_01_06/BX160106000000NAA_100A.mat
<path of your choice>/Baxley/2016_01_06/BX160106000000NAA_100B.mat
<path of your choice>/Baxley/2016_01_06/BX160106000000NAA_101A.mat
<path of your choice>/Baxley/2016_01_06/BX160106000000NAA_101B.mat

.. _Waldo World: https://waldo.world/narrowband-data/

The data is separated into amplitude (A) and phase (B) for both channels (0, 1).
It is still possible to use the LF package without following this directory structure, but doing so will prevent the use of the :func:`lf.data.rx.locate_mat` function.

Loading Data Files
------------------

Once the data file(s) of interest have been located, the LF package provides a number of ways for loading the data. 
If you are only interested in a single .mat file, the :func:`lf.data.rx.load_rx_data` function is of most use.
When loading an LF .mat file in python, there are some issue with type conversion.
In particular, most strings become lists of ascii codes.
The :func:`lf.data.rx.load_rx_data` function resolves all of these type conversions as well as converts the year, month, day, hour, minute, second time variables into a single datetime object. 
An optional argument is provided to check the validity of the .mat file to insure all of the expected variables have been saved.
If you are using narrowband data from the GT receivers, this should always pass.
A look up table is also utilized to map the site abbreviation to a full site name for easier use. 
Some example usage is shown in the :ref:`Quickstart Guide<quickstart>`.

For most use cases, all of the data for a single path will be of interest.
The :class:`lf.data.rx.LFData` class allows for easy loading of a path's data.
When initializing the object, either a list of four mat files (passed as strings) or four dictionaries must be provided. 
It is important to note the order of the lists are important.
They must be in the [N/S amp, N/S phase, E/W amp, E/W phase] order.
N/S corresponds to channel 0, E/W corresponds to channel 1 in the standard filename convention.
Internally, the :func:`lf.data.rx.load_rx_data` function is called with the validity check enabled.
If runtime is important to your application, you should instead manually load the four dictionaries using :func:`lf.data.rx.load_rx_data` with the validity check disabled then pass the outputs to :class:`lf.data.rx.LFData`.
Regardless of how the data is passed to the object, the common information between the various data files are compared and consolidated to simplify the interface and reduce storage overhead.
Once the data is loaded, the :class:`lf.data.rx.LFData` object provides a few methods for manipulating the data.
The :meth:`lf.data.rx.LFData.rotate_data` method rotates the data to correspond to radial and azimuthal component relative to the transmitter.
In many cases, this interpretation of the data provides more information since the majority of the tranmitter's signal will be contained in the azimuthal component.
The implementation of this relies on a :ref:`utility<Utility Functions>` function (:func:`lf.utils.rot_az`) which will be discussed later.
The :meth:`lf.data.rx.LFData.plot` will intelligently generate a plot based on whether the data has been rotated or not.
If the data has been rotated, it will plot all of the available polarizations, otherwise, it will only plot N/S and E/W.
Calibrating the data is done through combination of a :class:`lf.calibration.Calibration` table (discussed :ref:`below<Calibrating the Data>`) and the :class:`lf.data.rx.LFData` object.

.. _Calibrating the Data:

Calibrating the Data
--------------------

Data calibration is managed by the :class:`lf.calibration.Calibration` class.
This class relies on additional .mat files containing calibration information which are stored in a single directory.
This directory is used to initialize the calibration table prior to creating the table.
Once the table is created or loaded, additional functionality opens up.
It is possible to check the dates of receiver calibrations using the :meth:`lf.calibration.Calibration.get_cal_date` method.
This is used internally in the :meth:`lf.calibration.Calibration.cal_data` method to determine which calibration values should be applied to the data.
There are also :meth:`lf.calibration.Calibration.save_table` and :meth:`lf.calibration.Calibration.load_table` for both saving and loading calibration tables.
A single calibration table is capable of handling data from any receiver on any date.


After the table is setup, data can either be manually calibrated using the previously mentions :meth:`lf.calibration.Calibration.cal_data` method, or automatically managed by the :class:`lf.data.rx.LFData` object. 
It is generally preferable to use the automatic method to avoid writing code that already exists. 

.. _Utility Functions:

Utility Functions
-----------------

Many of these utility functions are not directly related to VLF data (and should probably be moved to a separate package), but they were useful in various methods and functions.
The :func:`lf.utils.findNans` function determines the start and stop indices of NaN values in a 1D array.
This functionlity is very useful for determining periods of receiver downtime which are viewed as NaNs. ::

   lf.utils.findNans(np.array([0, 1, 2, np.nan, np.nan, 5, 6, 7, np.nan, np.nan, np.nan, 11]))
      array([3, 5, 8, 11])

:func:`lf.utils.repeatedNans` extends the :func:`lf.utils.findNans` function by determining the length of consecutive NaNs in a 1D array.
This makes it simple to compute the length of time a receiver was offline. ::

   lf.utils.repeatedNans(np.array([0, 1, 2, np.nan, np.nan, 5, 6, 7, np.nan, np.nan, np.nan, 11]))
      array([2, 3])

The :func:`lf.utils.get_azimuth` function computes the azimuth angle between the receiver and transmitter.
This functionality allows for computing the radial and azimuthal polarization components from the measured N/S and E/W components.
The code for this function is heavily based on code written by Nick Gross for his Ph.D. dissertation. ::

   lf.utils.get_azimuth("OX", "NAA")
      52.40240527577832

:func:`lf.utils.rot_az` provides a simple rotation matrix to use in conjunction with :func:`lf.utils.get_azimuth`. 
The matrix is based on the sin and cos of the angle provided as input.::

   rotation_matrix = lf.utils.rot_az(lf.utils.get_azimuth("OX", "NAA"))

Computing the midpoint of tx-rx path is useful for finding an "average" lat, lon to characterize the path.
It can also be used for computing the time at which the sun is most overhead along the path.
This functionality is implemented in :func:`lf.utils.tx_rx_midpoint`. 
NOTE: The input order of rx, tx is reversed compared to :func:`lf.utils.get_azimuth`.
This will be fixed in a later release, but fixing it will break large sections of code that need to be adjusted first.::

   lat, lon = lf.utils.tx_rx_midpoint(tx, rx)
   lf.utils.tx_rx_midpoint("OX", "NAA")
      (40.06656767, -79.15781682)

