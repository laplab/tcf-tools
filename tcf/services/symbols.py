# *****************************************************************************
# * Copyright (c) 2011, 2014-2016 Wind River Systems, Inc. and others.
# * All rights reserved. This program and the accompanying materials
# * are made available under the terms of the Eclipse Public License 2.0
# * which accompanies this distribution, and is available at
# * https://www.eclipse.org/legal/epl-2.0/
# *
# * Contributors:
# *     Wind River Systems - initial API and implementation
# *****************************************************************************

"""TCF symbols service interface.

.. |find| replace:: :meth:`~SymbolsService.find`
.. |findByAddr| replace:: :meth:`~SymbolsService.findByAddr`
.. |findByName| replace:: :meth:`~SymbolsService.findByName`
.. |findFrameInfo| replace:: :meth:`~SymbolsService.findFrameInfo`
.. |findInScope| replace:: :meth:`~SymbolsService.findInScope`
.. |getArrayType| replace:: :meth:`~SymbolsService.getArrayType`
.. |getChildren| replace:: :meth:`~SymbolsService.getChildren`
.. |getContext| replace:: :meth:`~SymbolsService.getContext`
.. |getFlags| replace:: :meth:`~Symbol.getFlags`
.. |getID| replace:: :meth:`~Symbol.getID`
.. |getLocationInfo| replace:: :meth:`~SymbolsService.getLocationInfo`
.. |getName| replace:: :meth:`~SymbolsService.getName`
.. |getProperties| replace:: :meth:`~Symbol.getProperties`
.. |getSymFileInfo| replace:: :meth:`~SymbolsService.getSymFileInfo`
.. |getUpdatePolicy| replace:: :meth:`~Symbol.getUpdatePolicy`
.. |DoneFind| replace:: :class:`DoneFind`
.. |DoneFindFrameInfo| replace:: :class:`DoneFindFrameInfo`
.. |DoneGetArrayType| replace:: :class:`DoneGetArrayType`
.. |DoneGetChildren| replace:: :class:`DoneGetChildren`
.. |DoneGetContext| replace:: :class:`DoneGetContext`
.. |DoneGetLocationInfo| replace:: :class:`DoneGetLocationInfo`
.. |DoneGetSymFileInfo| replace:: :class:`DoneGetSymFileInfo`
.. |DoneList| replace:: :class:`DoneList`
.. |Symbol.getFlags| replace:: :meth:`Symbol.getFlags`
.. |Symbol.getProperties| replace:: :meth:`Symbol.getProperties`
.. |Symbol.getUpdatePolicy| replace:: :meth:`Symbol.getUpdatePolicy`
.. |Symbol| replace:: :class:`Symbol`
.. |SymbolClass| replace:: :class:`SymbolClass`
.. |SymbolsService.list| replace:: :meth:`~SymbolsService.list`
.. |TypeClass| replace:: :class:`TypeClass`

Properties
----------
Symbol Context Properties
^^^^^^^^^^^^^^^^^^^^^^^^^

.. seealso:: |Symbol|, |Symbol.getProperties|

+--------------------+--------------+-----------------------------------------+
| Name               | Type         | Description                             |
+====================+==============+=========================================+
| PROP_ADDRESS       | |int|        | Symbol address in symbol's memory       |
|                    |              | space.                                  |
+--------------------+--------------+-----------------------------------------+
| PROP_BASE_TYPE_ID  | |basestring| | ID of the symbol base type. It is       |
|                    |              | possible to get the base type symbols   |
|                    |              | by calling |getContext| on this ID.     |
+--------------------+--------------+-----------------------------------------+
| PROP_BIG_ENDIAN    | |bool|       | **True** if symbol's value is big       |
|                    |              | endian.                                 |
+--------------------+--------------+-----------------------------------------+
| PROP_BIT_STRIDE    | |int|        | Symbol's bit stride (if any).           |
+--------------------+--------------+-----------------------------------------+
| PROP_CONTAINER_ID  | |basestring| | ID of the symbol containing this symbol.|
+--------------------+--------------+-----------------------------------------+
| PROP_FLAGS         | |int|        | Symbol flags. See                       |
|                    |              | `Symbol Flags Properties`_.             |
+--------------------+--------------+-----------------------------------------+
| PROP_FRAME         | |int|        | Symbol frame index.                     |
+--------------------+--------------+-----------------------------------------+
| PROP_ID            | |basestring| | Symbol's unique TCF ID.                 |
+--------------------+--------------+-----------------------------------------+
| PROP_INDEX_TYPE_ID | |basestring| | Index type ID.                          |
+--------------------+--------------+-----------------------------------------+
| PROP_LENGTH        | |int|        | Symbol length (if applicable)           |
+--------------------+--------------+-----------------------------------------+
| PROP_LOC_ENT_OFFSET| |int|        | Symbol local entry point offset.        |
+--------------------+--------------+-----------------------------------------+
| PROP_LOWER_BOUND   | |int|        | Symbol's lower bound in memory.         |
+--------------------+--------------+-----------------------------------------+
| PROP_NAME          | |basestring| | Symbol's name.                          |
+--------------------+--------------+-----------------------------------------+
| PROP_OFFSET        | |int|        | Symbol's offset (if any).               |
+--------------------+--------------+-----------------------------------------+
| PROP_OWNER_ID      | |basestring| | Symbol's Owner TCF ID.                  |
+--------------------+--------------+-----------------------------------------+
| PROP_REGISTER      | |bool|       | **True** if symbol is stored in a       |
|                    |              | register.                               |
+--------------------+--------------+-----------------------------------------+
| PROP_SIZE          | |int|        | Symbol size in bytes.                   |
+--------------------+--------------+-----------------------------------------+
| PROP_SYMBOL_CLASS  | |int|        | Symbol's symbol class (see              |
|                    |              | |SymbolClass|)                          |
+--------------------+--------------+-----------------------------------------+
| PROP_TYPE_CLASS    | |int|        | Symbol's type class (see |TypeClass|)   |
+--------------------+--------------+-----------------------------------------+
| PROP_TYPE_ID       | |basestring| | Type TCF ID.                            |
+--------------------+--------------+-----------------------------------------+
| PROP_UPDATE_POLICY | |int|        | Update policy. See                      |
|                    |              | `Symbol Update Policy Properties`_.     |
+--------------------+--------------+-----------------------------------------+
| PROP_UPPER_BOUND   | |int|        | Symbols' upper bound address.           |
+--------------------+--------------+-----------------------------------------+
| PROP_VALUE         | |bytearray|  | Symbol value (if any)                   |
+--------------------+--------------+-----------------------------------------+

Symbol Flags Properties
^^^^^^^^^^^^^^^^^^^^^^^
All symbol flags are of type |int|.

.. seealso:: |Symbol.getFlags|

+-------------------------+--------------------------------+
| Name                    | Description                    |
+=========================+================================+
| SYM_FLAG_ARTIFICIAL     | Symbol is artificial.          |
+-------------------------+--------------------------------+
| SYM_FLAG_BIG_ENDIAN     | Symbol is big endian.          |
+-------------------------+--------------------------------+
| SYM_FLAG_BOOL_TYPE      | Symbol is a boolean.           |
+-------------------------+--------------------------------+
| SYM_FLAG_CLASS_TYPE     | Symbol is a class type symbol. |
+-------------------------+--------------------------------+
| SYM_FLAG_CONST_TYPE     | Symbol is a constant.          |
+-------------------------+--------------------------------+
| SYM_FLAG_ENUM_TYPE      | Symbol is an enum.             |
+-------------------------+--------------------------------+
| SYM_FLAG_EXTERNAL       | Symbol is external.            |
+-------------------------+--------------------------------+
| SYM_FLAG_INDIRECT       | Symbol is a data indirection.  |
+-------------------------+--------------------------------+
| SYM_FLAG_INHERITANCE    | Symbol is a base class.        |
+-------------------------+--------------------------------+
| SYM_FLAG_INTERFACE_TYPE | Symbol is an interface.        |
+-------------------------+--------------------------------+
| SYM_FLAG_LITTLE_ENDIAN  | Symbol is little endian.       |
+-------------------------+--------------------------------+
| SYM_FLAG_OPTIONAL       | Symbol is optional.            |
+-------------------------+--------------------------------+
| SYM_FLAG_PACKET_TYPE    | Symbol is a packet type.       |
+-------------------------+--------------------------------+
| SYM_FLAG_PARAMETER      | Symbol is a parameter.         |
+-------------------------+--------------------------------+
| SYM_FLAG_PRIVATE        | Symbol is private.             |
+-------------------------+--------------------------------+
| SYM_FLAG_PROTECTED      | Symbol is protected.           |
+-------------------------+--------------------------------+
| SYM_FLAG_PUBLIC         | Symbol is public.              |
+-------------------------+--------------------------------+
| SYM_FLAG_REFERENCE      | Symbol is a reference.         |
+-------------------------+--------------------------------+
| SYM_FLAG_RESTRICT_TYPE  | Symbol is of restrict type.    |
+-------------------------+--------------------------------+
| SYM_FLAG_RVALUE         | Symbol is a rvalue reference.  |
+-------------------------+--------------------------------+
| SYM_FLAG_SHARED_TYPE    | Symbol is of shared type.      |
+-------------------------+--------------------------------+
| SYM_FLAG_STRUCT_TYPE    | Symbol is of structure type.   |
+-------------------------+--------------------------------+
| SYM_FLAG_STRING_TYPE    | Symbol is a string type.       |
+-------------------------+--------------------------------+
| SYM_FLAG_SUBRANGE_TYPE  | Symbol is of subrange type.    |
+-------------------------+--------------------------------+
| SYM_FLAG_TYPEDEF        | Symbol is a typedef.           |
+-------------------------+--------------------------------+
| SYM_FLAG_TYPE_PARAMETER | Symbol is a of parameter type. |
+-------------------------+--------------------------------+
| SYM_FLAG_UNION_TYPE     | Symbol is of union type.       |
+-------------------------+--------------------------------+
| SYM_FLAG_VARARG         | Symbol is a variable argument. |
+-------------------------+--------------------------------+
| SYM_FLAG_VOLATILE_TYPE  | Symbol is of volatile type.    |
+-------------------------+--------------------------------+

Symbol Update Policy Properties
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
All symbol policy properties are of type |int|.

.. seealso:: |Symbol.getUpdatePolicy|

+------------------------------+----------------------------------------------+
| Name                         | Description                                  |
+==============================+==============================================+
| UPDATE_ON_EXE_STATE_CHANGES  | Update policy *Memory Map*: symbol properties|
|                              | become invalid when memory map changes :     |
|                              | when modules are loaded or unloaded. Symbol  |
|                              | OwnerID indicates memory space (process) that|
|                              | is invalidation events source. Most static   |
|                              | variables and types have this update policy. |
+------------------------------+----------------------------------------------+
| UPDATE_ON_MEMORY_MAP_CHANGES | Update policy *Execution State*: symbol      |
|                              | properties become invalid when execution     |
|                              | state changes : a thread is suspended,       |
|                              | resumed or exited. Symbol OwnerID indicates  |
|                              | executable context (thread) that is          |
|                              | invalidation events source. Most stack (auto)|
|                              | variables have this update policy.           |
+------------------------------+----------------------------------------------+

Symbol Command Properties
^^^^^^^^^^^^^^^^^^^^^^^^^
All symbol command properties are of type |int|.

Command codes that are used to calculate frame pointer and register values
during stack tracing.

.. seealso:: |findFrameInfo|

+--------------+--------------------------------------------------------------+
| Name         | Description                                                  |
+==============+==============================================================+
| CMD_ADD      | Add two values on top of the evaluation stack.               |
+--------------+--------------------------------------------------------------+
| CMD_AND      | And two values on top of the evaluation stack.               |
+--------------+--------------------------------------------------------------+
| CMD_ARG      | Load expression argument to evaluation stack.                |
+--------------+--------------------------------------------------------------+
| CMD_DEREF    | **deprecated** : Read memory at address on the top of the    |
|              | evaluation stack.                                            |
|              | Command arguments are the value size (Number) and endianness |
|              | (Boolean, false - little-endian, true - big-endian).         |
+--------------+--------------------------------------------------------------+
| CMD_DIV      | Divide two values on top of the evaluation stack.            |
+--------------+--------------------------------------------------------------+
| CMD_FCALL    | Evaluate function call on top of the evaluation stack.       |
+--------------+--------------------------------------------------------------+
| CMD_FP       | Load frame address to the evaluation stack.                  |
+--------------+--------------------------------------------------------------+
| CMD_GE       | Compare two values on top of the evaluation stack (Greater or|
|              | Equal).                                                      |
+--------------+--------------------------------------------------------------+
| CMD_GT       | Compare two values on top of the evaluation stack (Greater)  |
+--------------+--------------------------------------------------------------+
| CMD_LE       | Compare two values on top of the evaluation stack (Lighter or|
|              | Equal).                                                      |
+--------------+--------------------------------------------------------------+
| CMD_LOCATION | Evaluate DWARF location expression. Command arguments are    |
|              | byte array of DWARF expression instructions and an object    |
|              | that contains evaluation parameters.                         |
+--------------+--------------------------------------------------------------+
| CMD_LT       | Compare two values on top of the evaluation stack (Lighter)  |
+--------------+--------------------------------------------------------------+
| CMD_MUL      | Multiply two values on top of the evaluation stack.          |
+--------------+--------------------------------------------------------------+
| CMD_NEG      | Negate a value on top of the evaluation stack.               |
+--------------+--------------------------------------------------------------+
| CMD_NUMBER   | Load a number to the evaluation stack. Command argument is   |
|              | the number.                                                  |
+--------------+--------------------------------------------------------------+
| CMD_OR       | Or two values on top of the evaluation stack.                |
+--------------+--------------------------------------------------------------+
| CMD_PIECE    | Value on top of the evaluation stack is in pieces.           |
+--------------+--------------------------------------------------------------+
| CMD_REGISTER | **deprecated** : Load a register value to the evaluation     |
|              | stack. Command argument is the register ID.                  |
+--------------+--------------------------------------------------------------+
| CMD_SHL      | Left shift value on top of the evaluation stack.             |
+--------------+--------------------------------------------------------------+
| CMD_SHR      | Right shift value on top of the evaluation stack.            |
+--------------+--------------------------------------------------------------+
| CMD_SUB      | Substract two values on top of the evaluation stack.         |
+--------------+--------------------------------------------------------------+
| CMD_WR_MEM   | Value on top of the stack is a Wind River Memory ID ???      |
+--------------+--------------------------------------------------------------+
| CMD_WR_REG   | Value on top of the stack is a Wind River Register ID ???    |
+--------------+--------------------------------------------------------------+
| CMD_XOR      | Xor value on top of the evaluation stack.                    |
+--------------+--------------------------------------------------------------+

Symbol Location Properties
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. seealso:: |getLocationInfo|

+------------------+--------+-------------------------------------------------+
| Name             | Type   | Description                                     |
+==================+========+=================================================+
| LOC_ARG_CNT      | |int|  | Number of argument required to execute location |
|                  |        | instructions.                                   |
+------------------+--------+-------------------------------------------------+
| LOC_CODE_ADDR    | |int|  | Start address of code range where the location  |
|                  |        | info is valid, or **None** if it is valid       |
|                  |        | everywhere.                                     |
+------------------+--------+-------------------------------------------------+
| LOC_CODE_SIZE    | |int|  | Size in bytes of code range where the location  |
|                  |        | info is valid, or **None** if it is valid       |
|                  |        | everywhere.                                     |
+------------------+--------+-------------------------------------------------+
| LOC_LENGTH_CMDS  | |list| | Instructions to compute dynamic array length    |
|                  |        | location.                                       |
+------------------+--------+-------------------------------------------------+
| LOC_VALUE_CMDS   | |list| | Instructions to compute object value location,  |
|                  |        | e.g. address, or offset, or register ID, etc... |
+------------------+--------+-------------------------------------------------+
| LOC_DISCRIMINANT | |list| | List of discriminant values for a variant.      |
|                  |        | Each element of the list is a |dict| with two   |
|                  |        | values, the lower bound 'X' and upper bound 'Y'.|
+------------------+--------+-------------------------------------------------+

Service Methods
---------------
.. autodata:: NAME
.. autoclass:: SymbolsService

find
^^^^
.. automethod:: SymbolsService.find

findByAddr
^^^^^^^^^^
.. automethod:: SymbolsService.findByAddr

findByName
^^^^^^^^^^
.. automethod:: SymbolsService.findByName

findFrameInfo
^^^^^^^^^^^^^
.. automethod:: SymbolsService.findFrameInfo

findInScope
^^^^^^^^^^^
.. automethod:: SymbolsService.findInScope

getArrayType
^^^^^^^^^^^^
.. automethod:: SymbolsService.getArrayType

getChildren
^^^^^^^^^^^
.. automethod:: SymbolsService.getChildren

getContext
^^^^^^^^^^
.. automethod:: SymbolsService.getContext

getLocationInfo
^^^^^^^^^^^^^^^
.. automethod:: SymbolsService.getLocationInfo

getName
^^^^^^^
.. automethod:: SymbolsService.getName

getSymFileInfo
^^^^^^^^^^^^^^
.. automethod:: SymbolsService.getSymFileInfo

list
^^^^
.. automethod:: SymbolsService.list

Callback Classes
----------------
DoneFind
^^^^^^^^
.. autoclass:: DoneFind
    :members:

DoneFindFrameInfo
^^^^^^^^^^^^^^^^^
.. autoclass:: DoneFindFrameInfo
    :members:

DoneGetArrayType
^^^^^^^^^^^^^^^^
.. autoclass:: DoneGetArrayType
    :members:

DoneGetChildren
^^^^^^^^^^^^^^^
.. autoclass:: DoneGetChildren
    :members:

DoneGetContext
^^^^^^^^^^^^^^
.. autoclass:: DoneGetContext
    :members:

DoneGetLocationInfo
^^^^^^^^^^^^^^^^^^^
.. autoclass:: DoneGetLocationInfo
    :members:

DoneGetSymFileInfo
^^^^^^^^^^^^^^^^^^
.. autoclass:: DoneGetSymFileInfo
    :members:

DoneList
^^^^^^^^
.. autoclass:: DoneList
    :members:

Helper Classes
--------------

.. _Tcf-Symbol:

Symbol
^^^^^^
.. autoclass:: Symbol
    :members:

.. _Tcf-Symbol-Class:

SymbolClass
^^^^^^^^^^^
.. autoclass:: SymbolClass

.. _Tcf-Symbol-Type-Class:

TypeClass
^^^^^^^^^
.. autoclass:: TypeClass
"""

