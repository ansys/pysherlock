.. _installation:

================
Install packages
================

The ``ansys-sherlock-core`` package supports Python 3.7 through Python 3.10 on Windows.

To use PySherlock, you must download and install both the ``ansys-api-sherlock``
and ``ansys-sherlock-core`` packages. By using ``pip``, ``ansys-api-sherlock`` is
installed as part of ``ansys-sherlock-core``. Run the following to install

the publicly distributed version of the package.

.. code::

   pip install ansys-sherlock-core

If you want to install the ``ansys-api-sherlock`` and ``ansys-sherlock-core`` packages
from its source code directly, follow the upcoming instructions:

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

#. Download the latest ``ansys-sherlock-core`` package by running this
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
