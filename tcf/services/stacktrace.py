# *****************************************************************************
# * Copyright (c) 2011, 2014-2015, 2016 Wind River Systems, Inc. and others.
# * All rights reserved. This program and the accompanying materials
# * are made available under the terms of the Eclipse Public License 2.0
# * which accompanies this distribution, and is available at
# * https://www.eclipse.org/legal/epl-2.0/
# *
# * Contributors:
# *     Wind River Systems - initial API and implementation
# *****************************************************************************

"""TCF stacktrace service interface.

.. |getChildren| replace:: :meth:`~StackTraceService.getChildren`
.. |getChildrenRange| replace:: :meth:`~StackTraceService.getChildrenRange`
.. |getContext| replace:: :meth:`~StackTraceService.getContext`
.. |runcontrol| replace:: :mod:`~tcf.services.runcontrol`
.. |DoneGetChildren| replace:: :class:`DoneGetChildren`
.. |DoneGetContext| replace:: :class:`DoneGetContext`


The service implements thread stack back tracing.

Properties
----------

+--------------------------+--------------+-----------------------------------+
| Name                     | Type         | Description                       |
+==========================+==============+===================================+
| PROP_ARGUMENTS_ADDRESS   | |int|        | Memory address of function        |
|                          |              | arguments.                        |
+--------------------------+--------------+-----------------------------------+
| PROP_ARGUMENTS_COUNT     | |int|        | Number of function arguments.     |
+--------------------------+--------------+-----------------------------------+
| PROP_FRAME_ADDRESS       | |int|        | Stack frame memory address.       |
+--------------------------+--------------+-----------------------------------+
| PROP_ID                  | |basestring| | String, stack frame ID.           |
+--------------------------+--------------+-----------------------------------+
| PROP_INDEX               | |int|        | Stack frame level, starting from  |
|                          |              | stack top.                        |
+--------------------------+--------------+-----------------------------------+
| PROP_INSTRUCTION_ADDRESS | |int|        | Instruction pointer.              |
+--------------------------+--------------+-----------------------------------+
| PROP_LEVEL               | |int|        | Stack frame level, starting from  |
|                          |              | stack bottom.                     |
+--------------------------+--------------+-----------------------------------+
| PROP_NAME                | |basestring| | Human readable name.              |
+--------------------------+--------------+-----------------------------------+
| PROP_PARENT_ID           | |basestring| | Stack frame parent ID.            |
+--------------------------+--------------+-----------------------------------+
| PROP_PROCESS_ID          | |basestring| | Stack frame process ID.           |
+--------------------------+--------------+-----------------------------------+
| PROP_RETURN_ADDRESS      | |int|        | Return address.                   |
+--------------------------+--------------+-----------------------------------+
| PROP_TOP_FRAME           | |bool|       | **True** if the frame is top frame|
|                          |              | on a stack.                       |
+--------------------------+--------------+-----------------------------------+
| PROP_WALK                | |bool|       | **True** if the frame is found by |
|                          |              | stack walking (debug info).       |
+--------------------------+--------------+-----------------------------------+
| PROP_INLINED             | |int|        | Inlined function level.           |
+--------------------------+--------------+-----------------------------------+
| PROP_FUNC_ID             | |basestring| | Function symbol ID.               |
+--------------------------+--------------+-----------------------------------+
| PROP_CODE_AREA           | |CodeArea|   | Call site code area.              |
+--------------------------+--------------+-----------------------------------+

Service Methods
---------------
.. autodata:: NAME
.. autoclass:: StackTraceService

getName
^^^^^^^
.. automethod:: StackTraceService.getName

getContext
^^^^^^^^^^
.. automethod:: StackTraceService.getContext

getChildren
^^^^^^^^^^^
.. automethod:: StackTraceService.getChildren

getChildrenRange
^^^^^^^^^^^^^^^^
.. automethod:: StackTraceService.getChildrenRange

Callback Classes
----------------
DoneGetContext
^^^^^^^^^^^^^^^^^
.. autoclass:: DoneGetContext
    :members:

DoneGetChildren
^^^^^^^^^^^^^^^
.. autoclass:: DoneGetChildren
    :members:


Helper Classes
--------------
StackTraceContext
^^^^^^^^^^^^^^^^^
.. autoclass:: StackTraceContext
    :members:
"""

from .. import services
from .remote.LineNumbersProxy import _toCodeAreaArray

NAME = "StackTrace"
"""StackTrace service name."""

