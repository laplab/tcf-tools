# *****************************************************************************
# * Copyright (c) 2011, 2013-2014, 2016 Wind River Systems, Inc. and others.
# * All rights reserved. This program and the accompanying materials
# * are made available under the terms of the Eclipse Public License 2.0
# * which accompanies this distribution, and is available at
# * https://www.eclipse.org/legal/epl-2.0/
# *
# * Contributors:
# *     Wind River Systems - initial API and implementation
# *****************************************************************************

"""This is an optional service that can be implemented by a peer.

If implemented, the service can be used for monitoring system activity and
utilization.

It provides list of running processes, different process attributes like
command line, environment, etc., and some resource utilization data.

The service can be used by a client to provide functionality similar to Unix
**top** utility or Windows **Task Manager**.

.. |getChildren| replace:: :meth:`~SysMonitorService.getChildren`
.. |getCommandLine| replace:: :meth:`~SysMonitorService.getCommandLine`
.. |getContext| replace:: :meth:`~SysMonitorService.getContext`
.. |getEnvironment| replace:: :meth:`~SysMonitorService.getEnvironment`
.. |getProperties| replace:: :meth:`SysMonitorContext.getProperties`
.. |DoneGetChildren| replace:: :class:`DoneGetChildren`
.. |DoneGetCommandLine| replace:: :class:`DoneGetCommandLine`
.. |DoneGetContext| replace:: :class:`DoneGetContext`
.. |DoneGetEnvironment| replace:: :class:`DoneGetEnvironment`
.. |SysMonitorContext| replace:: :class:`SysMonitorContext`

Properties
----------
System Monitor Context Properties
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. seealso:: |SysMonitorContext|, |getProperties|

+------------------+--------------+-------------------------------------------+
| Name             | Type         | Description                               |
+==================+==============+===========================================+
| PROP_CMAJFLT     | |int|        | The number of major faults that the       |
|                  |              | process's  waited-for  children have made.|
+------------------+--------------+-------------------------------------------+
| PROP_CMINFLT     | |int|        | The number of minor faults that the       |
|                  |              | process's waited-for  children have made. |
+------------------+--------------+-------------------------------------------+
| PROP_CNSWAP      | |int|        | Cumulative NSwap for child processes.     |
+------------------+--------------+-------------------------------------------+
| PROP_CODEEND     | |int|        | The address below which program text can  |
|                  |              | run.                                      |
+------------------+--------------+-------------------------------------------+
| PROP_CODESTART   | |int|        | The address above which program text can  |
|                  |              | run.                                      |
+------------------+--------------+-------------------------------------------+
| PROP_CSTIME      | |int|        | The number of jiffies that this process's |
|                  |              | waited-for children have been scheduled in|
|                  |              | user mode.                                |
+------------------+--------------+-------------------------------------------+
| PROP_CUTIME      | |int|        | The number of jiffies that this process's |
|                  |              | waited-for children have been scheduled in|
|                  |              | user mode.                                |
+------------------+--------------+-------------------------------------------+
| PROP_CWD         | |basestring| | Current working directory of the process. |
+------------------+--------------+-------------------------------------------+
| PROP_EXITSIGNAL  | |int|        | Signal to be sent to parent when this     |
|                  |              | process exits.                            |
+------------------+--------------+-------------------------------------------+
| PROP_FILE        | |basestring| | Executable file of the process.           |
+------------------+--------------+-------------------------------------------+
| PROP_FLAGS       | |int|        | The kernel flags word of the process.     |
|                  |              | Details depend on the kernel.             |
+------------------+--------------+-------------------------------------------+
| PROP_GROUPNAME   | |basestring| | Group name of the process owner.          |
+------------------+--------------+-------------------------------------------+
| PROP_ID          | |basestring| | The TCF context ID.                       |
+------------------+--------------+-------------------------------------------+
| PROP_ITREALVALUE | |int|        | The time in milliseconds before the next  |
|                  |              | ``SIGALRM`` is sent  to  the  process due |
|                  |              | to an interval timer.                     |
+------------------+--------------+-------------------------------------------+
| PROP_MAJFLT      | |int|        | The number of major faults the process has|
|                  |              | made which have required loading a memory |
|                  |              | page from disk.                           |
+------------------+--------------+-------------------------------------------+
| PROP_MINFLT      | |int|        | The number of minor faults the process has|
|                  |              | made which have not required loading a    |
|                  |              | memory page from disk.                    |
+------------------+--------------+-------------------------------------------+
| PROP_NICE        | |int|        | The nice value.                           |
+------------------+--------------+-------------------------------------------+
| PROP_NSWAP       | |int|        | Number of pages swapped.                  |
+------------------+--------------+-------------------------------------------+
| PROP_PARENTID    | |basestring| | The TCF parent context ID.                |
+------------------+--------------+-------------------------------------------+
| PROP_PGRP        | |int|        | The process group ID of the process.      |
+------------------+--------------+-------------------------------------------+
| PROP_PID         | |int|        | System process ID.                        |
+------------------+--------------+-------------------------------------------+
| PROP_POLICY      | |basestring| | Scheduling policy.                        |
+------------------+--------------+-------------------------------------------+
| PROP_PPID        | |int|        | System ID of the parent process.          |
+------------------+--------------+-------------------------------------------+
| PROP_PRIORITY    | |int|        | The standard nice value.                  |
+------------------+--------------+-------------------------------------------+
| PROP_PROCESSOR   | |int|        | CPU number last executed on.              |
+------------------+--------------+-------------------------------------------+
| PROP_PSIZE       | |int|        | Memory pages size in bytes.               |
+------------------+--------------+-------------------------------------------+
| PROP_RLIMIT      | |int|        | Current limit in bytes on the rss of the  |
|                  |              | process.                                  |
+------------------+--------------+-------------------------------------------+
| PROP_ROOT        | |basestring| | The process's root directory (as set by   |
|                  |              | **chroot**).                              |
+------------------+--------------+-------------------------------------------+
| PROP_RSS         | |int|        | Resident Set Size: number of pages the    |
|                  |              | process has in real memory, minus used for|
|                  |              | administrative purposes. This is just the |
|                  |              | pages which count towards text, data, or  |
|                  |              | stack space. This does not include pages  |
|                  |              | which have not been demand-loaded in, or  |
|                  |              | which are swapped out.                    |
+------------------+--------------+-------------------------------------------+
| PROP_RTPRIORITY  | |int|        | Real-time scheduling priority.            |
+------------------+--------------+-------------------------------------------+
| PROP_SESSION     | |int|        | The session ID of the process.            |
+------------------+--------------+-------------------------------------------+
| PROP_SIGBLOCK    | |int|        | The bitmap of blocked signals.            |
+------------------+--------------+-------------------------------------------+
| PROP_SIGCATCH    | |int|        | The bitmap of caught signals.             |
+------------------+--------------+-------------------------------------------+
| PROP_SIGIGNORE   | |int|        | The bitmap of ignored signals.            |
+------------------+--------------+-------------------------------------------+
| PROP_SIGNALS     | |int|        | The bitmap of pending signals.            |
+------------------+--------------+-------------------------------------------+
| PROP_STACKSTART  | |int|        | The address of the start of the stack.    |
+------------------+--------------+-------------------------------------------+
| PROP_STARTTIME   | |int|        | The time in milliseconds the process      |
|                  |              | started after system boot.                |
+------------------+--------------+-------------------------------------------+
| PROP_STATE       | |basestring| | One character from the string ``RSDZTW``  |
|                  |              | where :                                   |
|                  |              |                                           |
|                  |              |     - **R** is running.                   |
|                  |              |     - **S** is sleeping in an             |
|                  |              |       interruptible wait.                 |
|                  |              |     - **D** is waiting in uninterruptible |
|                  |              |       disk sleep.                         |
|                  |              |     - **Z** is zombie.                    |
|                  |              |     - **T** is traced or stopped (on a    |
|                  |              |       signal).                            |
|                  |              |     - **W** is paging.                    |
+------------------+--------------+-------------------------------------------+
| PROP_STIME       | |int|        | The number of milliseconds that this      |
|                  |              | process has been scheduled in kernel mode.|
+------------------+--------------+-------------------------------------------+
| PROP_TGID        | |int|        | The process group ID of the process which |
|                  |              | currently owns the tty that the process is|
|                  |              | connected to.                             |
+------------------+--------------+-------------------------------------------+
| PROP_TRACERPID   | |int|        | ID of a process that has attached this    |
|                  |              | process for tracing or debugging.         |
+------------------+--------------+-------------------------------------------+
| PROP_TTY         | |int|        | The tty the process uses.                 |
+------------------+--------------+-------------------------------------------+
| PROP_UGID        | |int|        | Group ID of the process owner.            |
+------------------+--------------+-------------------------------------------+
| PROP_UID         | |int|        | User ID of the process owner.             |
+------------------+--------------+-------------------------------------------+
| PROP_USERNAME    | |basestring| | User name of the process owner.           |
+------------------+--------------+-------------------------------------------+
| PROP_UTIME       | |int|        | The number of milliseconds that this      |
|                  |              | process has been scheduled in user mode.  |
+------------------+--------------+-------------------------------------------+
| PROP_VSIZE       | |int|        | Virtual memory size in bytes.             |
+------------------+--------------+-------------------------------------------+
| PROP_WCHAN       | |int|        | This is the *channel* in which the process|
|                  |              | is waiting. It is the address of a system |
|                  |              | call, and can be looked up in a name list |
|                  |              | if you need a textual name.               |
+------------------+--------------+-------------------------------------------+

Service Methods
---------------
.. autodata:: NAME
.. autoclass:: SysMonitorService

getChildren
^^^^^^^^^^^
.. automethod:: SysMonitorService.getChildren

getCommandLine
^^^^^^^^^^^^^^
.. automethod:: SysMonitorService.getCommandLine

getContext
^^^^^^^^^^
.. automethod:: SysMonitorService.getContext

getEnvironment
^^^^^^^^^^^^^^
.. automethod:: SysMonitorService.getEnvironment

getName
^^^^^^^
.. automethod:: SysMonitorService.getName

Callback Classes
----------------
DoneGetChildren
^^^^^^^^^^^^^^^
.. autoclass:: DoneGetChildren
    :members:

DoneGetCommandLine
^^^^^^^^^^^^^^^^^^
.. autoclass:: DoneGetCommandLine
    :members:

DoneGetContext
^^^^^^^^^^^^^^
.. autoclass:: DoneGetContext
    :members:

DoneGetEnvironment
^^^^^^^^^^^^^^^^^^
.. autoclass:: DoneGetEnvironment
    :members:

Helper Classes
--------------
SysMonitorContext
^^^^^^^^^^^^^^^^^
.. autoclass:: SysMonitorContext
    :members:
"""

