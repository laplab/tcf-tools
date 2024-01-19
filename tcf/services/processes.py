# *****************************************************************************
# * Copyright (c) 2011, 2013-2014 Wind River Systems, Inc. and others.
# * All rights reserved. This program and the accompanying materials
# * are made available under the terms of the Eclipse Public License 2.0
# * which accompanies this distribution, and is available at
# * https://www.eclipse.org/legal/epl-2.0/
# *
# * Contributors:
# *     Wind River Systems - initial API and implementation
# *****************************************************************************

"""TCF Processes service interface.

.. |attach| replace:: :meth:`~ProcessContext.attach`
.. |detach| replace:: :meth:`~ProcessContext.detach`
.. |getChildren| replace:: :meth:`~ProcessesService.getChildren`
.. |getContext| replace:: :meth:`~ProcessesService.getContext`
.. |getEnvironment| replace:: :meth:`~ProcessesService.getEnvironment`
.. |getSignalList| replace:: :meth:`~ProcessesService.getSignalList`
.. |getSignalMask| replace:: :meth:`~ProcessesService.getSignalMask`
.. |setSignalMask| replace:: :meth:`~ProcessesService.setSignalMask`
.. |signal| replace:: :meth:`~ProcessesService.signal`
.. |start| replace:: :meth:`~ProcessesService.start`
.. |terminate| replace:: :meth:`~ProcessContext.terminate`
.. |Breakpoint| replace:: :class:`~tcf.services.breakpoints.BreakpointsService`
.. |DoneCommand| replace:: :class:`DoneCommand`
.. |DoneGetContext| replace:: :class:`DoneGetContext`
.. |DoneGetChildren| replace:: :class:`DoneGetChildren`
.. |DoneGetSignalList| replace:: :class:`DoneGetSignalList`
.. |DoneGetSignalMask| replace:: :class:`DoneGetSignalMask`
.. |DoneStart| replace:: :class:`DoneStart`
.. |Memory| replace:: :class:`~tcf.services.memory.MemoryService`
.. |ProcessContext| replace:: :class:`ProcessContext`
.. |ProcessesListener| replace:: :class:`ProcessesListener`
.. |RunControl| replace:: :class:`~tcf.services.runcontrol.RunControlService`


Processes service provides access to the target OS's process information,
allows to start and terminate a process, and allows to attach and detach a
process for debugging.

Debug services, like |Memory| and |RunControl|, require a process to be
attached before they can access it.

If a process is started by this service, its standard input/output streams are
available for client to read/write using Streams service. Stream type of such
streams is set to ``Processes``.

Properties
----------
Process Context Properties
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. seealso:: |ProcessContext|

+--------------------+--------------+-----------------------------------------+
| Name               | Type         | Description                             |
+====================+==============+=========================================+
| PROP_ATTACHED      | |bool|       | Is the context attached ?               |
+--------------------+--------------+-----------------------------------------+
| PROP_CAN_TERMINATE | |bool|       | Can terminate the context ?             |
+--------------------+--------------+-----------------------------------------+
| PROP_ID            | |basestring| | The TCF context ID.                     |
+--------------------+--------------+-----------------------------------------+
| PROP_NAME          | |basestring| | Process name. Client UI can show this   |
|                    |              | name to a user.                         |
+--------------------+--------------+-----------------------------------------+
| PROP_PARENT_ID     | |basestring| | The TCF parent context ID.              |
+--------------------+--------------+-----------------------------------------+
| PROP_STDERR_ID     | |basestring| | Process standard error stream ID.       |
+--------------------+--------------+-----------------------------------------+
| PROP_STDIN_ID      | |basestring| | Process standard input stream ID.       |
+--------------------+--------------+-----------------------------------------+
| PROP_STDOUT_ID     | |basestring| | Process standard output stream ID.      |
+--------------------+--------------+-----------------------------------------+

Signals Properties
^^^^^^^^^^^^^^^^^^

.. seealso:: |getSignalList|

+-----------------+--------------+--------------------------------------------+
| Name            | Type         | Description                                |
+=================+==============+============================================+
| SIG_CODE        | |int|        | Signal code, as defined by OS.             |
+-----------------+--------------+--------------------------------------------+
| SIG_DESCRIPTION | |basestring| | Human readable description of the signal.  |
+-----------------+--------------+--------------------------------------------+
| SIG_INDEX       | |int|        | Bit position in the signal mask.           |
+-----------------+--------------+--------------------------------------------+
| SIG_NAME        | |basestring| | Signal name, for example ``SIGHUP``.       |
+-----------------+--------------+--------------------------------------------+

Service Methods
---------------
.. autodata:: NAME
.. autoclass:: ProcessesService

addListener
^^^^^^^^^^^
.. automethod:: ProcessesService.addListener

getChildren
^^^^^^^^^^^
.. automethod:: ProcessesService.getChildren

getContext
^^^^^^^^^^
.. automethod:: ProcessesService.getContext

getEnvironment
^^^^^^^^^^^^^^
.. automethod:: ProcessesService.getEnvironment

getName
^^^^^^^
.. automethod:: ProcessesService.getName

getSignalList
^^^^^^^^^^^^^
.. automethod:: ProcessesService.getSignalList

getSignalMask
^^^^^^^^^^^^^
.. automethod:: ProcessesService.getSignalMask

removeListener
^^^^^^^^^^^^^^
.. automethod:: ProcessesService.removeListener

setSignalMask
^^^^^^^^^^^^^
.. automethod:: ProcessesService.setSignalMask

signal
^^^^^^
.. automethod:: ProcessesService.signal

start
^^^^^
.. automethod:: ProcessesService.start

Callback Classes
----------------
DoneCommand
^^^^^^^^^^^
.. autoclass:: DoneCommand
    :members:

DoneGetChildren
^^^^^^^^^^^^^^^
.. autoclass:: DoneGetChildren
    :members:

DoneGetContext
^^^^^^^^^^^^^^
.. autoclass:: DoneGetContext
    :members:

DoneGetEnvironment
^^^^^^^^^^^^^^^^^^
.. autoclass:: DoneGetEnvironment
    :members:

DoneGetSignalList
^^^^^^^^^^^^^^^^^
.. autoclass:: DoneGetSignalList
    :members:

DoneGetSignalMask
^^^^^^^^^^^^^^^^^
.. autoclass:: DoneGetSignalMask
    :members:

DoneStart
^^^^^^^^^
.. autoclass:: DoneStart
    :members:

Listener
--------
.. autoclass:: ProcessesListener
    :members:
    :show-inheritance:

Helper Classes
--------------
ProcessContext
^^^^^^^^^^^^^^
.. autoclass:: ProcessContext
    :members:
"""

