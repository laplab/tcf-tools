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

"""Registers service provides access to target CPU register values and
properties.

.. |canSearch| replace:: :meth:`RegisterContext.canSearch`
.. |get| replace:: :meth:`RegisterContext.get`
.. |getChildren| replace:: :meth:`RegistersService.getChildren`
.. |getContext| replace:: :meth:`RegistersService.getContext`
.. |getFirstBitNumber| replace:: :meth:`RegisterContext.getFirstBitNumber`
.. |getm| replace:: :meth:`RegisterContext.getm`
.. |getRole| replace:: :meth:`RegisterContext.getRole`
.. |search| replace:: :meth:`RegistersService.search`
.. |set| replace:: :meth:`RegisterContext.set`
.. |setm| replace:: :meth:`RegisterContext.setm`
.. |DoneGet| replace:: :class:`DoneGet`
.. |DoneGetChildren| replace:: :class:`DoneGetChildren`
.. |DoneGetContext| replace:: :class:`DoneGetContext`
.. |DoneSearch| replace:: :class:`DoneSearch`
.. |DoneSet| replace:: :class:`DoneSet`
.. |Location| replace:: :class:`Location`
.. |NamedValue| replace:: :class:`NamedValue`
.. |RegistersContext| replace:: :class:`RegistersContext`
.. |RegistersListener| replace:: :class:`RegistersListener`

Properties
----------
Register Context Properties
^^^^^^^^^^^^^^^^^^^^^^^^^^^

See |RegistersContext|

+---------------------+--------------+----------------------------------------+
| Name                | Type         | Description                            |
+=====================+==============+========================================+
| PROP_BIG_ENDIAN     | |bool|       | **True** if big endian.                |
+---------------------+--------------+----------------------------------------+
| PROP_BITS           | |int|        | If context is a bit field, contains the|
|                     |              | field bit numbers in the parent        |
|                     |              | context.                               |
+---------------------+--------------+----------------------------------------+
| PROP_CAN_SEARCH     | |list|       | A list of attribute names which can be |
|                     |              | searched for starting on this context. |
|                     |              | See `Register Search Properties`_.     |
+---------------------+--------------+----------------------------------------+
| PROP_DESCRIPTION    | |basestring| | Context description.                   |
+---------------------+--------------+----------------------------------------+
| PROP_FIRST_BIT      | |int|        | Bit numbering base (0 or 1) to use when|
|                     |              | showing bits to user.                  |
+---------------------+--------------+----------------------------------------+
| PROP_FLOAT          | |bool|       | **True** if the register value is a    |
|                     |              | floating-point value.                  |
+---------------------+--------------+----------------------------------------+
| PROP_ID             | |basestring| | ID of the context.                     |
+---------------------+--------------+----------------------------------------+
| PROP_LEFT_TO_RIGHT  | |bool|       | **True** if the lowest numbered bit    |
|                     |              | should be shown to user as the         |
|                     |              | left-most bit.                         |
+---------------------+--------------+----------------------------------------+
| PROP_MEMORY_ADDRESS | |int|        | The address of a memory mapped         |
|                     |              | register.                              |
+---------------------+--------------+----------------------------------------+
| PROP_MEMORY_CONTEXT | |basestring| | The context ID of a memory context in  |
|                     |              | which a memory mapped register is      |
|                     |              | located.                               |
+---------------------+--------------+----------------------------------------+
| PROP_NAME           | |basestring| | Context name.                          |
+---------------------+--------------+----------------------------------------+
| PROP_OFFSET         | |int|        | When present describes the offset in   |
|                     |              | the data of the parent register where  |
|                     |              | the value of a field can be found.     |
+---------------------+--------------+----------------------------------------+
| PROP_PARENT_ID      | |basestring| | ID of a parent context.                |
+---------------------+--------------+----------------------------------------+
| PROP_PROCESS_ID     | |basestring| | Process ID.                            |
+---------------------+--------------+----------------------------------------+
| PROP_READBLE        | |bool|       | **True** if context value can be read. |
+---------------------+--------------+----------------------------------------+
| PROP_READ_ONCE      | |bool|       | **True** if reading the context        |
|                     |              | (register) destroys its current value. |
+---------------------+--------------+----------------------------------------+
| PROP_ROLE           | |basestring| | The role the register plays in a       |
|                     |              | program execution. See                 |
|                     |              | `Register Role Properties`_.           |
+---------------------+--------------+----------------------------------------+
| PROP_SIDE_EFFECTS   | |bool|       | **True** if writing the context can    |
|                     |              | change values of other registers.      |
+---------------------+--------------+----------------------------------------+
| PROP_SIZE           | |int|        | Context size in bytes. Byte arrays in  |
|                     |              | get/set commands should be same size.  |
+---------------------+--------------+----------------------------------------+
| PROP_VALUES         | |dict|       | Predefined names (mnemonics) for some  |
|                     |              | of context values.                     |
+---------------------+--------------+----------------------------------------+
| PROP_VOLATILE       | |bool|       | **True** if the register value can     |
|                     |              | change even when target is stopped.    |
+---------------------+--------------+----------------------------------------+
| PROP_WRITEABLE      | |bool|       | **True** if context value can be       |
|                     |              | written.                               |
+---------------------+--------------+----------------------------------------+
| PROP_WRITE_ONCE     | |bool|       | **True** if register value can not be  |
|                     |              | overwritten - every write counts.      |
+---------------------+--------------+----------------------------------------+

.. _Tcf-Register-Role-Properties:

Register Role Properties
^^^^^^^^^^^^^^^^^^^^^^^^
All register roles are of type |basestring|.

.. seealso:: |getRole|

+-----------+-----------------------------------------------------------------+
| Name      | Description                                                     |
+===========+=================================================================+
| ROLE_CORE | Indicates register or register groups which belong to the core  |
|           | state.                                                          |
+-----------+-----------------------------------------------------------------+
| ROLE_FP   | Register defining the current frame pointer location.           |
+-----------+-----------------------------------------------------------------+
| ROLE_PC   | Program counter. Defines instruction to execute next.           |
+-----------+-----------------------------------------------------------------+
| ROLE_RET  | Register used to store the return address for calls.            |
+-----------+-----------------------------------------------------------------+
| ROLE_SP   | Register defining the current stack pointer location.           |
+-----------+-----------------------------------------------------------------+

Register Search Properties
^^^^^^^^^^^^^^^^^^^^^^^^^^
All register search properties are of type |basestring|.

.. seealso:: |canSearch|

+--------------------+--------------------------------------------------------+
| Name               | Description                                            |
+====================+========================================================+
| SEARCH_EQUAL_VALUE | The value which is searched for. This should be a      |
|                    | |basestring| of packed binary data. Array size should  |
|                    | match the size of the register.  See |struct| module.  |
+--------------------+--------------------------------------------------------+
| SEARCH_NAME        | The name of the property this filter applies to.       |
+--------------------+--------------------------------------------------------+

Service Methods
---------------
.. autodata:: NAME
.. autoclass:: RegistersService

addListener
^^^^^^^^^^^
.. automethod:: RegistersService.addListener

getChildren
^^^^^^^^^^^
.. automethod:: RegistersService.getChildren

getContext
^^^^^^^^^^
.. automethod:: RegistersService.getContext

getName
^^^^^^^
.. automethod:: RegistersService.getName

getm
^^^^
.. automethod:: RegistersService.getm

removeListener
^^^^^^^^^^^^^^
.. automethod:: RegistersService.removeListener

setm
^^^^
.. automethod:: RegistersService.setm

Callback Classes
----------------
DoneGet
^^^^^^^
.. autoclass:: DoneGet
    :members:

DoneGetChildren
^^^^^^^^^^^^^^^
.. autoclass:: DoneGetChildren
    :members:

DoneGetContext
^^^^^^^^^^^^^^
.. autoclass:: DoneGetContext
    :members:

DoneSearch
^^^^^^^^^^
.. autoclass:: DoneSearch
    :members:

DoneSet
^^^^^^^
.. autoclass:: DoneSet
    :members:

Listener
--------
.. autoclass:: RegistersListener
    :members:

Helper Classes
--------------
Location
^^^^^^^^
.. autoclass:: Location
    :members:

NamedValue
^^^^^^^^^^
.. autoclass:: NamedValue
    :members:

RegistersContext
^^^^^^^^^^^^^^^^
.. autoclass:: RegistersContext
    :members:
"""