from .. import services

NAME = "Symbols"
"""Symbols service name."""


class SymbolClass:
    """Symbol class values.


    This class allows to bind Symbol's class value to a type.

    .. code-block:: python

        import tcf.services.symbols as tcfsyms

        if symbol.getSymbolClass() is tcfsyms.TypeClass.function:
            # Print name + address
            print('{0} : 0x{1:016x}'.format(symbol.getName(),
                                            symbol.getAddress()))

    Here is the value/class association table:

    +-------+--------------+-----------------------------+
    | Value | Name         | Description                 |
    +=======+==============+=============================+
    | **0** | unknown      | Unknown symbol class.       |
    +-------+--------------+-----------------------------+
    | **1** | value        | Constant value.             |
    +-------+--------------+-----------------------------+
    | **2** | reference    | Variable data object.       |
    +-------+--------------+-----------------------------+
    | **3** | function     | Function body.              |
    +-------+--------------+-----------------------------+
    | **4** | type         | A type.                     |
    +-------+--------------+-----------------------------+
    | **5** | comp_unit    | A compilation unit.         |
    +-------+--------------+-----------------------------+
    | **6** | block        | A block of code.            |
    +-------+--------------+-----------------------------+
    | **7** | namespace    | A namespace.                |
    +-------+--------------+-----------------------------+
    | **8** | variant_part | A variant part.             |
    +-------+--------------+-----------------------------+
    | **9** | variant      | A member of a variant part. |
    +-------+--------------+-----------------------------+
    """
    unknown = 0
    value = 1
    reference = 2
    function = 3
    type = 4  # @ReservedAssignment
    comp_unit = 5
    block = 6
    namespace = 7
    variant_part = 8
    variant = 9