from .. import services

NAME = "SysMonitor"
"""SysMonitor service name."""

# Context property names.
PROP_ID = "ID"
PROP_PARENTID = "ParentID"
PROP_SYSTEMID = "SystemID"
PROP_SYSTEMTYPE = "SystemType"
PROP_CWD = "CWD"
PROP_ROOT = "Root"
PROP_UID = "UID"
PROP_UGID = "UGID"
PROP_USERNAME = "UserName"
PROP_GROUPNAME = "GroupName"
PROP_PID = "PID"
PROP_FILE = "File"
PROP_STATE = "State"
PROP_PPID = "PPID"
PROP_PGRP = "PGRP"
PROP_SESSION = "Session"
PROP_TTY = "TTY"
PROP_TGID = "TGID"
PROP_TRACERPID = "TracerPID"
PROP_FLAGS = "Flags"
PROP_MINFLT = "MinFlt"
PROP_CMINFLT = "CMinFlt"
PROP_MAJFLT = "MajFlt"
PROP_CMAJFLT = "CMajFlt"
PROP_UTIME = "UTime"
PROP_STIME = "STime"
PROP_CUTIME = "CUTime"
PROP_CSTIME = "CSTime"
PROP_PRIORITY = "Priority"
PROP_NICE = "Nice"
PROP_ITREALVALUE = "ITRealValue"
PROP_STARTTIME = "StartTime"
PROP_VSIZE = "VSize"
PROP_PSIZE = "PSize"
PROP_RSS = "RSS"
PROP_RLIMIT = "RLimit"
PROP_CODESTART = "CodeStart"
PROP_CODEEND = "CodeEnd"
PROP_STACKSTART = "StackStart"
PROP_SIGNALS = "Signals"
PROP_SIGBLOCK = "SigBlock"
PROP_SIGIGNORE = "SigIgnore"
PROP_SIGCATCH = "SigCatch"
PROP_WCHAN = "WChan"
PROP_NSWAP = "NSwap"
PROP_CNSWAP = "CNSwap"
PROP_EXITSIGNAL = "ExitSignal"
PROP_PROCESSOR = "Processor"
PROP_RTPRIORITY = "RTPriority"
PROP_POLICY = "Policy"