from .. import services

NAME = "Processes"
"""Processes service name."""

# Context property names.

PROP_ID = "ID"
PROP_PARENT_ID = "ParentID"
PROP_ATTACHED = "Attached"
PROP_CAN_TERMINATE = "CanTerminate"
PROP_NAME = "Name"
PROP_STDIN_ID = "StdInID"
PROP_STDOUT_ID = "StdOutID"
PROP_STDERR_ID = "StdErrID"

# Signal property names used by "getSignalList" command.

SIG_INDEX = "Index"
SIG_NAME = "Name"
SIG_CODE = "Code"
SIG_DESCRIPTION = "Description"


class ProcessesService(services.Service):
    """TCF processes service interface."""

    def getName(self):
        """Get this service name.

        :returns: A |basestring| representing this service name, which is the
                  value of :const:`NAME`
        """
        return NAME

    def getContext(self, contextID, done):
        """Retrieve context info for given context ID.

        A context corresponds to an execution thread, process, address space,
        etc.

        Context IDs are valid across TCF services, so it is allowed to issue
        |getContext| command with a context that was obtained, for example,
        from |Memory| service.

        However, |getContext| is supposed to return only process specific data.
        If the ID is not a process ID, |getContext| may not return any useful
        information.

        :param contextID: The TCF ID of the context to get properties for.
        :type contextID: |basestring|
        :param done: Call back interface called when operation is completed.
        :type done: |DoneGetContext|

        :returns: Pending command handle, can be used to cancel the command.
        """
        raise NotImplementedError("Abstract method")

    def getChildren(self, parent_context_id, attached_only, done):
        """Retrieve children of given context.

        :param parent_context_id: parent context ID. Can be **None** to
                                  retrieve top level of the hierarchy, or one
                                  of context IDs retrieved by previous
                                  |getContext| or |getChildren| commands.
        :type parent_context_id: |basestring| or **None**
        :param attached_only: If **True** return only attached process IDs.
        :type attached_only: |bool|
        :param done: Call back interface called when operation is completed.
        :type done: |DoneGetChildren|

        :returns: Pending command handle, can be used to cancel the command.
        """
        raise NotImplementedError("Abstract method")

    def getSignalList(self, context_id, done):
        """Get list of signals that can be send to the process.

        :param context_id: Process context ID or ***None***.
        :type context_id: |basestring| or **None**
        :param done: Call back interface called when operation is completed.
        :type done: |DoneGetSignalList|

        :returns: Pending command handle, can be used to cancel the command.

        .. seealso:: `Signals Properties`_
        """
        raise NotImplementedError("Abstract method")

    def getSignalMask(self, context_id, done):
        """Get process or thread signal mask.

        Bits in the mask control how signals should be handled by debug agent.
        When new context is created it inherits the mask from its parent.

        If context is not attached the command will return an error.

        :param context_id: TCF ID of the context ot get signal mask for.
        :type context_id: |basestring|
        :param done: Call back interface called when operation is completed
        :type done: |DoneGetSignalMask|

        :returns: Pending command handle, can be used to cancel the command.
        """
        raise NotImplementedError("Abstract method")

    def setSignalMask(self, context_id, dont_stop, dont_pass, done):
        """Set process or thread signal mask.

        Bits in the mask control how signals should be handled by debug agent.
        If context is not attached the command will return an error.

        :param dont_stop: Bit-set of signals that should not suspend execution
                          of the context. By default, debugger suspends a
                          context before it receives a signal.
        :type dont_stop: |int|
        :param dont_pass: Bit-set of signals that should not be delivered to
                          the context.
        :type dont_pass: |int|
        :param done: Call back interface called when operation is completed.
        :type done: |DoneCommand|

        :returns: Pending command handle, can be used to cancel the command.
        """
        raise NotImplementedError("Abstract method")

    def signal(self, context_id, signal, done):
        """Send a signal to a process or thread.

        :param context_id: TCF ID of the context to send a signal to.
        :type context_id: |basestring|
        :param signal: Signal code.
        :type signal: |int|
        :param done: Call back interface called when operation is completed.
        :type done: |DoneCommand|

        :returns: Pending command handle, can be used to cancel the command.
        """
        raise NotImplementedError("Abstract method")

    def getEnvironment(self, done):
        """Get default set of environment variables used to start a new
        process.

        :param done: call back interface called when operation is completed.
        :type done: :class:`DoneGetEnvironment`

        :returns: pending command handle, can be used to cancel the command.
        """
        raise NotImplementedError("Abstract method")

    def start(self, directory, fileName, command_line, environment, attach,
              done):
        """Start a new process on remote machine.

        :param directory: Initial value of working directory for the process.
        :type directory: |basestring|
        :param fileName: Process image file.
        :type fileName: |basestring|
        :param command_line: Command line arguments for the process.
                             :note: the service does NOT add image file name as
                             first argument for the process. If a client wants
                             first parameter to be the file name, it should add
                             it itself.
        :type command_line: |basestring|
        :param environment: Map of environment variables for the process, if
                            **None** then default set of environment variables
                            will be used.
        :type environment: |dict| or **None**
        :param attach: If **True** debugger should be attached to the process.
        :type attach: |bool|
        :param done: Call back interface called when operation is completed
        :type done: |DoneStart|

        :returns: Pending command handle, can be used to cancel the command.
        """
        raise NotImplementedError("Abstract method")

    def addListener(self, listener):
        """Add processes service event listener.

        :param listener: Processes event listener implementation to add to
                         service.
        :type listener: |ProcessesListener|
        """
        raise NotImplementedError("Abstract method")

    def removeListener(self, listener):
        """Remove processes service event listener.

        :param listener: Processes event listener implementation to remove from
                         service.
        :type listener: |ProcessesListener|
        """
        raise NotImplementedError("Abstract method")