class TypeClass:
    """Type class values.

    This class allows to bind Symbol's type class value to a type.

    .. code-block:: python

        import tcf.services.symbols as tcfsyms

        if symbol.getTypeClass() is tcfsyms.TypeClass.pointer:
            # print it as a pointer
            print('{0} : 0x{1:016x}'.format(symbol.getName(),
                                            symbol.getAddress()))

    Here is the value/type association table:

    +--------+-------------+---------------------------+
    | Value  | Name        | Description               |
    +========+=============+===========================+
    | **0**  | unknown     | Unknown type class.       |
    +--------+-------------+---------------------------+
    | **1**  | cardinal    | Unsigned integer.         |
    +--------+-------------+---------------------------+
    | **2**  | integer     | Signed integer.           |
    +--------+-------------+---------------------------+
    | **3**  | real        | Float, double.            |
    +--------+-------------+---------------------------+
    | **4**  | pointer     | Pointer to anything.      |
    +--------+-------------+---------------------------+
    | **5**  | array       | Array of anything.        |
    +--------+-------------+---------------------------+
    | **6**  | composite   | Struct, union, or class.  |
    +--------+-------------+---------------------------+
    | **7**  | enumeration | Enumeration type.         |
    +--------+-------------+---------------------------+
    | **8**  | function    | Function type.            |
    +--------+-------------+---------------------------+
    | **9**  | member_ptr  | A pointer on member type. |
    +--------+-------------+---------------------------+
    | **10** | complex     | A complex type.           |
    +--------+-------------+---------------------------+
    """
    unknown = 0
    cardinal = 1
    integer = 2
    real = 3
    pointer = 4
    array = 5
    composite = 6
    enumeration = 7
    function = 8
    member_ptr = 9
    complex = 10