class SysMonitorContext(object):
    """A context corresponds to an execution thread, process, address space,
    etc.

    A context can belong to a parent context. Contexts hierarchy can be simple
    plain list or it can form a tree. It is up to target agent developers to
    choose layout that is most descriptive for a given target. Context IDs are
    valid across all services. In other words, all services access same
    hierarchy of contexts, with same IDs, however, each service accesses its
    own subset of context's attributes and functionality, which is relevant to
    that service.

    :param props: The properties to initialise this system monitor context
                  with. See `System Monitor Context Properties`_.
    :type props: |dict|
    """
    def __init__(self, props):
        self._props = props or {}

    def __str__(self):
        return "[Sys Monitor Context %s]" % self._props

    def getID(self):
        """Get TCF context ID.

        :returns: A |basestring| representing this context TCF ID.
        """
        return self._props.get(PROP_ID, '')

    def getParentID(self):
        """Get parent context ID.

        :returns: A |basestring| representing this context parent TCF ID.
        """
        return self._props.get(PROP_PARENTID, '')

    def getSystemID(self):
        """Get target context ID.

        :returns: A |basestring| representing this target context ID or None
                  if unspecified.
        """
        return self._props.get(PROP_SYSTEMID, None)

    def getSystemType(self):
        """Get target context type.

        :returns: A |basestring| representing this target context type or None
                  if unspecified.
        """
        return self._props.get(PROP_SYSTEMTYPE, None)

    def getPGRP(self):
        """Get process group ID.

        :returns: An |int| representing this context process group ID, or
                  **-1** if it is not known.
        """
        return self._props.get(PROP_PGRP, -1)

    def getPID(self):
        """Get process ID.

        :returns: An |int| representing this context process ID, or
                  **-1** if it is not known.
        """
        return self._props.get(PROP_PID, -1)

    def getPPID(self):
        """Get process parent ID.

        :returns: An |int| representing this context parent process ID, or
                  **-1** if it is not known.
        """
        return self._props.get(PROP_PPID, -1)

    def getTGID(self):
        """Get process TTY group ID.

        :returns: An |int| representing this context process TTY group ID, or
                  **-1** if it is not known.
        """
        return self._props.get(PROP_TGID, -1)

    def getTracerPID(self):
        """Get tracer process ID.

        :returns: An |int| representing this context tracer process ID, or
                  **-1** if it is not known.
        """
        return self._props.get(PROP_TRACERPID, -1)

    def getUID(self):
        """Get process owner user ID.

        :returns: An |int| representing this context process owner user ID, or
                  **-1** if it is not known.
        """
        return self._props.get(PROP_UID, -1)

    def getUserName(self):
        """Get process owner user name.

        :returns: A |basestring| representing this context process owner user
                  name, or an empty string if it is not known.
        """
        return self._props.get(PROP_USERNAME, '')

    def getUGID(self):
        """Get process owner user group ID.

        :returns: An |int| representing this context process owner user group
                  ID, or **-1** if it is not known.
        """
        return self._props.get(PROP_UGID, -1)

    def getGroupName(self):
        """Get process owner user group name.

        :returns: A |basestring| representing this context process owner user
                  group name, or an empty string if it is not known.
        """
        return self._props.get(PROP_GROUPNAME, '')

    def getState(self):
        """Get process state.

        :returns: A |basestring| representing this context process state, or
                  an empty string if it is not known.
        """
        return self._props.get(PROP_STATE, '')

    def getVSize(self):
        """Get process virtual memory size in bytes.

        :returns: An |int| representing this context process virtual memory
                  size in bytes, or **-1** if it is not known.
        """
        return self._props.get(PROP_VSIZE, -1)

    def getPSize(self):
        """Get process virtual memory page size in bytes.

        :returns: An |int| representing this context process virtual memory
                  page size in bytes, or **-1** if it is not known.
        """
        return self._props.get(PROP_PSIZE, -1)

    def getRSS(self):
        """Get number of memory pages in process resident set.

        :returns: An |int| representing this context number of memory pages in
                  process resident set, or **-1** if it is not known.
        """
        return self._props.get(PROP_RSS, -1)

    def getFile(self):
        """Get context executable file.

        :returns: A |basestring| representing this context executable file, or
                  an empty string if it is not known.
        """
        return self._props.get(PROP_FILE, '')

    def getRoot(self):
        """Get context current file system root.

        :returns: A |basestring| representing this context current file system
                  root, or an empty string if it is not known.
        """
        return self._props.get(PROP_ROOT, '')

    def getCurrentWorkingDirectory(self):
        """Get context current working directory.

        :returns: A |basestring| representing this context current working
                  directory, or an empty string if it is not known.
        """
        return self._props.get(PROP_CWD, '')

    def getProperties(self):
        """Get all available context properties.

        :returns: A |dict| of properties definit this system monitor context.

        .. seealso:: `System Monitor Context Properties`_
        """
        return self._props


