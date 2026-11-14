.. _ref_contributing:

==========
Contribute
==========
Overall guidance on contributing to a PyAnsys library appears in the
`Contributing <https://dev.docs.pyansys.com/how-to/contributing.html>`_ topic
in the *PyAnsys Developer's Guide*. Ensure that you are thoroughly familiar with
this guide before attempting to contribute to PySherlock.

The following contribution information is specific to PySherlock.

Post issues
-----------

Use the `PySherlock Issues <https://github.com/ansys/pysherlock/issues>`_
page to submit questions, report bugs, and request new features. When possible, you
should use these issue templates:

* Bug report template
* Feature request template

If your issue does not fit into these categories, create your own issue.

To reach the PyAnsys team, email `pyansys.core@ansys.com <pyansys.core@ansys.com>`_.

View documentation
------------------

Documentation for the latest stable release of PySherlock is hosted at
`PySherlock Documentation <https://sherlock.docs.pyansys.com>`_.

In the upper right corner of the documentation’s title bar, there is an option
for switching from viewing the documentation for the latest stable release to
viewing the documentation for the development version or previously released versions.

Code style
----------

PySherlock follows the PEP8 standard as outlined in the `PyAnsys Development Guide
<https://dev.docs.pyansys.com>`_ and implements style checking using
`pre-commit <https://pre-commit.com/>`_.

To ensure your code meets minimum code styling standards, run::

  pip install pre-commit
  pre-commit run --all-files

You can also install this as a pre-commit hook by running::

  pre-commit install

This way, it's not possible for you to push code that fails the style checks. For example::

  $ pre-commit install
  $ git commit -am "added my cool feature"
  black....................................................................Passed
  blacken-docs.............................................................Passed
  isort....................................................................Passed
  flake8...................................................................Passed
  codespell................................................................Passed
  pydocstyle...............................................................Passed
  check for merge conflicts................................................Passed
  debug statements (python)................................................Passed
  check yaml...............................................................Passed
  trim trailing whitespace.................................................Passed
  Validate GitHub Workflows................................................Passed

Install the package
-------------------

PySherlock has three installation modes: user, developer, and offline.

Install in user mode
^^^^^^^^^^^^^^^^^^^^

Before installing PySherlock in user mode, use this command to make sure that
you have the latest version of `pip`_:

.. code:: bash

   python -m pip install -U pip

Then, use this command to install PySherlock:

.. code:: bash

   python -m pip install ansys-sherlock-core


Install in developer mode
^^^^^^^^^^^^^^^^^^^^^^^^^
To install PySherlock in developer mode, run these commands:

.. code:: bash

   git clone https://github.com/ansys/python-installer-qt-gui
   cd python-installer-qt-gui
   pip install pip -U
   pip install -e .

Then run this command:

.. code:: bash

   ansys_python_installer

**Details**

Installing PySherlock in developer mode allows you to modify the source
and enhance it.

Before contributing to the project, see the `PyAnsys Developer's
guide <https://dev.docs.pyansys.com/>`_. You must follow these steps:

#. Start by cloning this repository:

   .. code:: bash

      git clone https://github.com/ansys/pysherlock

#. Create a fresh-clean Python environment and activate it:

   .. code:: bash

      # Create a virtual environment
      python -m venv .venv

      # Activate it in a POSIX system
      source .venv/bin/activate

      # Activate it in Windows CMD environment
      .venv\Scripts\activate.bat

      # Activate it in Windows Powershell
      .venv\Scripts\Activate.ps1

   If you require additional information on virtual environments, see the
   official Python `venv <https://docs.python.org/3/library/venv.html>`_ topic.

#. To make sure you have the latest version of `pip <https://pypi.org/project/pip/>`_,
   run this command:

   .. code:: bash

      python -m pip install -U pip

#. Install the project in editable mode by running the following commands:

   .. code:: bash

      # Install the minimum requirements
      python -m pip install -e .

      # Install the minimum + tests requirements
      python -m pip install -e .[tests]

      # Install the minimum + doc requirements
      python -m pip install -e .[doc]

      # Install all requirements
      python -m pip install -e .[tests,doc]


Install in offline mode
^^^^^^^^^^^^^^^^^^^^^^^

If you lack an internet connection on your installation machine (or you do not have access to the
private Ansys PyPI packages repository), you should install PySherlock by downloading the wheelhouse
archive from the `Releases Page <https://github.com/ansys/pysherlock/releases>`_ for your
corresponding machine architecture.

Each wheelhouse archive contains all the Python wheels necessary to install PySherlock from scratch on Windows,
Linux, and MacOS from Python 3.10 to 3.12. You can install this on an isolated system with a fresh Python
installation or on a virtual environment.

For example, on Linux with Python 3.10, unzip the wheelhouse archive and install it with:

.. code:: bash

    unzip ansys-sherlock-core-v0.3.dev0-wheelhouse-Linux-3.10.zip wheelhouse
    pip install ansys-sherlock-core -f wheelhouse --no-index --upgrade --ignore-installed

If you're on Windows with Python 3.10, unzip to a wheelhouse directory and install using the preceding command.

Consider installing using a `virtual environment <https://docs.python.org/3/library/venv.html>`_.

Testing
-------

This project takes advantage of `tox <https://tox.wiki/>`_. This tool automates common
development tasks (similar to Makefile), but it is oriented towards Python
development.

Using ``tox``
^^^^^^^^^^^^^

While Makefile has rules, `tox`_ has environments. In fact, ``tox`` creates its
own virtual environment so that anything being tested is isolated from the project
to guarantee the project's integrity.

The following environments commands are provided:

- **tox -e style**: Checks for coding style quality.
- **tox -e py**: Checks for unit tests.
- **tox -e py-coverage**: Checks for unit testing and code coverage.
- **tox -e doc**: Checks for successfully building the documentation.

Raw testing
^^^^^^^^^^^

PySherlock also makes use of `PyTest <https://docs.pytest.org/en/stable/>`_,
which can be easily run by using this command to install the ``tests`` target:

.. code:: bash

   python -m pip install -e .[tests]


Once the dependencies are installed in your project, you can simply execute the
following command to run the PySherlock tests:

.. code:: bash

   pytest

Documentation
-------------

For building documentation, you can run the usual rules provided in the
`Sphinx <https://www.sphinx-doc.org/en/master/>`_ Makefile, such as:

.. code:: bash

    make -C doc/ html && your_browser_name doc/html/index.html

However, the recommended way of checking documentation integrity is to use
``tox``:

.. code:: bash

    tox -e doc && your_browser_name .tox/doc_out/index.html


Distributing
------------

If you would like to create either source or wheel files, start by installing
the building requirements and then executing the build module with these commands:

.. code:: bash

    python -m pip install -U pip
    python -m build
    python -m twine check dist/*