SYM_FLAG_PARAMETER = 0x0000001
SYM_FLAG_TYPEDEF = 0x0000002
SYM_FLAG_CONST_TYPE = 0x0000004
SYM_FLAG_PACKET_TYPE = 0x0000008
SYM_FLAG_SUBRANGE_TYPE = 0x0000010
SYM_FLAG_VOLATILE_TYPE = 0x0000020
SYM_FLAG_RESTRICT_TYPE = 0x0000040
SYM_FLAG_UNION_TYPE = 0x0000080
SYM_FLAG_CLASS_TYPE = 0x0000100
SYM_FLAG_INTERFACE_TYPE = 0x0000200
SYM_FLAG_SHARED_TYPE = 0x0000400
SYM_FLAG_REFERENCE = 0x0000800
SYM_FLAG_BIG_ENDIAN = 0x0001000
SYM_FLAG_LITTLE_ENDIAN = 0x0002000
SYM_FLAG_OPTIONAL = 0x0004000
SYM_FLAG_EXTERNAL = 0x0008000
SYM_FLAG_VARARG = 0x0010000
SYM_FLAG_ARTIFICIAL = 0x0020000
SYM_FLAG_TYPE_PARAMETER = 0x0040000
SYM_FLAG_PRIVATE = 0x0080000
SYM_FLAG_PROTECTED = 0x00100000
SYM_FLAG_PUBLIC = 0x00200000
SYM_FLAG_ENUM_TYPE = 0x00400000
SYM_FLAG_STRUCT_TYPE = 0x00800000
SYM_FLAG_STRING_TYPE = 0x01000000
SYM_FLAG_INHERITANCE = 0x02000000
SYM_FLAG_BOOL_TYPE = 0x04000000
SYM_FLAG_INDIRECT = 0x08000000
SYM_FLAG_RVALUE = 0x10000000

