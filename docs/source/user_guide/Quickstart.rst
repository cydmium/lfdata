.. _quickstart

Quickstart
==========

Before getting started, make sure LF is installed and at the latest version.

Locating the Data
-----------------

Data can be downloaded from `Waldo World`_.
Once you have obtained a set of data, you can move into python.

.. _Waldo World: https://waldo.world/

Getting the filenames of a single path's data is straight forward using :func:`lf.rx.locate_mat`.::

   import lf

   filenames = lf.rx.locate_mat(data_path, date, tx, rx, data_resolution)

Loading the Data
----------------

Once you have the filenames associated with the various mat files, there are a variety of ways to interact with the data.


Single File Loading
^^^^^^^^^^^^^^^^^^^

If you only want the full raw data, you can use scipy's loadmat function.::

   from scipy.io import loadmat

   data = loadmat(filename)

However, if you want a single mat file's data with some helpful data conversion the load_rx_data function becomes useful.::

   data_dict = lf.rx.load_rx_data(mat_file)

It is also possible to select specific variables of interest from the mat_file.
The axample below reads only the data and call_sign information.::

   data_dict = lf.rx.load_rx_data(mat_file, variables=["data", "call_sign"])

By default, load_rx_data verifies that the provided .mat file corresponds to an expect vlf data file.
If you want to disable that functionality, simply pass the optional file_check argument as False.::

   data_dict = lf.rx.load_rx_data(mat_file, file_check=False)

Single Path Loading
^^^^^^^^^^^^^^^^^^^

If you want to work with both channels (N/S and E/W) amplitude and phase data at once, the LF package begins to really show it's worth.
Using the filenames found with the locate_mat function ::

   lfdata = lf.data.LFData(mat_files=filenames)

This class will automatically condense the shared information between the mat files into a single usable object. It will also confirm the four .mat files provided correspond to the same path and time period. 

From here, it's possible to calibrate the data::

   lfdata.calibrate(cal_table)

or compute azimuthal and radial components::

   lfdata.rotate_data()

or visualize the data in a plot::

   lfdata.plot()
