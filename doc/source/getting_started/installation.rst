.. _installation:

================
Install packages
================

The ``ansy-sherlock`` package supports Python 3.7 through Python 3.10 on Windows.

To use PySherlock, you must download and install both the ``ansys-api-sherlock``
and ``ansys-sherlock`` packages.

.. TODO: uncomment the following lines when PySherlock is released to the public PyPi.
   Install the latest ``ansys-sherlock-core`` package from PyPi with:

..   .. code::

..   pip install ansys-sherlock-core

#. Download the latest ``ansys-api-sherlock`` package by running this
   ``git clone`` command:

   .. code::

      git clone https://github.com/ansys/ansys-api-sherlock.git


   Alternatively, you can download the ZIP file from the **Release** area of the
   `ansys-api-sherlock <https://github.com/ansys/ansys-api-sherlock>`_ GitHub
   repository and unzip it before proceeding with the installation.

#. After the package is downloaded, execute these commands to install it:

   .. code::

      cd ansys-api-sherlock
      pip install -e .

#. Download the latest ``ansys-sherlock`` package by running this
   ``git clone`` command:

   .. code::

      git clone https://github.com/ansys/pysherlock.git

   Alternatively, you can download the ZIP file from the **Release** area of the
   `pysherlock <https://github.com/ansys/pysherlock>`_ GitHub repository
   and unzip it before proceeding with the installation.

#. After the package is downloaded, execute these commands to install it:

   .. code::

      cd pysherlock
      pip install -e .