from .. import services

NAME = "Registers"
"""Registers service name."""

# Registers Context Properties

PROP_ID = "ID"
PROP_PARENT_ID = "ParentID"
PROP_PROCESS_ID = "ProcessID"
PROP_NAME = "Name"
PROP_DESCRIPTION = "Description"
PROP_SIZE = "Size"
PROP_READBLE = "Readable"
PROP_READ_ONCE = "ReadOnce"
PROP_WRITEABLE = "Writeable"
PROP_WRITE_ONCE = "WriteOnce"
PROP_SIDE_EFFECTS = "SideEffects"
PROP_VOLATILE = "Volatile"
PROP_FLOAT = "Float"
PROP_BIG_ENDIAN = "BigEndian"
PROP_LEFT_TO_RIGHT = "LeftToRight"
PROP_FIRST_BIT = "FirstBit"
PROP_BITS = "Bits"
PROP_VALUES = "Values"
PROP_MEMORY_ADDRESS = "MemoryAddress"
PROP_MEMORY_CONTEXT = "MemoryContext"
PROP_CAN_SEARCH = "CanSearch"
PROP_ROLE = "Role"
PROP_OFFSET = "Offset"

# Registers Role Properties

ROLE_PC = "PC"
ROLE_SP = "SP"
ROLE_FP = "FP"
ROLE_RET = "RET"
ROLE_CORE = "CORE"

