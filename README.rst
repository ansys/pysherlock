PySherlock
----------
|pyansys| |python| |pypi| |GH-CI| |codecov| |MIT| |black|

.. |pyansys| image:: https://img.shields.io/badge/Py-Ansys-ffc107.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABDklEQVQ4jWNgoDfg5mD8vE7q/3bpVyskbW0sMRUwofHD7Dh5OBkZGBgW7/3W2tZpa2tLQEOyOzeEsfumlK2tbVpaGj4N6jIs1lpsDAwMJ278sveMY2BgCA0NFRISwqkhyQ1q/Nyd3zg4OBgYGNjZ2ePi4rB5loGBhZnhxTLJ/9ulv26Q4uVk1NXV/f///////69du4Zdg78lx//t0v+3S88rFISInD59GqIH2esIJ8G9O2/XVwhjzpw5EAam1xkkBJn/bJX+v1365hxxuCAfH9+3b9/+////48cPuNehNsS7cDEzMTAwMMzb+Q2u4dOnT2vWrMHu9ZtzxP9vl/69RVpCkBlZ3N7enoDXBwEAAA+YYitOilMVAAAAAElFTkSuQmCC
   :target: https://docs.pyansys.com/
   :alt: PyAnsys

.. |python| image:: https://img.shields.io/pypi/pyversions/ansys-sherlock-core?logo=pypi
   :target: https://pypi.org/project/ansys-sherlock-core/
   :alt: Python

.. |pypi| image:: https://img.shields.io/pypi/v/ansys-sherlock-core.svg?logo=python&logoColor=white
   :target: https://pypi.org/project/ansys-sherlock-core
   :alt: PyPI

.. |codecov| image:: https://codecov.io/gh/pyansys/ansys-sherlock-core/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/pyansys/pysherlock
   :alt: Codecov

.. |GH-CI| image:: https://github.com/pyansys/pysherlock/actions/workflows/ci_cd.yml/badge.svg
   :target: https://github.com/pyansys/pysherlock/actions/workflows/ci_cd.yml
   :alt: GH-CI

.. |MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: MIT

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=flat
   :target: https://github.com/psf/black
   :alt: Black

PySherlock is a Python client library for the Ansys Sherlock product.

Project overview
----------------
ANSYS Sherlock is a reliability physics-based electronics design tool that provides
fast and accurate life predictions for electronic hardware at the component,
board and system levels in early stage design.
The PySherlock library provides Pythonic access to Sherlock's functions, enabling
users to automate and customize their specific workflows.
Below is a list of the currently supported features:

* Launch a Sherlock gRPC server and a Sherlock client
* Import ECAD files and generate project reports
* Define life cycle events and profiles
* Generate a stackup and update a stackup layer
* Update a project parts list
* Perform layer view operations such as updating a mount point's location
* Export a trace or trace reinforcement model for integration with ANSYS Workbench
* Execute one or more analyses

Documentation
-------------
The `PySherlock Client Documentation <https://sherlock.docs.pyansys.com/>`_ contains
information on installation, API documentations, and examples.

License
-------
``PySherlock`` is licensed under the MIT license.

This module allows users access to existing Sherlock functionalities and requires a legally licensed local
copy of Ansys Sherlock.

Please visit `Ansys <http://www.ansys.com>`_ for more information on getting a licensed copy.