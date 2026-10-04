.. _installation:

================
Install packages
================

The ``ansys-sherlock-core`` package supports Python 3.10 through Python 3.13 on Windows and Linux.

To use PySherlock, you must download and install both the ``ansys-api-sherlock``
and ``ansys-sherlock-core`` packages. By using ``pip``, ``ansys-api-sherlock`` is
installed as part of ``ansys-sherlock-core``.
Run the following to install the latest publicly distributed version of the package.

.. code::

   pip install ansys-sherlock-core

The following table shows the version of PySherlock to use for each release of Sherlock:

+------------+----------+
| PySherlock | Sherlock |
+============+==========+
| 0.4        | 2024 R1  |
+------------+----------+
| 0.6        | 2024 R2  |
+------------+----------+
| 0.8        | 2025 R1  |
+------------+----------+
| 0.9        | 2025 R2  |
+------------+----------+
| 1.0        | 2026 R1  |
+------------+----------+

To install a specific version of PySherlock, use the following command, where the <version> is one
of the values in the table preceding:

.. code::

   pip install ansys-sherlock-core==<version>


If you want to install the ``ansys-api-sherlock`` and ``ansys-sherlock-core`` packages
from its source code directly, follow these instructions.

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