# Registers Search Properties

SEARCH_NAME = "Name"
SEARCH_EQUAL_VALUE = "EqualValue"


class RegistersContext(object):
    """RegistersContext objects represent register groups, registers and bit
    fields.

    Register contexts are initialised with the properties described at
    `Register Context Properties`_.

    :param properties: The properties to initialise this register context with.
    :type properties: |dict|

    .. seealso:: `Register Context Properties`_
    """
    def __init__(self, props):
        self._props = props or {}

    def __str__(self):
        return "[Registers Context %s]" % self._props

    def getProperties(self):
        """Get context properties.

        See `Register Context Properties`_  definitions for property names.
        Context properties are read only, clients should not try to modify
        them.

        :returns: A |dict| of register context properties.

        .. seealso:: `Register Context Properties`_
        """
        return self._props

    def getID(self):
        """Get register TCF context ID.

        :returns: A |basestring| representing this register context ID.
        """
        return self._props.get(PROP_ID)

    def getParentID(self):
        """Get parent context ID.

        :returns: A |basestring| representing this register parent context ID
                  or **None**.
        """
        return self._props.get(PROP_PARENT_ID)

    def getProcessID(self):
        """Get process ID, if applicable.

        :returns: A |basestring| representing this register context process ID
                  or **None**.
        """
        return self._props.get(PROP_PROCESS_ID)

    def getName(self):
        """Get context (register, register group, bit field) name.

        :returns: A |basestring| representing this register context name or
                  **None**.
        """
        return self._props.get(PROP_NAME)

    def getDescription(self):
        """Get context description.

        :returns: A |basestring| representing this register context
                  description or **None**.
        """
        return self._props.get(PROP_DESCRIPTION)

    def getSize(self):
        """Get context size in bytes.

        Byte arrays in |get|/|set| methods should be same size.

        Hardware register can be smaller than this size, for example in case
        when register size is not an even number of bytes. In such case
        implementation should add/remove padding that consists of necessary
        number of zero bits.

        :returns: An |int| representing this register context size in bytes or
                 **0**.
        """
        return self._props.get(PROP_SIZE, 0)

    def isReadable(self):
        """Check if context value can be read.

        :returns: A |bool| set to **True** if the register context value can be
                  read.
        """
        return self._props.get(PROP_READBLE)

    def isReadOnce(self):
        """Check if reading the context (register) destroys its current value -
         it can be read only once.

        :returns: A |bool| set to **True** if the register context value can be
                  read only once.
        """
        return self._props.get(PROP_READ_ONCE)

    def isWriteable(self):
        """Check if context value can be written.

        :returns: A |bool| set to **True** if the register context value can be
                  written.
        """
        return self._props.get(PROP_WRITEABLE)

    def isWriteOnce(self):
        """Check if register value can not be overwritten - every write counts.

        :returns: A |bool| set to **True** if the register context value can be
                  written only once.
        """
        return self._props.get(PROP_WRITE_ONCE)

    def hasSideEffects(self):
        """Check if writing the context can change values of other registers.

        :returns: A |bool| set to **True** if writting the register context
                  value can change values of other registers.
        """
        return self._props.get(PROP_SIDE_EFFECTS)

    def isVolatile(self):
        """Check if the register value can change even when target is stopped.

        :returns: A |bool| set to **True** if the register value can change at
                  any time.
        """
        return self._props.get(PROP_VOLATILE)

    def isFloat(self):
        """Check if the register value is a floating-point value.

        :returns: A |bool| set to **True** if this register context reprsents a
                  floating-point register.
        """
        return self._props.get(PROP_FLOAT)

    def isBigEndian(self):
        """Check endianness of the context.

        Big endian means decreasing numeric significance with increasing bit
        number.

        The endianness is used to encode and decode values of |get|, |getm|,
        |set| and |setm| commands.

        :returns: A |bool| set to **True** if this register endianness is big.
        """
        return self._props.get(PROP_BIG_ENDIAN)

    def isLeftToRight(self):
        """Check if the lowest numbered bit (i.e. bit #0 or bit #1 depending on
        |getFirstBitNumber| value) should be shown to user as the left-most bit
        or the right-most bit.

        :returns: A |bool| set to **True** if the first bit is left-most bit.
        """
        return self._props.get(PROP_LEFT_TO_RIGHT)

    def getFirstBitNumber(self):
        """If the context has bit field children, bit positions of the fields
        can be zero-based or 1-based.

        :returns: An |int| representing this register first bit position -
                  **0** or **1**.
        """
        return self._props.get(PROP_FIRST_BIT, 0)

    def getBitNumbers(self):
        """If context is a bit field, get the field bit numbers in parent
        context.

        :returns: A |list| of  of bit numbers.
        """
        return self._props.get(PROP_BITS)

    def getNamedValues(self):
        """A context can have predefined names (mnemonics) for some of its
        values.

        This method returns a list of such named values.

        :returns: A |list| of |NamedValue| objects or **None**.
        """
        return self._props.get(PROP_VALUES)

    def getMemoryAddress(self):
        """Get the address of a memory mapped register.

        :returns: An |int| representing this register's memory mapped address
                  or **None**.
        """
        return self._props.get(PROP_MEMORY_ADDRESS)

    def getMemoryContext(self):
        """Get the context ID of a memory context in which a memory mapped
        register is located.

        :returns: A |basestring| representing this register's memory context
                  ID or **None**.
        """
        return self._props.get(PROP_MEMORY_CONTEXT)

    def canSearch(self):
        """Get a list of property names which can be searched for starting on
        this context.

        :returns: A |list| of property names.

        .. seealso:: `Register Search Properties`_
        """
        return self._props.get(PROP_CAN_SEARCH)

    def getRole(self):
        """Get the role the register plays in a program execution.

        :returns: A |basestring| representing this register context role name
                  or **None**.

        .. seealso:: `Register Role Properties`_
        """
        return self._props.get(PROP_ROLE)

    def getOffset(self):
        """Get the offset in the data of the parent register where the value
        of a field can be found.

        :returns: An |int| representing this register offset in parent
                  register or **None**.
        """
        return self._props.get(PROP_OFFSET)

    def get(self, done):
        """Read value of the context.

        :param done: Call back interface called when operation is completed.
        :type done: |DoneGet|

        :returns: Pending command handle, can be used to cancel the command.
        """
        raise NotImplementedError("Abstract method")

    def set(self, value, done):  # @ReservedAssignment
        """Set value of the context.

        :param value: An array of packed binary data. Array size should match
                      the size of the register. See |struct| module.
        :type value: |basestring|
        :param done: Call back interface called when operation is completed.
        :type done: |DoneSet|

        :returns: Pending command handle, can be used to cancel the command.
        """
        raise NotImplementedError("Abstract method")

    def search(self, filterProps, done):
        """Search register contexts that passes given search filter.

        Search is only supported for properties listed by the |canSearch|
        method.

        :param filterProps: Dictionary of properties to search for.
        :type filterProps: |dict|
        :param done: Call back interface called when operation is completed.
        :type done: |DoneSearch|

        :returns: Pending command handle, can be used to cancel the command.

        .. seealso:: `Register Search Properties`_
        """
        raise NotImplementedError("Abstract method")


