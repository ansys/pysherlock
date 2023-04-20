==========
User guide
==========
This section provides a basic overview of how to use PySherlock.

==============
Prerequisites
==============
See the `Getting started <../getting_started/index.html>`_ for installation instructions
and information on how to launch Sherlock and the gRPC server. The Sherlock gRPC server
must be running to use PySherlock.

===================
PySherlock services
===================
This section describes PySherlock core classes, methods, and functions that correspond to major
Sherlock functional areas. Use the search feature or click links to view API documentation.

.. image:: ../_static/sherlock-services.png
  :align: center
  :width: 300
  :alt: Sherlock Services

================
Using PySherlock
================
After the Sherlock gRPC server has started, you can use PySherlock methods to perform operations with
the Sherlock client.

Subsequent topics describe how to use PySherlock to automate the process depicted in this diagram:

.. image:: ../_static/userGuide-example-workflow-chart.png
  :align: center
  :width: 600
  :alt: User Guide Example Workflow

.. Below is a workflow that demonstrates how to launch sherlock, import an ODB++ archive to create a
.. new project, update the parts list, create a random vibe event and profile, run a random vibe analysis,
.. and generate a project report.

---------------
Launch Sherlock
---------------
Launch Sherlock and start the gRPC server on default port 9090 using the ``launcher`` module
``launch_sherlock()`` method.
Please go to the `launcher module documentation <../api/launcher.html>`_ to see detailed documentation
on this module and its methods.

The ``launch_sherlock()`` method returns a ``sherlock`` gRPC connection object.
This object is used to invoke the APIs from their respective services.

.. code::

    from ansys.sherlock.core.launcher import launch_sherlock
    sherlock = launch_sherlock()

--------------------
Import ODB++ archive
--------------------
Import an ODB++ archive ``ODB++ Tutorial.tgz`` using the ``project`` module ``import_odb_archive()`` method.
After the import, a project named ``Tutorial`` is created with a CCA named ``Main Board``.
Please go to the `project module documentation <../api/project.html>`_ to see detailed documentation
on this module and its methods.

.. code::

    sherlock.project.import_odb_archive(
            "C:\\Temp\\ODB++ Tutorial.tgz",
            True,
            True,
            True,
            True,
            project="Tutorial",
            cca_name="Main Board"
    )

-----------------
Update parts list
-----------------
Update the parts list for the previously created CCA ``Main Board`` using the ``parts`` module
``update_parts_list()`` method. The example below updates the parts list by using the Sherlock Part Library.
Please go to the `parts module documentation <../api/parts.html>`_ to see detailed documentation
on this module and its methods.

.. code::

    sherlock.parts.update_parts_list(
            "Tutorial",
            "Main Board",
            "Sherlock Part Library",
            "Both",
            "Error"
    )

------------------------
Create random vibe event
------------------------
Create a random vibe event using the ``lifecycle`` module ``add_random_vibe_event()`` method.
Please go to the `lifecycle module documentation <../api/lifecycle.html>`_ to see detailed documentation
on this module and its methods.

.. code::

    sherlock.lifecycle.add_random_vibe_event(
            "Tutorial",
            "Phase 1",
            "RVEvent 1",
            100,
            "ms",
            0.5,
            "PER MIN",
            "0,0",
            "Uniaxial",
            "0,0,-1"
    )

--------------------------
Create random vibe profile
--------------------------
Create a random vibe profile using the ``lifecycle`` module ``add_random_vibe_profile()`` method.

.. code::

    sherlock.lifecycle.add_random_vibe_profile(
            "Tutorial",
            "Phase 1",
            "RVEvent 1",
            "Profile 1",
            "HZ",
            "G2/Hz",
            [(30.4, 7.61e-5), (204, 0.1), (296, 0.06), (385, 0.06), (454, 0.03), (497, 0.06)]
    )

------------
Run analysis
------------
Run a random vibe analysis using the ``analysis`` module ``run_analysis()`` method.
Please go to the `analysis module documentation <../api/analysis.html>`_ to see detailed documentation
on this module and its methods.

.. code::

    sherlock.analysis.run_analysis(
            "Tutorial",
            "Main Board",
            [
                ("RANDOMVIBE",
                [
                    ("Phase 1", ["RVEvent 1"])
                ]
                )
            ]
    )

------------------------
Generate Sherlock report
------------------------
Generate a Sherlock project report for the project ``Tutorial`` using the ``project`` module
``generate_project_report()`` method. The report is saved in the PDF file
``C:\Temp\tutorial_project_report.pdf``.

.. code::

    sherlock.project.generate_project_report(
            "Tutorial",
            "User Name",
            "Ansys, Inc",
            "C:\\Temp\\tutorial_project_report.pdf"
    )