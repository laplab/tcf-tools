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

"""Breakpoint is represented by unique identifier and set of properties.

.. |add| replace:: :meth:`BreakpointsService.add`
.. |addListener| replace:: :meth:`BreakpointsService.addListener`
.. |change| replace:: :meth:`BreakpointsService.change`
.. |contextAdded| replace:: :meth:`BreakpointsListener.contextAdded`
.. |contextChanged| replace:: :meth:`BreakpointsListener.contextChanges`
.. |contextRemoved| replace:: :meth:`BreakpointsListener.contextRemoved`
.. |disable| replace:: :meth:`BreakpointsService.disable`
.. |enable| replace:: :meth:`BreakpointsService.enable`
.. |getCapabilities| replace:: :meth:`BreakpointsService.getCapabilities`
.. |getIDs| replace:: :meth:`BreakpointsService.getIDs`
.. |getProperties| replace:: :meth:`BreakpointsService.getProperties`
.. |getStatus| replace:: :meth:`BreakpointsService.getStatus`
.. |remove| replace:: :meth:`BreakpointsService.remove`
.. |removeListener| replace:: :meth:`BreakpointsService.removeListener`
.. |set| replace:: :meth:`BreakpointsService.set`
.. |Access Modes| replace:: :ref:`Tcf-Breakpoints-Access-Modes`
.. |BreakpointInstance| replace:: :class:`BreakpointInstance`
.. |BreakpointsListener| replace:: :class:`BreakpointsListener`
.. |BreakpointStatus| replace:: :class:`BreakpointStatus`
.. |Breakpoints Properties| replace:: :ref:`Tcf-Breakpoints-Properties`
.. |DoneCommand| replace:: :class:`DoneCommand`
.. |DoneGetCapabilities| replace:: :class:`DoneGetCapabilities`
.. |DoneGetIDs| replace:: :class:`DoneGetIDs`
.. |DoneGetProperties| replace:: :class:`DoneGetProperties`
.. |DoneGetStatus| replace:: :class:`DoneGetStatus`
.. |Pathmap Service| replace:: :mod:`tcf.services.pathmap`
.. |Status| replace:: :ref:`Tcf-Breakpoints-Status`
.. |Status Instances| replace:: :ref:`Tcf-Breakpoints-Status-Instances`
.. |Time Scales| replace:: :ref:`Tcf-Breakpoints-Time-Scales`
.. |Time Units| replace:: :ref:`Tcf-Breakpoints-Time-Units`
.. |Types| replace:: :ref:`Tcf-Breakpoints-Types`

A breakpoint identifier (String id) needs to be unique across all hosts and
targets.

Breakpoint properties (|dict|) is extendible dictionary of named attributes,
which define breakpoint location and behavior. This module defines some common
attribute names (see |Breakpoints Properties|), host tools and target agents
may support additional attributes.

For each breakpoint a target agent maintains another extendible collection of
named attributes: breakpoint status (see |Status|). While breakpoint properties
are persistent and represent user input, breakpoint status reflects dynamic
target agent reports about breakpoint current state, like actual addresses
where breakpoint is planted or planting errors.

Breakpoint Properties
---------------------

.. _Tcf-Breakpoints-Properties:

Properties
^^^^^^^^^^
+-----------------------+--------------+--------------------------------------+
| Name                  | Type         | Description                          |
+=======================+==============+======================================+
| PROP_ACTION           | |basestring| | Expression or script.                |
+-----------------------+--------------+--------------------------------------+
| PROP_ACCESS_MODE      | |int|        | The access mode that will trigger    |
|                       |              | the breakpoint. Access mode can be a |
|                       |              | bitwise OR of the values defined in  |
|                       |              | |Access Modes|.                      |
+-----------------------+--------------+--------------------------------------+
| PROP_CLIENT_DATA      | |dict|       | Properties set by the client.        |
+-----------------------+--------------+--------------------------------------+
| PROP_COLUMN           | |int|        | The source code column number of     |
|                       |              | breakpoint location.                 |
+-----------------------+--------------+--------------------------------------+
| PROP_CONDITION        | |basestring| | Expression that must evaluate to     |
|                       |              | true before the breakpoint is        |
|                       |              | triggered.                           |
+-----------------------+--------------+--------------------------------------+
| PROP_CONTEXT_IDS      | |list|       | Context identifiers for which this   |
|                       |              | breakpoint should be installed.      |
+-----------------------+--------------+--------------------------------------+
| PROP_CONTEXT_NAMES    | |list|       | Contexts names (such as a            |
|                       |              | process/thread name) for which this  |
|                       |              | breakpoint should be installed.      |
+-----------------------+--------------+--------------------------------------+
| PROP_CONTEXT_QUERY    | |basestring| | See :mod:`tcf.services.contextquery` |
+-----------------------+--------------+--------------------------------------+
| PROP_ENABLED          | |bool|       | If true, the breakpoint is enabled.  |
+-----------------------+--------------+--------------------------------------+
| PROP_EVENT_ARGS       | |basestring| | Eventpoint arguments.                |
+-----------------------+--------------+--------------------------------------+
| PROP_EVENT_TYPE       | |basestring| | Breakpoint event type.               |
+-----------------------+--------------+--------------------------------------+
| PROP_EXECUTABLE_PATHS | |list|       | All the target executable paths for  |
|                       |              | which this breakpoint should be      |
|                       |              | installed.                           |
+-----------------------+--------------+--------------------------------------+
| PROP_FILE             | |basestring| | The source code file name of         |
|                       |              | breakpoint location.                 |
+-----------------------+--------------+--------------------------------------+
| PROP_ID               | |basestring| | Breakpoint ID. This is the only      |
|                       |              | required property.                   |
+-----------------------+--------------+--------------------------------------+
| PROP_IGNORE_COUNT     | |int|        | Number of times this breakpoint is   |
|                       |              | to be ignored before it is triggered.|
|                       |              | The ignore count is tested after all |
|                       |              | other Location and Condition         |
|                       |              | properties are validated.            |
+-----------------------+--------------+--------------------------------------+
| PROP_LINE             | |int|        | The source code line number of       |
|                       |              | breakpoint location.                 |
+-----------------------+--------------+--------------------------------------+
| PROP_LINE_OFFSET      | |int|        | Max number of lines breakpoint is    |
|                       |              | allowed to be moved in case of       |
|                       |              | inexact line info match.             |
+-----------------------+--------------+--------------------------------------+
| PROP_LOCATION         | |basestring| | Defines location of the breakpoint.  |
|                       |              | The expression evaluates either to a |
|                       |              | memory address or a register         |
|                       |              | location.                            |
+-----------------------+--------------+--------------------------------------+
| PROP_MASK             | |int|        | A mask which is bitwise ANDed with   |
|                       |              | the value accessed.                  |
+-----------------------+--------------+--------------------------------------+
| PROP_PATTERN          | |int|        | A mask value which may be further    |
|                       |              | refined with a mask.                 |
+-----------------------+--------------+--------------------------------------+
| PROP_SCALE            | |basestring| | The scale for the time value. See    |
|                       |              | |Time Scales|.                       |
+-----------------------+--------------+--------------------------------------+
| PROP_SIZE             | |int|        | The number of bytes starting at      |
|                       |              | address given by the location        |
|                       |              | expression.                          |
+-----------------------+--------------+--------------------------------------+
| PROP_STOP_GROUP       | |list|       | TCF Context identifiers representing |
|                       |              | contexts to be stopped when this     |
|                       |              | breakpoint is triggered. This is an  |
|                       |              | *Action* property that is used to    |
|                       |              | stop contexts in addition to the one |
|                       |              | that triggered the breakpoint.       |
+-----------------------+--------------+--------------------------------------+
| PROP_TEMPORARY        | |bool|       | If set, results in the breakpoint    |
|                       |              | being removed after it is triggered  |
|                       |              | once. The default value for this     |
|                       |              | property is **False**.               |
+-----------------------+--------------+--------------------------------------+
| PROP_TIME             | |int|        | The time value in the execution of   |
|                       |              | the program at which to set the      |
|                       |              | breakpoint.                          |
+-----------------------+--------------+--------------------------------------+
| PROP_TYPE             | |basestring| | The breakpoint type. See |Types|.    |
+-----------------------+--------------+--------------------------------------+
| PROP_UNITS            | |basestring| | The units for the time value. See    |
|                       |              | |Time Units|.                        |
+-----------------------+--------------+--------------------------------------+
| PROP_SKIP_PROLOGUE    | |basestring| | If set, the breakpoint is set after  |
|                       |              | the function prologue. The default   |
|                       |              | value for this property is **False**.|
+-----------------------+--------------+--------------------------------------+

.. _Tcf-Breakpoints-Access-Modes:

Access Modes
^^^^^^^^^^^^
According to its **PROP_ACCESS_MODE** property, the breakpoints is triggered
on one of these access modes:

+--------------------+----------+---------------------------------------------+
| Name               | Value    | Description                                 |
+====================+==========+=============================================+
| ACCESSMODE_CHANGE  | 0x08     | Breakpoint is triggered by a data change    |
|                    |          | (not an explicit write) at the breakpoint   |
|                    |          | location.                                   |
+--------------------+----------+---------------------------------------------+
| ACCESSMODE_EXECUTE | 0x04     | Breakpoint is triggered by an instruction   |
|                    |          | execution at the breakpoint location.       |
|                    |          | Whether the breakpoint is triggered before  |
|                    |          | or after the instruction execution depends  |
|                    |          | on the target support for this mode. This is|
|                    |          | the default for Line and Address            |
|                    |          | breakpoints.                                |
+--------------------+----------+---------------------------------------------+
| ACCESSMODE_READ    | 0x01     | Breakpoints is triggered by a read from the |
|                    |          | breakpoint location.                        |
+--------------------+----------+---------------------------------------------+
| ACCESSMODE_WRITE   | 0x02     | Breakpoint is triggered by a write to the   |
|                    |          | breakpoint location.                        |
+--------------------+----------+---------------------------------------------+

.. _Tcf-Breakpoints-Time-Scales:

Time Scales
^^^^^^^^^^^
+--------------------+--------------------------------------------------------+
| Name               | Description                                            |
+====================+========================================================+
| TIMESCALE_ABSOLUTE | Time value in the absolute time scale.                 |
+--------------------+--------------------------------------------------------+
| TIMESCALE_RELATIVE | Time value in the relative time scale. This is the     |
|                    | default value for this property. In the relative time  |
|                    | scale, the Time property may have a negative value.    |
+--------------------+--------------------------------------------------------+

.. _Tcf-Breakpoints-Time-Units:

Time Units
^^^^^^^^^^
+----------------------------+------------------------------------------------+
| Name                       | Description                                    |
+============================+================================================+
| TIMEUNIT_CYCLE_COUNT       | Time value in cycles. This is the default type.|
+----------------------------+------------------------------------------------+
| TIMEUNIT_INSTRUCTION_COUNT | Time value in instructions.                    |
+----------------------------+------------------------------------------------+
| TIMEUNIT_NSECS             | Time value in nano seconds.                    |
+----------------------------+------------------------------------------------+

.. _Tcf-Breakpoints-Types:

Types
^^^^^
+---------------+-------------------------------------------------------------+
| Name          | Description                                                 |
+===============+=============================================================+
| TYPE_HARDWARE | Hardware breakpoint type.                                   |
+---------------+-------------------------------------------------------------+
| TYPE_AUTO     | Auto breakpoint type.                                       |
+---------------+-------------------------------------------------------------+
| TYPE_SOFTWARE | Software breakpoint type.                                   |
+---------------+-------------------------------------------------------------+

.. _Tcf-Breakpoints-Status:

Status
^^^^^^
+------------------+--------------+-------------------------------------------+
| Name             | Type         | Description                               |
+==================+==============+===========================================+
| STATUS_COLUMN    | |int|        | Breakpoint column.                        |
+------------------+--------------+-------------------------------------------+
| STATUS_ERROR     | |basestring| | Breakpoint status error.                  |
+------------------+--------------+-------------------------------------------+
| STATUS_FILE      | |basestring| | Breakpoint file.                          |
+------------------+--------------+-------------------------------------------+
| STATUS_INSTANCES | |list|       | Breakpoint status instance. See           |
|                  |              | |Status Instances|.                       |
+------------------+--------------+-------------------------------------------+
| STATUS_LINE      | |int|        | Breakpoint line.                          |
+------------------+--------------+-------------------------------------------+

.. _Tcf-Breakpoints-Status-Instances:

Status Instances
^^^^^^^^^^^^^^^^
+--------------------------+--------------+-----------------------------------+
| Name                     | Type         | Description                       |
+==========================+==============+===================================+
| INSTANCE_ADDRESS         | |int|        | Breakpoint address.               |
+--------------------------+--------------+-----------------------------------+
| INSTANCE_CONDITION_ERROR | |basestring| | Breakpoint error message for an   |
|                          |              | invalid condition.                |
+--------------------------+--------------+-----------------------------------+
| INSTANCE_CONTEXT         | |basestring| | Breakpoint context.               |
+--------------------------+--------------+-----------------------------------+
| INSTANCE_ERROR           | |basestring| | Breakpoint status instance error. |
+--------------------------+--------------+-----------------------------------+
| INSTANCE_HIT_COUNT       | |int|        | Breakpoint hit count.             |
+--------------------------+--------------+-----------------------------------+
| INSTANCE_MEMORY_CONTEXT  | |basestring| | Breakpoint memory context.        |
+--------------------------+--------------+-----------------------------------+
| INSTANCE_SIZE            | |int|        | Breakpoint size.                  |
+--------------------------+--------------+-----------------------------------+
| INSTANCE_TYPE            | |basestring| | Breakpoint type.                  |
+--------------------------+--------------+-----------------------------------+

Service Capabilities
^^^^^^^^^^^^^^^^^^^^
All capabilities are of |bool| type, but the **CAPABILITY_CONTEXT_ID** which is
of |basestring| type, and **CAPABILITY_ACCESS_MODE** which is of |int| type.

+----------------------------+------------------------------------------------+
+ Name                       | Description                                    |
+============================+================================================+
| CAPABILITY_ACCESS_MODE     | An access mode value, which is a bitwise OR of |
|                            | the values defined in |Access Modes|. A value  |
|                            | of ``0`` means that the ``PROP_ACCESS_MODE``   |
|                            | breakpoint property is not supported for the   |
|                            | given context.                                 |
+----------------------------+------------------------------------------------+
| CAPABILITY_BREAKPOINT_TYPE | If **True**, **PROP_TYPE** breakpoint property |
|                            | is supported.                                  |
+----------------------------+------------------------------------------------+
| CAPABILITY_CLIENT_DATA     | If **True**, **PROP_CLIENT_DATA** breakpoint   |
|                            | property is supported.                         |
+----------------------------+------------------------------------------------+
| CAPABILITY_CONDITION       | If **True**, **PROP_CONDITION** breakpoint     |
|                            | property is supported.                         |
+----------------------------+------------------------------------------------+
| CAPABILITY_CONTEXT_ID      | ID of a context that was used to query         |
|                            | capabilities.                                  |
+----------------------------+------------------------------------------------+
| CAPABILITY_CONTEXT_IDS     | If **True**, **PROP_CONTEXT_IDS** breakpoint   |
|                            | property is supported.                         |
+----------------------------+------------------------------------------------+
| CAPABILITY_CONTEXT_NAMES   | If **True**, **PROP_CONTEXT_NAMES** breakpoint |
|                            | property is supported.                         |
+----------------------------+------------------------------------------------+
| CAPABILITY_CONTEXT_QUERY   | If **True**, **PROP_CONTEXT_QUERY** breakpoint |
|                            | property is supported.                         |
+----------------------------+------------------------------------------------+
| CAPABILITY_FILE_LINE       | If **True**, **PROP_FILE**, **PROP_LINE** and  |
|                            | **PROP_COLUMN** breakpoint properties are      |
|                            | supported.                                     |
+----------------------------+------------------------------------------------+
| CAPABILITY_FILE_MAPPING    | If **True**, using file pathmapping is         |
|                            | supported. See |Pathmap Service|.              |
+----------------------------+------------------------------------------------+
| CAPABILITY_HAS_CHILDREN    | If **True**, children of the context can have  |
|                            | different capabilities.                        |
+----------------------------+------------------------------------------------+
| CAPABILITY_IGNORE_COUNT    | If **True**, **PROP_IGNORE_COUNT** breakpoint  |
|                            | property is supported.                         |
+----------------------------+------------------------------------------------+
| CAPABILITY_LOCATION        | If **True**, **PROP_LOCATION** breakpoint      |
|                            | property is supported.                         |
+----------------------------+------------------------------------------------+
| CAPABILITY_STOP_GROUP      | If **True**, **PROP_STOP_GROUP** breakpoint    |
|                            | property is supported.                         |
+----------------------------+------------------------------------------------+
| CAPABILITY_TEMPORARY       | If **True**, **PROP_TEMPORARY** breakpoint     |
|                            | property is supported.                         |
+----------------------------+------------------------------------------------+
| CAPABILITY_SKIP_PROLOGUE   | If **True**, **PROP_SKIP_PROLOGUE** breakpoint |
|                            | property is supported.                         |
+----------------------------+------------------------------------------------+

Service Methods
---------------
.. autodata:: NAME
.. autoclass:: BreakpointsService

add
^^^
.. automethod:: BreakpointsService.add

addListener
^^^^^^^^^^^
.. automethod:: BreakpointsService.addListener

change
^^^^^^
.. automethod:: BreakpointsService.change

disable
^^^^^^^
.. automethod:: BreakpointsService.disable

enable
^^^^^^
.. automethod:: BreakpointsService.enable

getCapabilities
^^^^^^^^^^^^^^^
.. automethod:: BreakpointsService.getCapabilities

getIDs
^^^^^^
.. automethod:: BreakpointsService.getIDs

getName
^^^^^^^
.. automethod:: BreakpointsService.getName

getProperties
^^^^^^^^^^^^^
.. automethod:: BreakpointsService.getProperties

getStatus
^^^^^^^^^
.. automethod:: BreakpointsService.getStatus

remove
^^^^^^
.. automethod:: BreakpointsService.remove

removeListener
^^^^^^^^^^^^^^
.. automethod:: BreakpointsService.removeListener

set
^^^
.. automethod:: BreakpointsService.set

Callback Classes
----------------
DoneCommand
^^^^^^^^^^^
.. autoclass:: DoneCommand
    :members:

DoneGetCapabilities
^^^^^^^^^^^^^^^^^^^
.. autoclass:: DoneGetCapabilities
    :members:

DoneGetIDs
^^^^^^^^^^
.. autoclass:: DoneGetIDs
    :members:

DoneGetProperties
^^^^^^^^^^^^^^^^^
.. autoclass:: DoneGetProperties
    :members:

DoneGetStatus
^^^^^^^^^^^^^^^^^^^
.. autoclass:: DoneGetStatus
    :members:

Listener
--------
.. autoclass:: BreakpointsListener
    :members:

Helper Classes
--------------
BreakpointInstance
^^^^^^^^^^^^^^^^^^
.. autoclass:: BreakpointInstance
    :members:

BreakpointStatus
^^^^^^^^^^^^^^^^
.. autoclass:: BreakpointStatus
    :members:
"""