class RegistersService(services.Service):
    def getName(self):
        """Get this service name.

        :returns: A |basestring| representing this service name, which is the
                  value of :const:`NAME`
        """
        return NAME

    def getContext(self, contextID, done):
        """Retrieve context info for given context ID.

        :param contextID: TCF ID of the register to retrieve.
        :type contextID: |basestring|
        :param done: Call back interface called when operation is completed.
        :type done: |DoneGetContext|

        :returns: Pending command handle, can be used to cancel the command.
        """
        raise NotImplementedError("Abstract method")

    def getChildren(self, parent_context_id, done):
        """Retrieve contexts available for registers commands.

        A context corresponds to an execution thread, stack frame, registers
        group, etc...

        A context can belong to a parent context. Contexts hierarchy can be
        simple plain list or it can form a tree. It is up to target agent
        developers to choose layout that is most descriptive for a given
        target. Context IDs are valid across all services. In other words, all
        services access same hierarchy of contexts, with same IDs, however,
        each service accesses its own subset of context's attributes and
        functionality, which is relevant to that service.

        :param parent_context_id: parent context ID. Can be **None**.
                                  :note: to retrieve top level of the
                                  hierarchy, or one of context IDs retrieved by
                                  previous |getChildren| commands.
        :type parent_context_id: |basestring| or **None**
        :param done: Call back interface called when operation is completed.
        :type done: |DoneGetChildren|

        :returns: Pending command handle, can be used to cancel the command.
        """
        raise NotImplementedError("Abstract method")

    def getm(self, locs, done):
        """Read values of multiple locations in registers.

        :param locs: List of data |Location|.
        :type locs: |list| or |tuple|
        :param done: Call back interface called when operation is completed.
        :type done: |DoneGet|

        :returns: Pending command handle, can be used to cancel the command.
        """
        raise NotImplementedError("Abstract method")

    def setm(self, locs, value, done):
        """Set values of multiple locations in registers.

        :param locs: List of data |Location|.
        :type locs: |list| or |tuple|
        :param value: An array of packed binary data. Array size should match
                      the size of the register. See |struct| module.
        :type value: |basestring|
        :param done: Call back interface called when operation is completed.
        :type done: |DoneSet|

        :returns: Pending command handle, can be used to cancel the command.
        """
        raise NotImplementedError("Abstract method")

    def addListener(self, listener):
        """Add registers service event listener.

        :param listener: Register event listener implementation to add this
                         service.
        :type listener: |RegistersListener|
        """
        raise NotImplementedError("Abstract method")

    def removeListener(self, listener):
        """Remove registers service event listener.

        :param listener: Register event listener implementation to remove from
                         this service.
        :type listener: |RegistersListener|
        """
        raise NotImplementedError("Abstract method")