# Symbol context property names.

PROP_ID = "ID"
PROP_OWNER_ID = "OwnerID"
PROP_UPDATE_POLICY = "UpdatePolicy"
PROP_NAME = "Name"
PROP_SYMBOL_CLASS = "Class"
PROP_TYPE_CLASS = "TypeClass"
PROP_TYPE_ID = "TypeID"
PROP_BASE_TYPE_ID = "BaseTypeID"
PROP_INDEX_TYPE_ID = "IndexTypeID"
PROP_SIZE = "Size"
PROP_LENGTH = "Length"
PROP_LOWER_BOUND = "LowerBound"
PROP_UPPER_BOUND = "UpperBound"
PROP_OFFSET = "Offset"
PROP_ADDRESS = "Address"
PROP_VALUE = "Value"
PROP_BIG_ENDIAN = "BigEndian"
PROP_REGISTER = "Register"
PROP_FLAGS = "Flags"
PROP_CONTAINER_ID = "ContainerID"
PROP_FRAME = "Frame"
PROP_LOC_ENT_OFFSET = "LocalEntryOffset"
PROP_BIT_STRIDE = "BitStride"

# Symbol context properties update policies.

UPDATE_ON_MEMORY_MAP_CHANGES = 0
UPDATE_ON_EXE_STATE_CHANGES = 1

# Command codes that are used to calculate frame pointer and register values
# during stack tracing.

CMD_NUMBER = 1
CMD_FP = 3
CMD_ADD = 5
CMD_SUB = 6
CMD_MUL = 7
CMD_DIV = 8
CMD_AND = 9
CMD_OR = 10
CMD_XOR = 11
CMD_NEG = 12
CMD_GE = 13
CMD_GT = 14
CMD_LE = 15
CMD_LT = 16
CMD_SHL = 17
CMD_SHR = 18
CMD_ARG = 19
CMD_LOCATION = 20
CMD_FCALL = 21
CMD_WR_REG = 22
CMD_WR_MEM = 23
CMD_PIECE = 24

# Deprecated

CMD_REGISTER = 2
CMD_DEREF = 4

# Symbol location properties.

LOC_CODE_ADDR = "CodeAddr"
LOC_CODE_SIZE = "CodeSize"
LOC_ARG_CNT = "ArgCnt"
LOC_VALUE_CMDS = "ValueCmds"
LOC_LENGTH_CMDS = "LengthCmds"
LOC_DISCRIMINANT = "Discriminant"