from .. import services

# Service name.
NAME = "Breakpoints"
"""Breakpoints service name."""

# Breakpoint property names.
PROP_ID = "ID"
PROP_ENABLED = "Enabled"
PROP_TYPE = "BreakpointType"
PROP_CONTEXT_NAMES = "ContextNames"
PROP_CONTEXT_IDS = "ContextIds"
PROP_EXECUTABLE_PATHS = "ExecPaths"
PROP_CONTEXT_QUERY = "ContextQuery"
PROP_LOCATION = "Location"
PROP_SIZE = "Size"
PROP_ACCESS_MODE = "AccessMode"
PROP_FILE = "File"
PROP_LINE = "Line"
PROP_COLUMN = "Column"
PROP_PATTERN = "MaskValue"
PROP_MASK = "Mask"
PROP_STOP_GROUP = "StopGroup"
PROP_IGNORE_COUNT = "IgnoreCount"
PROP_TIME = "Time"
PROP_SCALE = "TimeScale"
PROP_UNITS = "TimeUnits"
PROP_CONDITION = "Condition"
PROP_TEMPORARY = "Temporary"
PROP_EVENT_TYPE = "EventType"
PROP_EVENT_ARGS = "EventArgs"
PROP_CLIENT_DATA = "ClientData"
PROP_SKIP_PROLOGUE = "SkipPrologue"
PROP_ACTION = "Action"
PROP_LINE_OFFSET = "LineOffset"