class NamedValue(object):
    """A register context can have predefined names (mnemonics) for some its
    values.

    NamedValue objects represent such values.

    :param value: A |basestring| of packed binary data. Array size should match
                  the size of the register. See |struct| module.
    :type value: |basestring|
    :param name: Register named value name.
    :type name: |basestring|
    :param description: Register named value description.
    :type description: |basestring|
    """
    def __init__(self, value, name, description):
        self.value = value
        self.name = name
        self.description = description

    def getValue(self):
        """Get value associated with the name.

        :returns: A |basestring| of packed binary data. Array size should match
                  the size of the register. See |struct| module.
        """
        return self.value

    def getName(self):
        """Get name (mnemonic) of the value.

        :returns: A |basestring| representing this register named value name.
        """
        return self.name

    def getDescription(self):
        """Get human readable description of the value.

        :returns: A |basestring| representing this register named value
                  description.
        """
        return self.description


class DoneGet(object):
    """Client call back interface for |get| or |getm|."""
    def doneGet(self, token, error, value):
        """Called when value retrieval is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param value: A |basestring| of packed binary data. Array size should
                      match the size of the register. See |struct| module.
        :type value: |basestring|
        """
        pass


class DoneSet(object):
    """Client call back interface for |set| or |setm|.
    """
    def doneSet(self, token, error):
        """Called when value setting is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        """
        pass