class ProcessContext(object):
    """A context corresponds to an execution thread, process, address space,
    etc.

    A context can belong to a parent context. Contexts hierarchy can be simple
    plain list or it can form a tree. It is up to target agent developers to
    choose layout that is most descriptive for a given target. Context IDs are
    valid across all services. In other words, all services access same
    hierarchy of contexts, with same IDs, however, each service accesses its
    own subset of context's attributes and functionality, which is relevant to
    that service.

    :param props: A |dict| of properties to initialise this Process context
                  with. See `Process Context Properties`_
    :type props: |dict|
    """
    def __init__(self, props):
        self._props = props or {}

    def __str__(self):
        return "[Processes Context %s]" % self._props

    def getProperties(self):
        """Get context properties.

        See `Process Context Properties`_ definitions for property names.

        Context properties are read only, clients should not try to modify
        them.

        :returns: A |dict| of context properties.
        """
        return self._props

    def getID(self):
        """Retrieve context ID.

        :returns: A |basestring| representing this Process context ID.
        """
        return self._props.get(PROP_ID)

    def getParentID(self):
        """Retrieve parent context ID.

        :returns: A |basestring| representing this Process parent context ID.
        """
        return self._props.get(PROP_PARENT_ID)

    def getName(self):
        """Retrieve human readable context name.

        :returns: A |basestring| representing this Process context name or
                  **None**.
        """
        return self._props.get(PROP_NAME)

    def isAttached(self):
        """Check if context is attached.

        Services like |RunControl|, |Memory|, |Breakpoint| work only with
        attached processes.

        :returns: A |bool| stating if this process context is attached or not.
        """
        return bool(self._props.get(PROP_ATTACHED))

    def canTerminate(self):
        """Check if this process can be terminated.

        :returns: A |bool| stating if this process context is terminated or
                  not.
        """
        return self._props.get(PROP_CAN_TERMINATE)

    def attach(self, done):
        """Attach debugger to a process.

        Services like |RunControl|, |Memory|, |Breakpoint| work only with
        attached processes.

        :param done: Call back interface called when operation is completed.
        :type done: |DoneCommand|

        :returns: Pending command handle, can be used to cancel the command.
        """
        raise NotImplementedError("Abstract method")

    def detach(self, done):
        """Detach debugger from a process.

        Process execution will continue without debugger supervision.

        :param done: Call back interface called when operation is completed.
        :type done: |DoneCommand|

        :returns: Pending command handle, can be used to cancel the command.
        """
        raise NotImplementedError("Abstract method")

    def terminate(self, done):
        """Terminate a process.

        :param done: Call back interface called when operation is completed.
        :type done: |DoneCommand|

        :returns: Pending command handle, can be used to cancel the command.
        """
        raise NotImplementedError("Abstract method")