# Deprecated
PROP_CONTEXTNAMES = "ContextNames"
PROP_CONTEXTIDS = "ContextIds"
PROP_EXECUTABLEPATHS = "ExecPaths"
PROP_ACCESSMODE = "AccessMode"
PROP_IGNORECOUNT = "IgnoreCount"


# BreakpointType values
TYPE_SOFTWARE = "Software"
TYPE_HARDWARE = "Hardware"
TYPE_AUTO = "Auto"

# AccessMode values
ACCESSMODE_READ = 0x01
ACCESSMODE_WRITE = 0x02
ACCESSMODE_EXECUTE = 0x04
ACCESSMODE_CHANGE = 0x08

# TimeScale values
TIMESCALE_RELATIVE = "Relative"
TIMESCALE_ABSOLUTE = "Absolute"

# TimeUnits values
TIMEUNIT_NSECS = "Nanoseconds"
TIMEUNIT_CYCLE_COUNT = "CycleCount"
TIMEUNIT_INSTRUCTION_COUNT = "InstructionCount"

# Breakpoint status field names.
STATUS_INSTANCES = "Instances"
STATUS_ERROR = "Error"
STATUS_FILE = "File"
STATUS_LINE = "Line"
STATUS_COLUMN = "Column"

# Breakpoint instance field names.
INSTANCE_ERROR = "Error"
INSTANCE_CONTEXT = "LocationContext"
INSTANCE_ADDRESS = "Address"
INSTANCE_SIZE = "Size"
INSTANCE_TYPE = "BreakpointType"
INSTANCE_MEMORY_CONTEXT = "MemoryContext"
INSTANCE_HIT_COUNT = "HitCount"
INSTANCE_CONDITION_ERROR = "ConditionError"

