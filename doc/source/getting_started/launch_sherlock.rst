.. _launch_and_connect:

===============
Launch Sherlock
===============

To launch Sherlock, use the
:func:`launch_and_connect()<ansys.sherlock.core.launcher.launch_and_connect>`
method. This method automatically searches for the latest version of Sherlock installed locally if
the version isn't specified in the parameters. It then launches the Sherlock gRPC server on
the port specified. If a port is not specified, port ``9090`` is used.

This method also launches a Sherlock client connected to the same port and
returns a ``sherlock`` gRPC connection object that can be used to invoke the APIs from their
respective services.

This code starts the Sherlock gRPC server on the default port:

.. code::

    from ansys.sherlock.core import launcher
    sherlock, install_dir = launcher.launch_and_connect()

This code uses the optional ``port`` parameter to start the Sherlock gRPC server on port
``11000``:

.. code::

    from ansys.sherlock.core import launcher
    sherlock = launcher.launch_and_connect(port=11000)

You can use the :func:`Common.check()<ansys.sherlock.core.common.Common.check>`
method to perform a health check on the ``sherlock`` gRPC connection object:

.. code::

    sherlock.common.check()