class DoneCommand(object):
    """Client callback interface for simple commands like |attach|, |detach|,
       |terminate|, |setSignalMask| and |signal|.
    """
    def doneCommand(self, token, error):
        """Called when command is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        """
        pass


class DoneGetContext(object):
    """Client callback interface for |getContext|."""
    def doneGetContext(self, token, error, context):
        """Called when context data retrieval is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param context: Retrieved context data.
        :type context: |ProcessContext|
        """
        pass


class DoneGetChildren(object):
    """Client callback interface for |getChildren|."""
    def doneGetChildren(self, token, error, context_ids):
        """Called when context list retrieval is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param context_ids: List of available context IDs.
        :type context_ids: |tuple| or |list|
        """
        pass


class DoneGetSignalList(object):
    """Call-back interface to be called when |getSignalList| command is
    complete.
    """
    def doneGetSignalList(self, token, error, signalList):
        """Called when signal list retrieval is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param signalList: The list of signals supported for this process.
        :type signalList: |tuple| or |list|
        """
        pass


class DoneGetSignalMask(object):
    """Client callback interface for |getSignalMask|."""
    def doneGetSignalMask(self, token, error, dont_stop, dont_pass, pending):
        """Called when context signal mask retrieval is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param dont_stop: Bit-set of signals that should suspend execution of
                          the context.
        :type dont_stop: |int|
        :param dont_pass: Bit-set of signals that should not be delivered to
                          the context.
        :type dont_pass: |int|
        :param pending: Bit-set of signals that are generated but not
                        delivered yet.
        :type pending: |int|

        .. note:: *pending* is meaningful only if the context is suspended.
        """
        pass


class DoneGetEnvironment(object):
    """Client callback interface for |getEnvironment|."""
    def doneGetEnvironment(self, token, error, environment):
        """Called when environment retrieval is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param environment: A |dict| of context environment variables.
        :type environment: |dict|
        """
        pass


class DoneStart(object):
    """Client callback interface for |start|."""
    def doneStart(self, token, error, process):
        """Called when process start is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param process: A |ProcessContext| object representing the started
                        process.
        :type process: |ProcessContext|
        """
        pass


class ProcessesListener(object):
    """Process event listener is notified when a process exits.

    Event are reported only for processes that were started by |start| command.
    """

    def exited(self, process_id, exit_code):
        """Called when a process exits.

        :param process_id: TCF process context ID.
        :type process_id: |basestring|
        :param exit_code: * If positive, the process exit code.
                          * If negative, process was terminated by a signal,
                            the signal code  **-** *exit_code*.
        """
        pass