# Breakpoint service capabilities.
CAPABILITY_CONTEXT_ID = "ID"
CAPABILITY_HAS_CHILDREN = "HasChildren"
CAPABILITY_BREAKPOINT_TYPE = "BreakpointType"
CAPABILITY_LOCATION = "Location"
CAPABILITY_CONDITION = "Condition"
CAPABILITY_FILE_LINE = "FileLine"
CAPABILITY_FILE_MAPPING = "FileMapping"
CAPABILITY_CONTEXT_IDS = "ContextIds"
CAPABILITY_CONTEXT_NAMES = "ContextNames"
CAPABILITY_CONTEXT_QUERY = "ContextQuery"
CAPABILITY_STOP_GROUP = "StopGroup"
CAPABILITY_TEMPORARY = "Temporary"
CAPABILITY_IGNORE_COUNT = "IgnoreCount"
CAPABILITY_ACCESS_MODE = "AccessMode"
CAPABILITY_CLIENT_DATA = "ClientData"
CAPABILITY_SKIP_PROLOGUE = "SkipPrologue"

# Deprecated
CAPABILITY_CONTEXTNAMES = "ContextNames"
CAPABILITY_CONTEXTIDS = "ContextIds"
CAPABILITY_IGNORECOUNT = "IgnoreCount"
CAPABILITY_ACCESSMODE = "AccessMode"


