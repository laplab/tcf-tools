# *****************************************************************************
# * Copyright (c) 2011-2014 Wind River Systems, Inc. and others.
# * All rights reserved. This program and the accompanying materials
# * are made available under the terms of the Eclipse Public License 2.0
# * which accompanies this distribution, and is available at
# * https://www.eclipse.org/legal/epl-2.0/
# *
# * Contributors:
# *     Wind River Systems - initial API and implementation
# *****************************************************************************

"""Extension of Processes service.

.. |start| replace:: :meth:`~tcf.services.processes.ProcessesService.start`
.. |DoneStart| replace:: :class:`~tcf.services.processes.DoneStart`

It provides new |start| command that supports additional parameters.

Properties
----------
Process Context Properties
^^^^^^^^^^^^^^^^^^^^^^^^^^
+-----------------+--------+--------------------------------------------------+
| Name            | Type   | Description                                      |
+=================+========+==================================================+
| PROP_CAN_ATTACH | |bool| | **True** if process can be attached.             |
+-----------------+--------+--------------------------------------------------+
| PROP_IS_PROCESS | |bool| | **True** if context is a process (as opposed to  |
|                 |        | thread or some specific processes).              |
+-----------------+--------+--------------------------------------------------+

Processes Service Capablities
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
+----------------------+--------+---------------------------------------------+
| Name                 | Type   | Description                                 |
+======================+========+=============================================+
| PROP_PROC_CREATION   | |bool| | **True** if process creation is supported.  |
+----------------------+--------+---------------------------------------------+
| PROP_THREAD_CREATION | |bool| | **True** if thread creation is supported.   |
+----------------------+--------+---------------------------------------------+
| PROP_MAX_THREAD_ARGS | |int|  | Maximum number of argument for thread       |
|                      |        | creation.                                   |
+----------------------+--------+---------------------------------------------+
| PROP_START_PARAMS    | |list| | The list of parameters supported by |start| |
|                      |        | command.                                    |
+----------------------+--------+---------------------------------------------+

Process Start Properties
^^^^^^^^^^^^^^^^^^^^^^^^
+-----------------------+--------------+--------------------------------------+
| Name                  | Type         | Description                          |
+=======================+==============+======================================+
| START_ATTACH          | |bool|       | Attach the debugger to the process.  |
+-----------------------+--------------+--------------------------------------+
| START_ATTACH_CHILDREN | |bool|       | Auto-attach process children.        |
+-----------------------+--------------+--------------------------------------+
| START_STOP_AT_ENTRY   | |bool|       | Stop at process entry.               |
+-----------------------+--------------+--------------------------------------+
| START_STOP_AT_MAIN    | |bool|       | Stop at main().                      |
+-----------------------+--------------+--------------------------------------+
| START_USE_TERMINAL    | |bool|       | Use pseudo-terminal for the process  |
|                       |              | standard I/O.                        |
+-----------------------+--------------+--------------------------------------+
| START_MEM_SPACE_ID    | |basestring| | Process memory space in which to     |
|                       |              | start thead in.                      |
+-----------------------+--------------+--------------------------------------+
| START_SYMBOL          | |basestring| | Entry point symbol to start thread.  |
+-----------------------+--------------+--------------------------------------+
| START_ADDRESS         | |long|       | Entry point address to start thread. |
+-----------------------+--------------+--------------------------------------+
| START_NAME            | |basestring| | Name of the thread to start.         |
+-----------------------+--------------+--------------------------------------+
| START_PRIORITY        | |int|        | The thread priority.                 |
+-----------------------+--------------+--------------------------------------+
| START_STACK_SIZE      | |long|       | The thread stack size.               |
+-----------------------+--------------+--------------------------------------+
| START_PROC_OPTIONS    | |int|        | The process options flag value.      |
+-----------------------+--------------+--------------------------------------+
| START_THREAD_OPTIONS  | |int|        | The thread options flag value.       |
+-----------------------+--------------+--------------------------------------+

Service Methods
---------------
.. autodata:: NAME
.. autoclass:: ProcessesV1Service

start
^^^^^
.. automethod:: ProcessesV1Service.start

getCapabilities
^^^^^^^^^^^^^^^
.. automethod:: ProcessesV1Service.getCapabilities
"""

from . import processes

NAME = "ProcessesV1"
"""Processes version 1 service name."""

# Process start parameters

START_ATTACH = "Attach"
START_ATTACH_CHILDREN = "AttachChildren"
START_STOP_AT_ENTRY = "StopAtEntry"
START_STOP_AT_MAIN = "StopAtMain"
START_USE_TERMINAL = "UseTerminal"
START_MEM_SPACE_ID = "MemSpaceID"
START_SYMBOL = "StartSymbol"
START_ADDRESS = "StartAddress"
START_NAME = "Name"
START_PRIORITY = "Priority"
START_STACK_SIZE = "StackSize"
START_PROC_OPTIONS = "ProcessOptions"
START_THREAD_OPTIONS = "ThreadOptions"

# Context properties.

PROP_CAN_ATTACH = "CanAttach"
PROP_IS_PROCESS = "IsProcess"

# Capability properties.

PROP_PROC_CREATION = "ProcessCreation"
PROP_THREAD_CREATION = "ThreadCreation"
PROP_MAX_THREAD_ARGS = "MaxThreadArgs"
PROP_START_PARAMS = "StartParams"


class DoneGetCapabilities (object):
    """A class to implement TCF's ProcessesV1 |getCapabilities| end.

    When TCF's ProcessesV1 service |getCapabilities| method is called, this
    class can be specified as the *done* parameter.
    """

    def doneGetCapabilities(self, token, error, capabilityData):
        """Implementation method for TCF's ProcessesV1 service
        doneGetCapabilities().

        :param token: TCF request token corresponding to the command.
        :param error: Potential error returned by the TCF agent.
        :param capabilityData: Capability data properties.
        """
        raise NotImplementedError("Abstract method")


class ProcessesV1Service(processes.ProcessesService):
    """TCF processes Version 1 service interface."""

    def getName(self):
        """Get this service name.

        :returns: This service name, which is the value of :const:`NAME`
        """
        return NAME

    def start(self, directory, filePath, command_line, environment, params,
              done):
        """Start a new process on remote machine.

         .. note:: The service does **NOT** add image file name as first
                   argument for the process. If a client wants first parameter
                   to be the file name, it should add it itself.

        :param directory: Initial value of working directory for the process.
        :type directory: |basestring|
        :param filePath: Process image file.
        :type filePath: |basestring|
        :param command_line: Command line arguments for the process.
        :type command_line: |list| of |basestring|
        :param environment: A |dict| of environment variables for the process,
                            if **None** then default set of environment
                            variables will be used.
        :type environment: |dict| or **None**
        :param params: Additional process start parameters as |dict|, see
                       `Process Start Properties`_ for supported keys.
        :type params: |dict|
        :param done: Call back interface called when operation is completed.
        :type done: |DoneStart|
        """
        raise NotImplementedError("Abstract method")

    def getCapabilities(self, done):
        """Retrieve the capabilities for the service.

        :param done: Callback interface called when operation is completed.

        :returns: Pending command handle.
        """
        raise NotImplementedError("Abstract method")
