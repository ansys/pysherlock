==========
User Guide
==========
This guide provides a general overview of the basics and usage of the PySherlock
library.

=============
Pre-requisite
=============
Please go to the section `Getting Started <../getting_started/index.html>`_ for installation instructions
and how to launch Sherlock and the gRPC server. The Sherlock gRPC server must be running in order to use
PySherlock.

===================
PySherlock Services
===================
PySherlock methods are divided into modules which corresponds to major Sherlock functional areas.
Please go to the `API Reference <../api/index.html>`_ to see a brief description for each and a
complete list of the available methods, descriptions, and examples.

.. image:: ../_static/sherlock-services.png
  :align: center
  :width: 300
  :alt: Sherlock Services

================
Using PySherlock
================
After the Sherlock gRPC server has started, PySherlock methods can be used to perform operations with
the Sherlock client.

We will illustrate how to use PySherlock to automate the process depicted in the below diagram.

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

``launch_sherlock()`` returns a a gRPC connection object ``sherlock``
which is used to invoke the APIs from their respective services.

.. code::

    from ansys.sherlock.core.launcher import launch_sherlock
    sherlock = launch_sherlock()

--------------------
Import ODB++ Archive
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
Update Parts List
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
Create Random Vibe Event
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
Create Random Vibe Profile
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
Run Analysis
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
Generate Sherlock Report
------------------------
Generate a Sherlock project report for the project ``Tutorial`` using the ``project`` module
``generate_project_report()`` method. The report will be saved in the pdf file
``C:\Temp\tutorial_project_report.pdf``.

.. code::

    sherlock.project.generate_project_report(
            "Tutorial",
            "User Name",
            "Ansys, Inc",
            "C:\\Temp\\tutorial_project_report.pdf"
    )