class BreakpointsService(services.Service):
    """TCF Breakpoints service interface."""

    def getName(self):
        """Get this service name.

        :returns: A |basestring| representing this service name, which is the
                  value of :const:`NAME`
        """
        return NAME

    def set(self, properties, done):  # @ReservedAssignment
        """Download breakpoints data to target agent.

        The command is intended to be used only to initialize target
        breakpoints table when communication channel is open. After that, host
        should notify target about (incremental) changes in breakpoint data by
        sending |add|, |change| and |remove| commands.

        :param properties: List of breakpoints to set.
        :type properties: |list|
        :param done: Command result call back object.
        :type done: |DoneCommand|

        :returns: Pending command handle.
        """
        raise NotImplementedError("Abstract method")

    def add(self, properties, done):
        """Called when breakpoint is added into breakpoints table.

        :param properties: Breakpoint properties. See |Breakpoints Properties|.
        :type properties: |dict|
        :param done: Command result call back object.
        :type done: |DoneCommand|

        :returns: Pending command handle.
        """
        raise NotImplementedError("Abstract method")

    def change(self, properties, done):
        """Called when breakpoint properties are changed.

        :param properties: Breakpoint properties. See |Breakpoints Properties|.
        :type properties: |dict|
        :param done: Command result call back object.
        :type done: |DoneCommand|

        :returns: Pending command handle.
        """
        raise NotImplementedError("Abstract method")

    def enable(self, ids, done):
        """Tell target to change (only) **PROP_ENABLED** breakpoint property to
        **True**.

        See |Breakpoints Properties| for **PROP_ENABLED** description.

        :param ids: A list of enabled breakpoint identifiers.
        :type ids: |list| or |tuple| of |basestring|
        :param done: Command result call back object.
        :type done: |DoneCommand|

        :returns: Pending command handle.
        """
        raise NotImplementedError("Abstract method")

    def disable(self, ids, done):
        """Tell target to change (only) **PROP_ENABLED** breakpoint property to
        **False**.

        See |Breakpoints Properties| for **PROP_ENABLED** description.

        :param ids: A list of disabled breakpoint identifiers.
        :type ids: |list| or |tuple| of |basestring|
        :param done: Command result call back object.
        :type done: |DoneCommand|

        :returns: Pending command handle.
        """
        raise NotImplementedError("Abstract method")

    def remove(self, ids, done):
        """Tell target to remove breakpoints.

        :param id: unique breakpoint identifier.
        :type id: |basestring|
        :param done: Command result call back object.
        :type done: |DoneCommand|

        :returns: Pending command handle.
        """
        raise NotImplementedError("Abstract method")

    def getIDs(self, done):
        """Upload IDs of breakpoints known to target agent.

        :param done: Command result call back object.
        :type done: |DoneGetIDs|

        :returns: Pending command handle.
        """
        raise NotImplementedError("Abstract method")

    def getProperties(self, bpID, done):
        """Upload properties of given breakpoint from target agent breakpoint
        table.

        :param bpID: Unique breakpoint identifier.
        :type bpID: |basestring|
        :param done: Command result call back object.
        :type done: |DoneGetProperties|

        :returns: Pending command handle.
        """
        raise NotImplementedError("Abstract method")

    def getStatus(self, bpID, done):
        """Upload status of given breakpoint from target agent.

        :param bpID: Unique breakpoint identifier.
        :type bpID: |basestring|
        :param done: Command result call back object.
        :type done: |DoneGetStatus|

        :returns: Pending command handle.
        """
        raise NotImplementedError("Abstract method")

    def getCapabilities(self, bpID, done):
        """Report breakpoint service capabilities to clients so they can adjust
        to different implementations of the service.

        When called with a **None** context ID the global capabilities are
        returned, otherwise context specific capabilities are returned. A
        special capability property is used to indicate that all child contexts
        have the same capabilities.

        :param bpID: A context ID or **None**.
        :type bpID: |basestring| or **None**
        :param done: command result call back object.
        :type done: |DoneGetCapabilities|

        :returns: Pending command handle.
        """
        raise NotImplementedError("Abstract method")

    def addListener(self, listener):
        """Add breakpoints service event listener.

        :param listener: Object that implements |BreakpointsListener| interface
                         to add to the channel.
        :type listener: |BreakpointsListener|
        """
        raise NotImplementedError("Abstract method")

    def removeListener(self, listener):
        """Remove breakpoints service event listener.

        :param listener: Listener to remove from this breakpoints service
                         channel.
        :type listener: |BreakpointsListener|
        """
        raise NotImplementedError("Abstract method")


