.. _installation:

============
Installation
============

The ``ansy-sherlock`` package supports Python 3.7 through
Python 3.10 on Windows.

================
Install packages
================

To use PySherlock, you must download and install both the ``ansys-api-sherlock``
and ``ansys-sherlock`` packages.

.. TODO: uncomment the following lines when PySherlock is released to the public PyPi.
   Install the latest ``ansys-sherlock-core`` package from PyPi with:

..   .. code::

..   pip install ansys-sherlock-core

#. Download the latest ``ansys-api-sherlock`` package either by using the following
   ``git clone`` command or downloading the zipped file from the GitHub
   `ansys-api-sherlock repository <https://github.com/pyansys/ansys-api-sherlock>`_.

   .. code::

      git clone https://github.com/pyansys/ansys-api-sherlock.git

#. After the pacakge is downloaded, execute these commands to install it:

   .. code::

      cd ansys-api-sherlock
      pip install -e .

#. Download the latest ``ansys-sherlock`` package either by using the following
   ``git clone`` command or downloading the zipped file from the GitHub
   `pysherlock repository <https://github.com/pyansys/pysherlock>`_.
   
   .. code::

      git clone https://github.com/pyansys/pysherlock.git

#. After the package is downloaded, execute these commands to install it:

   .. code::

      cd pysherlock
      pip install -e .