class Symbol(object):
    """Symbol context interface.

    :param props: Properties to create this symbol with.
    :type props: |dict|

    .. seealso:: `Symbol Context Properties`_
    """
    def __init__(self, props):
        self._props = props or {}

    def __repr__(self):
        return self.__class__.__name__ + '(' + repr(self._props) + ')'

    def __str__(self):
        res = self.__class__.__name__ + ' ['
        for key in list(self._props.keys()):
            res += str(key) + '=' + str(self._props.get(key))
            if key == PROP_SYMBOL_CLASS:
                # Add a meaningful word here.
                value = self._props.get(key)
                for attr in dir(SymbolClass):
                    if getattr(SymbolClass, attr) == value:
                        res += '(' + attr + ')'
                        break
            if key == PROP_TYPE_CLASS:
                # Add a meaningful word here.
                value = self._props.get(key)
                for attr in dir(TypeClass):
                    if getattr(TypeClass, attr) == value:
                        res += '(' + attr + ')'
                        break
            if key == PROP_FLAGS and self._props.get(key) != 0:
                value = self._props.get(key)
                flags = []
                if value & SYM_FLAG_PARAMETER:
                    flags.append('PARAMETER')
                if value & SYM_FLAG_TYPEDEF:
                    flags.append('TYPEDEF')
                if value & SYM_FLAG_CONST_TYPE:
                    flags.append('CONST_TYPE')
                if value & SYM_FLAG_PACKET_TYPE:
                    flags.append('PACKET_TYPE')
                if value & SYM_FLAG_SUBRANGE_TYPE:
                    flags.append('SUBRANGE_TYPE')
                if value & SYM_FLAG_VOLATILE_TYPE:
                    flags.append('VOLATILE_TYPE')
                if value & SYM_FLAG_RESTRICT_TYPE:
                    flags.append('RESTRICT_TYPE')
                if value & SYM_FLAG_UNION_TYPE:
                    flags.append('UNION_TYPE')
                if value & SYM_FLAG_CLASS_TYPE:
                    flags.append('CLASS_TYPE')
                if value & SYM_FLAG_INTERFACE_TYPE:
                    flags.append('INTERFACE_TYPE')
                if value & SYM_FLAG_SHARED_TYPE:
                    flags.append('SHARED_TYPE')
                if value & SYM_FLAG_REFERENCE:
                    flags.append('REFERENCE')
                if value & SYM_FLAG_BIG_ENDIAN:
                    flags.append('BIG_ENDIAN')
                if value & SYM_FLAG_LITTLE_ENDIAN:
                    flags.append('LITTLE_ENDIAN')
                if value & SYM_FLAG_OPTIONAL:
                    flags.append('OPTIONAL')
                if value & SYM_FLAG_EXTERNAL:
                    flags.append('EXTERNAL')
                if value & SYM_FLAG_VARARG:
                    flags.append('VARARG')
                if value & SYM_FLAG_ARTIFICIAL:
                    flags.append('ARTIFICIAL')
                if value & SYM_FLAG_TYPE_PARAMETER:
                    flags.append('TYPE_PARAMETER')
                if value & SYM_FLAG_PRIVATE:
                    flags.append('PRIVATE')
                if value & SYM_FLAG_PROTECTED:
                    flags.append('PROTECTED')
                if value & SYM_FLAG_PUBLIC:
                    flags.append('PUBLIC')
                if value & SYM_FLAG_ENUM_TYPE:
                    flags.append('ENUM_TYPE')
                if value & SYM_FLAG_STRUCT_TYPE:
                    flags.append('STRUCT_TYPE')
                if value & SYM_FLAG_STRING_TYPE:
                    flags.append('STRING_TYPE')
                if value & SYM_FLAG_INHERITANCE:
                    flags.append('INHERITANCE')
                if value & SYM_FLAG_BOOL_TYPE:
                    flags.append('BOOL_TYPE')
                res += '(' + '|'.join(flags) + ')'
            res += ', '
        res = res.rstrip(', ')
        res += ']'
        return res

    def getID(self):
        """Get symbol ID.

        :returns: A |basestring| representing this symbol's unique TCF ID.
        """
        return self._props.get(PROP_ID)

    def getFrame(self):
        """Get symbol frame index.

        :returns: A |int| representing frame index (from top stack frame), or
                  **None** if the symbol is not defined in a frame.
        """
        return self._props.get(PROP_FRAME, None)

    def getOwnerID(self):
        """Get symbol owner ID.

        The owner can a thread or memory space (process).

        Certain changes in owner state can invalidate cached symbol properties,
        see |getUpdatePolicy| and `Symbol Update Policy Properties`_.

        :returns: A |basestring| representing this symbol's owner ID, or
                  **None** if unknown.
        """
        return self._props.get(PROP_OWNER_ID)

    def getUpdatePolicy(self):
        """Get symbol properties update policy ID.

        Symbol properties can change during program execution.

        If a client wants to cache symbols, it should invalidate cached data
        according to update policies of cached symbols.

        :returns: An |int| representing this symbol update policy, see
                  `Symbol Update Policy Properties`_.
        """
        return self._props.get(PROP_UPDATE_POLICY)

    def getName(self):
        """Get this symbol name.

        :returns: A |basestring| representing this symbol's name.
        """
        return self._props.get(PROP_NAME)

    def getSymbolClass(self):
        """Get symbol class.

        :returns: An |int| representing this symbol's symbol class, or
                  **None** if unknown.

        .. seealso:: |SymbolClass|
        """
        return self._props.get(PROP_SYMBOL_CLASS, SymbolClass.unknown)

    def getTypeClass(self):
        """Get symbol type class.

        :returns: An |int| representing this symbol's type class, or **None**
                  if unknown.

        .. seealso:: |TypeClass|
        """
        return self._props.get(PROP_TYPE_CLASS, TypeClass.unknown)

    def getTypeID(self):
        """Get type ID.

        If the symbol is a type and not a ``typedef``, return same as |getID|.

        :returns: A |basestring| representing this symbol's type ID.
        """
        return self._props.get(PROP_TYPE_ID)

    def getBaseTypeID(self):
        """Get base type ID.

        :returns: If this symbol is a

            * pointer type - return pointed type
            * array type - return element type
            * function type - return function result type
            * class type - return base class
            * otherwise - return **None**
        """
        return self._props.get(PROP_BASE_TYPE_ID)

    def getBitStride(self):
        """Return bit stride of this symbol for this array.

        :returns: An |int| reprsenting this symbol's bit stride in bits or
                  **None**.
        """
        return self._props.get(PROP_BIT_STRIDE)

    def getContainerID(self):
        """Get container type ID.

        :returns: If this symbol is a

            * field or member - return containing class type
            * member pointer - return containing class type
            * otherwise - return **None**
        """
        return self._props.get(PROP_CONTAINER_ID)

    def getIndexTypeID(self):
        """Get index type ID.

        :returns: If this symbol is a

            * array type - return array index type
            * otherwise - return **None**
        """
        return self._props.get(PROP_INDEX_TYPE_ID)

    def getSize(self):
        """Get value size of the symbol (or type).

        :returns: An |int| representing this symbol's size in bytes.
        """
        return self._props.get(PROP_SIZE, 0)

    def getLength(self):
        """If symbol is an array type, get its number of elements.

        :returns: An |int| reprsenting the number of elements of this symbol if
                  it is an array.
        """
        return self._props.get(PROP_LENGTH, 0)

    def getLowerBound(self):
        """If symbol is an array type, get array index lower bound.

        :returns: An |int| representing this array lower bound.
        """
        return self._props.get(PROP_LOWER_BOUND)

    def getUpperBound(self):
        """If symbol is an array type, get the array index upper bound.

        :returns: An |int| representing this array upper bound.
        """
        return self._props.get(PROP_UPPER_BOUND)

    def getOffset(self):
        """Return offset of this symbol for member of class, struct or union.

        :returns: An |int| reprsenting this symbol's offset in bytes or **0**.
        """
        return self._props.get(PROP_OFFSET, 0)

    def getAddress(self):
        """Return address of the symbol.

        :returns: An |int| representing this symbol's address or **None**
        """
        return self._props.get(PROP_ADDRESS)

    def getValue(self):
        """If symbol is a constant object, return its value.

        :returns: A |bytearray| representing this symbol's value.
        """
        return self._props.get(PROP_VALUE)

    def isBigEndian(self):
        """Get symbol values endianness.

        :returns: A |bool| set to **True** if this symbol is big-endian
        """
        return self._props.get(PROP_BIG_ENDIAN, False)

    def getRegisterID(self):
        """Return register ID if the symbol represents a register variable.

        :returns: A |basestring| representing this register ID or **None**.
        """
        return self._props.get(PROP_REGISTER)

    def getFlags(self):
        """Get symbol flags.

        :returns: An |int| representing this symbol flags (see
                  `Symbol Flags Properties`_).
        """
        return self._props.get(PROP_FLAGS, 0)

    def getLocalEntryOffset(self):
        """Return offset of the symbol local entry point.

        :returns: An |int| representing this symbol's local entry point offset
                  or **None**
        """
        return self._props.get(PROP_LOC_ENT_OFFSET)

    def getProperties(self):
        """Get complete map of context properties.

        :returns: A |dict| of the properties describing this symbol.
        """
        return self._props