class BreakpointInstance(object):
    """A class to represent a breakpoint status instances.

    :param props: The properties to initialise the breakpoint status instance
                  with. See |Status Instances|.
    :type props: |dict|
    """
    def __init__(self, props):
        self._properties = props or {}

    def __repr__(self):
        return self.__class__.__name__ + '(' + str(self._properties) + ')'

    def __str__(self):
        res = self.__class__.__name__ + ' ['
        res += 'Context=' + self.context
        res += ', ' + INSTANCE_ADDRESS + '=' + str(self.address)
        res += ', ' + INSTANCE_HIT_COUNT + '=' + str(self.hitcount)
        res += ', ' + INSTANCE_TYPE + '=' + str(self.type)
        res += ', ' + INSTANCE_SIZE + '=' + str(self.size)
        res += ', ' + INSTANCE_MEMORY_CONTEXT + '=' + str(self.memorycontext)
        res += ', ' + INSTANCE_ERROR + '=' + str(self.error)
        res += ']'
        return res

    @property
    def address(self):
        """Breakpoint status instance address.

        :returns: An |int| representing the address this breakpoint status
                  instance occurred at, or **None** if unknown.
        """
        return self._properties.get(INSTANCE_ADDRESS, None)

    @property
    def context(self):
        """ID of the context this Breakpoint status instance occurred for.

        :returns: A |basestring| representing the ID of the context this
                  breakpoint status instance occurred for, or **None**
                  if unknown.
        """
        return self._properties.get(INSTANCE_CONTEXT, None)

    @property
    def error(self):
        """Potential error for this Breakpoint status instance.

        :returns: A |basestring| representing the error for this breakpoint
                  status instance, or **None** if there is no error.
        """
        return self._properties.get(INSTANCE_ERROR, None)

    @property
    def hitcount(self):
        """Number of breakpoint hit count for this breakpoint status instance.

        :returns: An |int| representing the number of times this breakpoint
                  status instance has been hit, or **None** if unknown.
        """
        return self._properties.get(INSTANCE_HIT_COUNT, None)

    @property
    def memorycontext(self):
        """ID of the memory context this Breakpoint status instance occurred
        for.

        :returns: A |basestring| representing the ID of the memory context this
                  breakpoint status instance occurred for, or **None**
                  if unknown.
        """
        return self._properties.get(INSTANCE_MEMORY_CONTEXT, None)

    @property
    def size(self):
        """The size of this breakpoint.

        :returns: An |int| representing the size of the breakpoint this status
                  instance occured for, or **None**
                  if unknown.
        """
        return self._properties.get(INSTANCE_SIZE, None)

    @property
    def type(self):
        """The type of this breakpoint.

        See |Types|.

        :returns: A |basestring| representing the type of the breakpoint this
                  status instance occured for, or **None** if unknown.

        .. seealso:: |Types|
        """
        return self._properties.get(INSTANCE_TYPE, None)


