.. _launch_sherlock:

===============
Launch Sherlock
===============

To launch Sherlock, use the :func:`launch_sherlock()<ansys.sherlock.core.launcher.launch_sherlock>`
method. This method takes an optional ``port`` parameter and automatically searches for the
latest version of Sherlock installed locally. It then launches the Sherlock gRPC server on
the port specified. If a port is not specified, port ``9090`` is used.

This method also launches a Sherlock client connected to the same port and
returns a ``sherlock`` gRPC connection object that can be used to invoke the APIs from their
respective services.

This code starts the Sherlock gRPC server on the default port:

.. code::

    from ansys.sherlock.core import launcher
    sherlock = launcher.launch_sherlock()

This code uses the optional ``port`` parameter to start the Sherlock gRPC server on port
``11000``:

.. code::

    from ansys.sherlock.core import launcher
    sherlock = launcher.launch_sherlock(port=11000)

You can use the :func:`Common.check()<ansys.sherlock.core.common.Common.check>`
method to perform a health check on the ``sherlock`` gRPC connection object:

.. code::

    sherlock.common.check()