PROP_ID = "ID"
PROP_PARENT_ID = "ParentID"
PROP_PROCESS_ID = "ProcessID"
PROP_NAME = "Name"
PROP_TOP_FRAME = "TopFrame"
PROP_LEVEL = "Level"
PROP_FRAME_ADDRESS = "FP"
PROP_RETURN_ADDRESS = "RP"
PROP_INSTRUCTION_ADDRESS = "IP"
PROP_ARGUMENTS_COUNT = "ArgsCnt"
PROP_ARGUMENTS_ADDRESS = "ArgsAddr"
PROP_INDEX = "Index"
PROP_WALK = "Walk"
PROP_INLINED = "Inlined"
PROP_FUNC_ID = "FuncID"
PROP_CODE_AREA = "CodeArea"


class StackTraceService(services.Service):
    """TCF stacktrace service interface."""

    def getName(self):
        """Get this service name.

        :returns: This service name, which is the value of :const:`NAME`
        """
        return NAME

    def getContext(self, ids, done):
        """Retrieve context info for given context IDs.

        The command will fail if parent thread is not suspended. Client can use
        |runcontrol| service to suspend a thread.

        :param ids: List of context IDs.
        :type ids: |tuple| or |list|
        :param done: call back interface called when operation is completed
        :type done: |DoneGetContext|
        """
        raise NotImplementedError("Abstract method")

    def getChildren(self, parent_context_id, done):
        """Retrieve stack trace contexts list.

        Parent context usually corresponds to an execution thread.

        Some targets have more than one stack. In such case children of a
        thread are stacks, and stack frames are deeper in the hierarchy - they
        can be retrieved with additional :meth:`getChildren` commands.

        The command will fail if parent thread is not suspended. Client can use
        |runcontrol| service to suspend a thread.

        :param parent_context_id: Parent context ID.
        :type parent_context_id: |basestring|
        :param done: call back interface called when operation is completed
        :type done: |DoneGetChildren|
        """
        raise NotImplementedError("Abstract method")

    def getChildrenRange(self, parent_context_id, range_start, range_end,
                         done):
        """Retrieve a range of stack trace contexts.

        Parent context usually corresponds to an execution thread.

        Some targets have more than one stack. In such case children of a
        thread are stacks, and stack frames are deeper in the hierarchy - they
        can be retrieved with additional :meth:`getChildren` commands.

        The command will fail if parent thread is not suspended. Client can use
        |runcontrol| service to suspend a thread.

        :param parent_context_id: Parent context ID.
        :type parent_context_id: |basestring|
        :param range_start: Start index of the range (inclusive). Index 0 is
                            the top frame.
        :type range_start: |int|
        :param range_end: End index of the range (inclusive).
        :type range_end: |int|
        :param done: call back interface called when operation is completed
        :type done: |DoneGetChildren|
        """
        raise NotImplementedError("Abstract method")


class DoneGetContext(object):
    """Client call back interface for |getContext|."""

    def doneGetContext(self, token, error, contexts):
        """Called when context data retrieval is done.

        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param contexts: A list of context data or **None** if error.
        :type contexts: |tuple| or **None**
        """
        pass


class DoneGetChildren(object):
    """Client call back interface for |getChildren|."""

    def doneGetChildren(self, token, error, context_ids):
        """Called when context list retrieval is done.

        .. note:: Stack frames are ordered from stack bottom to top.

        :param error: error description if operation failed, **None** if
                      succeeded
        :param context_ids: A list of available context IDs.
        :type context_ids: |tuple|
        """
        pass


