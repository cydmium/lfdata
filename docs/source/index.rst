.. lf documentation master file, created by
   sphinx-quickstart on Fri May  8 14:17:58 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

LF
==

**LF** provides a set of useful tools for interacting with data measured by LF AWESOME receivers maintained by the LF Radio Lab at Georgia Tech.
This data is publicly available at `Waldo World`_.

.. _Waldo World: https://waldo.world/

Installation
------------

LF is avaiable in PyPi_!
It can be easily installed through pip.

.. _PyPi: https://pypi.org/project/lf/

::

   pip install lf

Features
--------

LF is designed to simplify interactions with vlf and lf data.

- Easily load a single channel of data
- Verify the mat file contains the expected information
- Locate all .mat files associated with a single tx-rx path
- Store a single tx-rx path's data in a compact data object
- Calibrate tx-rx data based on built-in calibration information
- Convert the data from N/S-E/W channels to Radial-Azimuthal channels
- Plot path data
- Determine the data quality for a single or set of path(s)
- Store data from multiple paths on a single day in a table-like object
- Trim time bounds on data (ex. Pull out only daytime or nighttime data)
- Unwrap phase data
- Median filter data
- Sort through multiple days and determine which paths contain good data on each day
- A variety of utility functions for small functionality not included in the main classes

User Guide
----------

.. toctree::
   :maxdepth: 2

   user_guide/Intro
   user_guide/Quickstart
   

Contact Information
-------------------

.. toctree::
   :maxdepth: 2

   contact


API Reference
-------------

.. toctree::
   :maxdepth: 2

   api/api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