class SymbolsService(services.Service):
    """TCF Symbols services interface"""

    def getName(self):
        """Get this service name.

        :returns: A |basestring| representing this service name, which is the
                  value of :const:`NAME`
        """
        return NAME

    def getContext(self, contextID, done):
        """Retrieve symbol context info for given symbol ID.

        :param contextID: ID of the symbol to retrieve.
        :type contextID: |basestring|
        :param done: Call back interface called when operation is completed.
        :type done: |DoneGetContext|

        :returns: Pending command handle, can be used to cancel the command.
        """
        raise NotImplementedError("Abstract method")

    def getChildren(self, parent_context_id, done):
        """Retrieve children IDs for given parent ID.

        Meaning of the operation depends on parent kind:

            * struct, union, or class type - get fields
            * enumeration type - get enumerators

        :param parent_context_id: Parent symbol context ID.
        :type parent_context_id: |basestring|
        :param done: Call back interface called when operation is completed.
        :type done: |DoneGetChildren|

        :returns: Pending command handle, can be used to cancel the command.
        """
        raise NotImplementedError("Abstract method")

    def find(self, context_id, ip, name, done):
        """Search first symbol with given name in given context.

        The context can be memory space, process, thread or stack frame.

        :param context_id: A search scope context ID.
        :type context_id: |basestring|
        :param ip: instruction pointer - ignored if *context_id* is a stack
                   frame ID.
        :param ip: |int|
        :param name: Symbol name to look for.
        :type name: |basestring|
        :param done: Call back interface called when operation is completed.
        :type done: |DoneFind|

        :returns: Pending command handle, can be used to cancel the command.
        """
        raise NotImplementedError("Abstract method")

    def findByName(self, context_id, ip, name, done):
        """Search symbols with given name in given context.

        The context can be memory space, process, thread or stack frame.

        :param context_id: A search scope context ID.
        :type context_id: |basestring|
        :param ip: instruction pointer - ignored if *context_id* is a stack
                   frame ID.
        :type ip: |int|
        :param name: Symbol name to look for.
        :type name: |basestring|
        :param done: Call back interface called when operation is completed.
        :type done: |DoneFind|

        :returns: Pending command handle, can be used to cancel the command.
        """
        raise NotImplementedError("Abstract method")

    def findByAddr(self, context_id, addr, done):
        """Search symbol with given address in given context.

        The context can be memory space, process, thread or stack frame.

        :param context_id: A search scope context ID.
        :type context_id: |basestring|
        :param addr: Address of the symbol to look for.
        :type addr: |int|
        :param done: Call back interface called when operation is completed.
        :type done: |DoneFind|

        :returns: Pending command handle, can be used to cancel the command.
        """
        raise NotImplementedError("Abstract method")

    def findInScope(self, context_id, ip, scope_id, name, done):
        """Search symbols with given name in given context or in given symbol
        scope.

        The context can be memory space, process, thread or stack frame.

        The symbol scope can be any symbol.

        If *ip* is not **None**, the search of the symbol name is done first in
        the scope defined by *context_id* and *ip*.

        If the symbol is not found, the supplied scope is then used.

        :param context_id: A search scope context ID.
        :type context_id: |basestring|
        :param ip: instruction pointer. Can be null if only *scope_id* should
                   be used.
        :type ip: |int| or **None**
        :param scope_id: Symbol scope context ID.
        :type scope_id: |basestring|
        :param name: Symbol name to look for.
        :type name: |basestring|
        :param done: Call back interface called when operation is completed.
        :type done: |DoneFind|

        :returns: Pending command handle, can be used to cancel the command.
        """
        raise NotImplementedError("Abstract method")

    def list(self, context_id, done):  # @ReservedAssignment
        """List all symbols in given context.

        The context can be a stack frame.

        :param context_id: A scope context ID.
        :type context_id: |basestring|
        :param done: Call back interface called when operation is completed.
        :type done: |DoneList|

        :returns: Pending command handle, can be used to cancel the command.
        """
        raise NotImplementedError("Abstract method")

    def getArrayType(self, type_id, length, done):
        """Create an array type.

        :param type_id: Symbol ID of the array cell type.
        :type type_id: |basestring|
        :param length: length of the array. A length of 0 creates a pointer
                       type.
        :type length: |int|
        :param done: Call back interface called when operation is completed.
        :type done: |DoneGetArrayType|

        :returns: Pending command handle, can be used to cancel the command.
        """
        raise NotImplementedError("Abstract method")

    def findFrameInfo(self, context_id, address, done):
        """Retrieve stack tracing commands for given instruction address in a
        context memory.

        :param context_id: Executable context ID.
        :type context_id: |basestring|
        :param address: Instruction address.
        :type address: |int|
        :param done: Call back interface called when operation is completed.
        :type done: |DoneFindFrameInfo|

        :returns: Pending command handle, can be used to cancel the command.
        """
        raise NotImplementedError("Abstract method")

    def getLocationInfo(self, symbolID, done):
        """Retrieve symbol location information.

        :param symbol_id: Symbol ID.
        :type symbol_id: |basestring|
        :param done: Call back interface called when operation is completed.
        :type done: |DoneGetLocationInfo|

        :returns: Pending command handle, can be used to cancel the command.
        """
        raise NotImplementedError("Abstract method")

    def getSymFileInfo(self, contextID, address, done):
        """Get symbol file info for a module that contains given address in a
        memory space.

        :param contextID: A memory space (process) ID.
        :type contextID: |basestring|
        :param address: An address in the memory space.
        :type address: |int|
        :param done: Call back interface called when operation is completed.
        :type done: |DoneGetSymFileInfo|

        :returns: Pending command handle, can be used to cancel the command.
        """
        raise NotImplementedError("Abstract method")


