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
Use the `https://github.com/pyansys/pysherlock/issues`_ page to
submit questions, report bugs, and request new features.


Adhere to code style
--------------------
PySherlock is compliant with the `PyAnsys code style
<https://dev.docs.pyansys.com/coding-style/index.html>`_. It uses the tool
`pre-commit <https://pre-commit.com/>`_ to check the code style. You can
install and activate this tool with:

.. code:: bash

   python -m pip install pre-commit
   pre-commit install

You can then use the ``style`` rule defined in ``Makefile`` with:

.. code:: bash

   make style

Or, you can directly execute `pre-commit <https://pre-commit.com/>`_ with:

.. code:: bash

    pre-commit run --all-files --show-diff-on-failure
