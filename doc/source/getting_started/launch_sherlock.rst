.. _launch_sherlock:

===============
Launch Sherlock
===============

To launch Sherlock, use the ``launch_sherlock()`` method. This takes an optional ``port``
parameter and automatically searches for the latest local version of Sherlock, and
launches the Sherlock gRPC server on the port specified. Without a specified port, port 9090
is used by default. It also launches a Sherlock client connected to the same port and
returns a gRPC connection object ``Sherlock`` which can be used to invoke the APIs from their
respective services.

.. code::

    from ansys.sherlock.core import launcher
    sherlock = launcher.launch_sherlock()

To start the Sherlock gRPC server on a different port by using the ``port`` parameter.

.. code::

    from ansys.sherlock.core import launcher
    sherlock = launcher.launch_sherlock(port=11000)

This example uses the gRPC connection object to perform a health check on
the gRPC connection via the :func:`check<ansys.sherlock.core.common.Common.check>` method:

.. code::

    sherlock.common.check()