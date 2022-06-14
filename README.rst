PySherlock Project Overview
---------------------------
ANSYS Sherlock is a reliability physics-based electronics design tool that provides
fast and accurate life predictions for electronic hardware at the component, 
board and system levels in early stage design.
The PySherlock library provides Pythonic access to Sherlock's functions, enabling
users to automate and customize their specific workflows.
Below is a list of the currently supported features:

* Launch a Sherlock gRPC server and a Sherlock client

.. * Import ECAD files and generate project reports
.. * Define life cycle events and profiles
.. * Generate a stackup and update a stackup layer
.. * Update a project parts list
.. * Perform layer view operations such as updating a component's location
.. * Export a 3D model, material definitions and material assignments for integration with ANSYS Workbench
.. * Execute one or more analyses

Installation
------------
.. Include installation directions.  Note that this README will be
.. included in your PyPI package, so be sure to include ``pip``
.. directions along with developer installation directions.  For example.

Install PySherlock with:

.. code::

   pip install ansys-sherlock-core

Alternatively, clone and install in development mode with:

.. code::

   git clone https://github.com/pyansys/pysherlock
   pip install -e .


Documentation and Issues
------------------------
Documentation link will be provided here once the documentation site becomes available.


Getting Started
---------------
Launch Sherlock Locally
^^^^^^^^^^^^^^^^^^^^^^^
.. code::

    from ansys.sherlock.core import launcher
    sherlock = launcher.launch_sherlock()

This automatically searches for the latest local version of Sherlock, and 
launches the Sherlock gRPC server on port 9090.  It also launches a Sherlock 
client connected to the same port and returns a gRPC connection object 
which can be used to invoke the APIs from their respective services.

Alternatively you can start the Sherlock gRPC server on a different port by 
using the ``port`` parameter. For example:

.. code::

    from ansys.sherlock.core import launcher
    sherlock = launcher.launch_sherlock(port=9092)

Below is an example of using the gRPC connection object to perform a health check on 
the gRPC connection using the SherlockCommonService's check() API:

.. code::

    sherlock.common.check()

.. Example Usage
.. -------------

.. .. code:: python


.. Testing
.. -------
.. You can feel free to include this at the README level or in CONTRIBUTING.md


License
-------
``PySherlock`` is licensed under the MIT license.

This module allows users access to existing Sherlock functionalities and requires a legally licensed local copy of Ansys.

Please visit `Ansys <http://www.ansys.com>`_ for more information on getting a licensed copy.