class SysMonitorService(services.Service):
    """System monitor service interface."""

    def getName(self):
        """Get this service name.

        :returns: A |basestring| representing this service name, which is the
                  value of :const:`NAME`
        """
        return NAME

    def getContext(self, contextID, done):
        """Retrieve context info for given context ID.

        :param contextID: TCF context ID.
        :type contextID: |basestring|
        :param done: Callback interface called when operation is completed.
        :type done: |DoneGetContext|

        :returns: Pending command handle, can be used to cancel the command.
        """
        raise NotImplementedError("Abstract method")

    def getChildren(self, parent_context_id, done):
        """Retrieve children of given context.

        :param parent_context_id: parent context ID. Can be **None** - to
                                  retrieve top level of the hierarchy, or one
                                  of context IDs retrieved by previous
                                  |getContext| or |getChildren| methods.
        :type parent_context_id: |basestring| or **None**
        :param done: callback interface called when operation is completed
        :type done: |DoneGetChildren|

        :returns: Pending command handle, can be used to cancel the command.
        """
        raise NotImplementedError("Abstract method")

    def getCommandLine(self, contextID, done):
        """Get context command line.

        :param contextID: ID of the context to get command line for.
        :type contextID: |basestring|
        :param done: Callback interface called when operation is completed.
        :type done: |DoneGetCommandLine|

        :returns: Pending command handle, can be used to cancel the command.
        """
        raise NotImplementedError("Abstract method")

    def getEnvironment(self, contextID, done):
        """Get context environment variables.

        :param contextID: ID of the context to get environment for.
        :type contextID: |basestring|
        :param done: Callback interface called when operation is completed.
        :type done: |DoneGetEnvironment|

        :returns: Pending command handle, can be used to cancel the command.
        """
        raise NotImplementedError("Abstract method")


class DoneGetContext(object):
    """Client callback interface for |getContext|."""

    def doneGetContext(self, token, error, context):
        """Called when context data retrieval is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param context: Retrieved context data.
        :type context: |SysMonitorContext|
        """
        pass


class DoneGetChildren(object):
    """Client callback interface for |getChildren|."""

    def doneGetChildren(self, token, error, context_ids):
        """Called when context list retrieval is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param context_ids: A list of available context IDs.
        :type context_ids: |list|
        """
        pass


class DoneGetCommandLine(object):
    """Client callback interface for |getCommandLine|."""

    def doneGetCommandLine(self, token, error, cmd_line):
        """Called when command line retrieval is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param cmd_line: A list of |basestring| representing this context
                         command line.
        :type cmd_line: |list|
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