class DoneSearch(object):
    """Client call back interface for |search|.
    """
    def doneSearch(self, token, error, paths):
        """Called when context search is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param paths: List of paths to each context with properties matching
                      the filter.
        :type paths: |list| or |tuple|
        """
        pass


class DoneGetContext(object):
    """Client call back interface for |getContext|."""
    def doneGetContext(self, token, error, context):
        """Called when context data retrieval is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param context: The so retrieved register context.
        :type context: |RegistersContext|
        """
        pass


class DoneGetChildren(object):
    """Client call back interface for :meth:`~RegistersService.getChildren`
    """
    def doneGetChildren(self, token, error, context_ids):
        """Called when context list retrieval is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param context_ids: A list of available context IDs.
        :type context_ids: |list| or |tuple|
        """
        pass


class RegistersListener(object):
    """Registers event listener is notified when registers context hierarchy
    changes, and when a register is modified by the service commands.
    """

    def contextChanged(self):
        """Called when register context properties changed.

        Most targets have static set of registers and register properties.
        Such targets never generate this event. However, some targets,
        for example, JTAG probes, allow user to modify register definitions.
        Clients should flush all cached register context data.
        """
        pass

    def registerChanged(self, contextID):
        """Called when register content was changed and clients need to update
        themselves.

        Clients, at least, should invalidate corresponding cached registers
        data.

        Not every change is notified - it is not possible, only those, which
        are not caused by normal execution of the debuggee.

        At least, changes caused by |set| command should be notified.

        :param contextID: ID of the changed register.
        :type contextID: |basestring|
        """
        pass


class Location(object):
    """Class Location represents value location in register context.

    :param contextID: Register context ID.
    :type contextID: |basestring|
    :param offs: Offset in the context, in bytes.
    :type offs: |int|
    :param size: Value size in bytes.
    :type size: |int|
    """
    def __init__(self, contextID, offs, size):
        self._id = contextID
        self._offs = offs
        self._size = size

    def __iter__(self):
        yield self._id
        yield self._offs
        yield self._size

    @property
    def id(self):
        """Register location ID."""
        return self._id

    @property
    def offs(self):
        """Register location offset."""
        return self._offs

    @property
    def size(self):
        """Register location size."""
        return self._size