class BreakpointStatus(object):
    """A class to represent a breakpoint status.

    :param props: The properties to initialise the breakpoint status with.
                  See |Status|.
    :type props: |dict|
    """
    def __init__(self, props):
        self._properties = props or {}
        iprops = self._properties.get(STATUS_INSTANCES, [])
        self._instances = []
        for iprop in iprops:
            self._instances.append(BreakpointInstance(iprop))

    def __repr__(self):
        return self.__class__.__name__ + '(' + str(self._properties) + ')'

    def __str__(self):
        res = self.__class__.__name__ + ' ['
        res += STATUS_FILE + '=' + str(self.file)
        res += ', ' + STATUS_LINE + '=' + str(self.line)
        res += ', ' + STATUS_COLUMN + '=' + str(self.column)
        res += ', ' + STATUS_ERROR + '=' + str(self.error)
        res += ', ' + STATUS_INSTANCES + '=['
        firstInstance = True
        for instance in self._instances:
            if not firstInstance:
                res += ', '
            res += str(instance)
            firstInstance = False
        res += ']'
        res += ']'
        return res

    @property
    def column(self):
        """Column in *file* the breakpoint is planted at.

        :returns: An |int| representing the column at which this breakpoint
                  status occurred in *file*, or **None** if unknown.
        """
        return self._properties.get(STATUS_COLUMN, None)

    @property
    def error(self):
        """Breakpoint status error.

        A breakpoint status may have an error.

        :returns: A |basestring| representing this breakpoint status error, or
                  **None**.
        """
        return self._properties.get(STATUS_ERROR, None)

    @property
    def file(self):
        """File the breakpoint is planted in.

        :returns: A |basestring| representing the path of the file the
                  breakpoint is planted in, or **None** if the file is not
                  known, or unreachable.
        """
        return self._properties.get(STATUS_FILE, None)

    @property
    def instances(self):
        """Breakpoint status instances.

        :returns: A |tuple| of |BreakpointInstance| objects representing the
                  various instances of this breakpoint status.
        """
        return self._instances

    @property
    def line(self):
        """Line in *file* the breakpoint is planted at.

        :returns: An |int| representing the line at which this breakpoint
                  status occurred in *file*, or **None** if unknown.
        """
        return self._properties.get(STATUS_LINE, None)