class StackTraceContext(object):
    """StackTrace context class.

    *StackTraceContext* represents stack trace objects : stacks and stack
    frames.

    :param props: The properties to initialise object with. See `Properties`_.
    :type props: |dict|
    """
    def __init__(self, props):
        self._props = props or {}

    def __str__(self):
        return "[Stack Trace Context %s]" % self._props

    def __eq__(self, other):
        # Two frames are considered equal if they have the same properties
        if other and isinstance(other, StackTraceContext):
            return self.getProperties() == other.getProperties()
        return False

    def __getComparable(self, other):
        assert isinstance(other, StackTraceContext)

        # levels from bottom to top, but we want top first when sorted
        levels = (other.getLevel(), self.getLevel())
        # indexes from top to bottom
        indexes = (self.getIndex(), other.getIndex())

        # By default, use Level as it is more reliable to perform comparison,
        # even between frames from successive runcontrol (Level is absolute,
        # Index is function of the top frame which changes).
        if -1 not in levels:
            return levels
        if -1 not in indexes:
            return indexes

        return None

    def __ge__(self, other):
        # Compare frames through their index or levels.
        if other and isinstance(other, StackTraceContext):
            comp = self.__getComparable(other)
            return comp and comp[0] >= comp[1]
        return False

    def __gt__(self, other):
        # Compare frames through their index or levels.
        if other and isinstance(other, StackTraceContext):
            comp = self.__getComparable(other)
            return comp and comp[0] > comp[1]
        return True

    def __le__(self, other):
        # Compare frames through their index or levels.
        if other and isinstance(other, StackTraceContext):
            comp = self.__getComparable(other)
            return comp and comp[0] <= comp[1]
        return False

    def __lt__(self, other):
        # Compare frames through their index or levels.
        if other and isinstance(other, StackTraceContext):
            comp = self.__getComparable(other)
            return comp and comp[0] < comp[1]
        return False

    def __ne__(self, other):
        # Two frames are considered equal if they have the same properties
        if other and isinstance(other, StackTraceContext):
            return self.getProperties() != other.getProperties()
        return True

    def getID(self):
        """Get Context ID.

        :returns: A |basestring| representing this stack context ID. This is
                  the only mandatory field.
        """
        return self._props.get(PROP_ID, '')

    def getIndex(self):
        """Get stack index.

        :returns: An |int| representing this stack index, 0 being the top
                  frame, or **-1** if unknown.
        """
        return self._props.get(PROP_INDEX, -1)

    def getLevel(self):
        """Get stack level.

        :returns: An |int| representing this context stack level, or **-1** if
                  unknown.
        """
        return self._props.get(PROP_LEVEL, -1)

    def getParentID(self):
        """Get parent context ID.

        :returns: A |basestring| representing parent context ID, or an empty
                  |basestring| if unknown.
        """
        return self._props.get(PROP_PARENT_ID, '')

    def getProcessID(self):
        """Get process context ID.

        :returns: A |basestring| representing process context ID, or an empty
                  |basestring| if unknown.
        """
        return self._props.get(PROP_PROCESS_ID, '')

    def getName(self):
        """Get context name - if context represents a stack.

        :returns: A |basestring| representing this stack context name or
                  **None**.
        """
        return self._props.get(PROP_NAME, None)

    def getFrameAddress(self):
        """Get memory address of this frame.

        :returns: An |int| representing this frame address or **None** if not a
                  stack frame.
        """
        return self._props.get(PROP_FRAME_ADDRESS, None)

    def getReturnAddress(self):
        """Get program counter saved in this stack frame.

        This return address is the address of instruction to be executed when
        the function returns.

        :returns: An |int| representing the return address or **None** if not a
                  stack frame.
        """
        return self._props.get(PROP_RETURN_ADDRESS, None)

    def getInstructionAddress(self):
        """Get address of the next instruction to be executed in this stack
        frame.

        For top frame it is same as PC register value.

        For other frames it is same as return address of the next frame.

        :returns: An |int| representing this instruction address or **None** if
                  not a stack frame.
        """
        return self._props.get(PROP_INSTRUCTION_ADDRESS, None)

    def getArgumentsCount(self):
        """Get number of function arguments for this frame.

        :returns: An |int| reprsenting this stack function arguments count.
        """
        return self._props.get(PROP_ARGUMENTS_COUNT, 0)

    def getArgumentsAddress(self):
        """Get address of function arguments area in memory.

        :returns: An |int| representing this stack function arguments address
                  or **None** if not available.
        """
        return self._props.get(PROP_ARGUMENTS_ADDRESS, None)

    def getInlined(self):
        """Get inlined function level.

        :returns: An |int| representing the inlined function level, or
                  **None**.
        """
        return self._props.get(PROP_INLINED, None)

    def getFuncID(self):
        """Get function symbol ID.

        If **None**, client should use Symbols service to find function
        symbol ID.

        :returns: A |basestring| representing function symbol ID, or an empty
                  |basestring| if unknown.
        """
        return self._props.get(PROP_FUNC_ID, '')

    def getCodeArea(self):
        """Get code area context.

        Get code area that describes source code location of the frame.
        If **None**, client should use LineNumbers service to find frame source
        location.

        :returns: A |list| of |CodeArea| objects. representing this stack code
                  area or **None** if not available.
        """
        if self._props.get(PROP_CODE_AREA, None):
            return _toCodeAreaArray((self._props.get(PROP_CODE_AREA, None),))
        return None

    def getProperties(self):
        """Get complete map of context properties.

        :returns: A |dict| of context properties. See `Properties`_.
        """
        return self._props

    def isTopFrame(self):
        """Check if this stack frame is the top frame.

        :returns: A |bool| set to **True** if this stack is the toplevel
                  stack frame, **False** else.
        """
        return self._props.get(PROP_TOP_FRAME, False)