class DoneGetContext(object):
    """Client call back interface for |getContext|."""
    def doneGetContext(self, token, error, context):
        """Called when |getContext| is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param context: Retreived symbol context.
        :type context: |Symbol|
        """
        pass


class DoneGetLocationInfo(object):
    """Client call back interface for |getLocationInfo|.
    """
    def doneGetLocationInfo(self, token, error, props):
        """Called when location information retrieval is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param props: Symbol location properties, see
                      `Symbol Location Properties`_.
        :type props: |dict|
        """
        pass


class DoneGetChildren(object):
    """Client call back interface for |getChildren|."""
    def doneGetChildren(self, token, error, context_ids):
        """Called when context list retrieval is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param context_ids: List of available context IDs.
        :type context_ids: |list|
        """
        pass


class DoneFind(object):
    """Client call back interface for |find|, |findByName| and |findInScope|
    commands.
    """
    def doneFind(self, token, error, symbol_ids):
        """Called when symbol search is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param symbol_ids: List of symbol ID.
        :type symbol_ids: |list|
        """
        pass


class DoneGetSymFileInfo(object):
    """Client call back interface for |getSymFileInfo|."""
    def doneGetSymFileInfo(self, token, error, props):
        """Called when symbol file information retrieval is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param props: Symbol file properties.
        :type props: |dict|
        """
        pass


class DoneList(object):
    """Client call back interface for |list|."""
    def doneList(self, token, error, symbol_ids):
        """Called when symbol list retrieval is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param symbol_ids: List of symbol IDs.
        :type symbol_ids: |list|
        """
        pass


class DoneGetArrayType(object):
    """Client call back interface for |getArrayType|."""
    def doneGetArrayType(self, token, error, type_id):
        """Called when array type creation is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param type_id: Array type symbol ID.
        :type type_id: |basestring|
        """
        pass


class DoneFindFrameInfo(object):
    """Client call back interface for |findFrameInfo|."""
    def doneFindFrameInfo(self, token, error, address, size, fp_cmds,
                          reg_cmds):
        """Called when stack tracing information retrieval is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param address: Start of instruction address range.
        :type address: |int|
        :param size: Size of instruction address range.
        :type size: |int|
        :param fp_cmds: Commands to calculate stack frame pointer.
        :type fp_cmds: |list|
        :param reg_cmds: Map register IDs -> commands to calculate register
                         values.
        :type reg_cmds: |dict|
        """
        pass