class DoneCommand(object):
    """Call back interface for breakpoint service commands.

    ..seealso:: |add|, |change|, |disable|, |enable|, |remove|, |set|
    """

    def doneCommand(self, token, error):
        """Called when command is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        """
        pass


class DoneGetIDs(object):
    """Call back interface for |getIDs| command."""

    def doneGetIDs(self, token, error, ids):
        """Called when |getIDs| command is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param ids: IDs of breakpoints known to target agent.
        :type ids: |list| or |tuple| of |basestring|
        """
        pass


class DoneGetProperties(object):
    """Call back interface for |getProperties| command."""

    def doneGetProperties(self, token, error, properties):
        """Called when |getProperties| command is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param properties: Properties of the breakpoint.
        :type properties: |dict|

        .. seealso:: |Breakpoints Properties|
        """
        pass


class DoneGetStatus(object):
    """Call back interface for :meth:`~BreakpointsService.getStatus` command.
    """
    def doneGetStatus(self, token, error, status):
        """Called when |getStatus| command is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param status: Status of the breakpoint.
        :type status: |BreakpointStatus|
        """
        pass


class DoneGetCapabilities(object):
    """Call back interface for |getCapabilities| command."""

    def doneGetCapabilities(self, token, error, capabilities):
        """Called when |getCapabilities| command is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param capabilities: Breakpoints service capabilities description.
        :type capabilities: |dict|
        """
        pass


class BreakpointsListener(object):
    """Breakpoints service events listener.

    .. note:: Note that |contextAdded|, |contextChanged| and |contextRemoved|
              events carry exactly same set of breakpoint properties that was
              sent by a client to a target. The purpose of these events is to
              let all clients know about breakpoints that were created by other
              clients.
    """

    def breakpointStatusChanged(self, bpID, status):
        """Called when breakpoint status changes.

        :param bpID: Unique breakpoint identifier.
        :type bpID: |basestring|
        :param status: Breakpoint status.
        :type status: |dict|
        """
        pass

    def contextAdded(self, bps):
        """Called when new breakpoints are added.

        :param bps: Array of breakpoints.
        :type bps: |list| or |tuple| of |dict|
        """
        pass

    def contextChanged(self, bps):
        """Called when breakpoint properties change.

        :param bps: Array of breakpoints.
        :type bps: |list| or |tuple| of |dict|
        """
        pass

    def contextRemoved(self, ids):
        """Called when breakpoints are removed.

        :param ids: Array of breakpoint IDs.
        :type ids: |list| of |basestring|
        """
        pass
