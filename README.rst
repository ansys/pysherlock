PySherlock
==========

Overview
--------
Ansys Sherlock is a reliability physics-based electronics design tool that provides
fast and accurate life predictions for electronic hardware at the component, 
board, and system levels in early stage design.

PySherlock provides Pythonic access to Sherlock's functions, enabling
users to automate and customize their specific workflows.
With PySherlock, you can perform many tasks, including these:

* Launch a Sherlock gRPC server and a Sherlock client
* Import ECAD files and generate project reports
* Define lifecycle events and profiles
* Generate a stackup and update a stackup layer
* Update a project parts list
* Perform layer view operations such as updating a mount point's location
* Export a trace or trace reinforcement model for integration with Ansys Workbench
* Execute one or more analyses

Documentation and issues
------------------------
For comprehensive information on PySherlock, see the latest release
`documentation <https://sherlock.docs.pyansys.com/>`_.

On the `PySherlock Issues <https://github.com/pyansys/pysherlock/issues>`_ page,
you can create issues to submit questions, report bugs, and request new features.
This is the best place to post questions and code.

License
-------
PySherlock is licensed under the MIT license.

PySherlock makes no commercial claim over Ansys whatsoever. This library extends the functionality
of Ansys Sherlock by adding a Python interface to Sherlock without changing the core behavior
or license of the original software. The use of the interactive control of PySherlock requires
a legally licensed local copy of Sherlock.

For more information on Sherlock, see the `Ansys Sherlock <https://www.ansys.com/products/structures/ansys-sherlock>`_
page on the Ansys website.