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

"""TCF Disassembly service interface.

Disassembly Properties
----------------------
Properties
^^^^^^^^^^
+------------------+--------------+-------------------------------------------+
| Name             | Type         | Description                               |
+==================+==============+===========================================+
| PROP_ISA         | |basestring| | The name of the instruction set           |
|                  |              | architecture.                             |
+------------------+--------------+-------------------------------------------+
| PROP_OPCODEVALUE | |bool|       | If **True**, the instruction code byte    |
|                  |              | values are returned.                      |
+------------------+--------------+-------------------------------------------+
| PROP_PSEUDO      | |bool|       | If **True**, pseudo-instructions are      |
|                  |              | requested.                                |
+------------------+--------------+-------------------------------------------+
| PROP_SIMPLIFIED  | |bool|       | If **True**, simplified mnemonics are     |
|                  |              | specified.                                |
+------------------+--------------+-------------------------------------------+

Capabilities
^^^^^^^^^^^^
+------------------------+--------------+-------------------------------------+
| Name                   | Type         | Description                         |
+========================+==============+=====================================+
| CAPABILITY_ISA         | |basestring| | The name of the instruction set     |
|                        |              | architecture.                       |
+------------------------+--------------+-------------------------------------+
| CAPABILITY_OPCODEVALUE | |bool|       | If **True**, the decoded instruction|
|                        |              | code bytes are retrievable with the |
|                        |              | OpcodeValue parameter.              |
+------------------------+--------------+-------------------------------------+
| CAPABILITY_PSEUDO      | |bool|       | If **True**, pseudo-instructions are|
|                        |              | supported or requested.             |
+------------------------+--------------+-------------------------------------+
| CAPABILITY_SIMPLIFIED  | |bool|       | If **True**, simplified mnemonics   |
|                        |              | are supported or requested.         |
+------------------------+--------------+-------------------------------------+

Fields
^^^^^^
+---------------------+--------------+----------------------------------------+
| Name                | Type         | Description                            |
+=====================+==============+========================================+
| FIELD_ADDRESS_SPACE | |int|        | Context ID of the address space used   |
|                     |              | with ``FTYPE_ADDRESS`` types.          |
+---------------------+--------------+----------------------------------------+
| FIELD_TEXT          | |basestring| | Value of the field for ``FTYPE_STRING``|
|                     |              | and ``FTYPE_REGISTER`` types.          |
+---------------------+--------------+----------------------------------------+
| FIELD_TYPE          | |basestring| | Instruction field properties. The type |
|                     |              | of the instruction field. See          |
|                     |              | `Field Types`_.                        |
+---------------------+--------------+----------------------------------------+
| FIELD_VALUE         | |int|        | Value of the field for                 |
|                     |              | ``FTYPE_ADDRESS``,                     |
|                     |              | ``FTYPE_DISPLACEMENT``, or             |
|                     |              | ``FTYPE_IMMEDIATE`` types.             |
+---------------------+--------------+----------------------------------------+

Field Types
^^^^^^^^^^^
+--------------------+--------------------------------------+
| Name               | Description                          |
+====================+======================================+
| FTYPE_ADDRESS      | Instruction field type Address.      |
+--------------------+--------------------------------------+
| FTYPE_DISPLACEMENT | Instruction field type Displacement. |
+--------------------+--------------------------------------+
| FTYPE_IMMEDIATE    | Instruction field type Immediate.    |
+--------------------+--------------------------------------+
| FTYPE_REGISTER     | Instruction field type Register.     |
+--------------------+--------------------------------------+
| FTYPE_STRING       | Instruction field type String.       |
+--------------------+--------------------------------------+

Service Methods
---------------
.. autodata:: NAME
.. autoclass:: DisassemblyService

disassemble
^^^^^^^^^^^
.. automethod:: DisassemblyService.disassemble

getCapabilities
^^^^^^^^^^^^^^^
.. automethod:: DisassemblyService.getCapabilities

getName
^^^^^^^
.. automethod:: DisassemblyService.getName

Callback Classes
----------------
DoneDisassemble
^^^^^^^^^^^^^^^
.. autoclass:: DoneDisassemble
    :members:

DoneGetCapabilities
^^^^^^^^^^^^^^^^^^^
.. autoclass:: DoneGetCapabilities
    :members:

Helper Classes
--------------
DisassemblyLine
^^^^^^^^^^^^^^^
.. autoclass:: DisassemblyLine
    :members:
"""

from .. import services

NAME = "Disassembly"
"""Disassembly service name."""

CAPABILITY_ISA = "ISA"
CAPABILITY_SIMPLIFIED = "Simplified"
CAPABILITY_PSEUDO = "Pseudo"
CAPABILITY_OPCODEVALUE = "OpcodeValue"

FIELD_TYPE = "Type"
FIELD_TEXT = "Text"
FIELD_VALUE = "Value"
FIELD_ADDRESS_SPACE = "AddressSpace"

# Instruction field types
FTYPE_STRING = "String"
FTYPE_REGISTER = "Register"
FTYPE_ADDRESS = "Address"
FTYPE_DISPLACEMENT = "Displacement"
FTYPE_IMMEDIATE = "Immediate"

# disassemble parameters
PROP_ISA = "ISA"
PROP_SIMPLIFIED = "Simplified"
PROP_PSEUDO = "PseudoInstructions"
PROP_OPCODEVALUE = "OpcodeValue"


class DisassemblyService(services.Service):
    def getName(self):
        """Get this service name.

        :returns: The value of string :const:`NAME`
        """
        return NAME

    def getCapabilities(self, context_id, done):
        """Retrieve disassembly service capabilities a given context-id.

        :param context_id: a context ID, usually one returned by Run Control
                            or Memory services.
        :param done: command result call back object.
        :type done: :class:`DoneGetCapabilities`

        :returns: pending command handle.
        """
        raise NotImplementedError("Abstract method")

    def disassemble(self, context_id, addr, size, params, done):
        """Disassemble instruction code from a specified range of memory
        addresses, in a specified context.

        :param context_id: a context ID, usually one returned by Run Control
                            or Memory services.
        :param addr: address of first instruction to disassemble.
        :param size: size in bytes of the address range.
        :param params: properties to control the disassembly output, an
                        element of capabilities array, see
                        :meth:`~DisassemblyService.getCapabilities`
        :param done: command result call back object.
        :type done: :class:`DoneDisassemble`

        :returns: pending command handle.
        """
        raise NotImplementedError("Abstract method")


class DoneGetCapabilities(object):
    """Call back interface for 'getCapabilities' command."""
    def doneGetCapabilities(self, token, error, capabilities):
        """Called when capabilities retrieval is done.

        :param token: command handle.
        :param error: error object or None.
        :param capabilities: array of capabilities, see `Capabilities`_ for
                              contents of each array element.
        """
        pass


class DoneDisassemble(object):
    """Call back interface for 'disassemble' command."""
    def doneDisassemble(self, token, error, disassembly):
        """Called when disassembling is done.

        :param token: command handle.
        :param error: error object or None.
        :param disassembly: array of disassembly lines.
        """
        pass


class DisassemblyLine(object):
    """Represents a single disassembly line.

    :param addr: Address of the disassembled line.
    :param size: The size (in bytes) of this disassembled line.
    :param instuction: Disassembled instruction.
    :param opcode: Instruction opcode (if any)
    """
    def __init__(self, addr, size, instruction, opcode=None):
        self.addr = addr
        self.size = size or 0
        self.instruction = instruction
        self.opcode = opcode

    def getAddress(self):
        """
        :returns: Instruction address.
        """
        return self.addr

    def getOpcodeValue(self):
        """
        :returns: a |bytearray| representing this instruction opcode value.
        """
        return self.opcode

    def getSize(self):
        """
        :returns: Instruction size in bytes.
        """
        return self.size

    def getInstruction(self):
        """Get disassembled instruction.

        :returns: array of instruction fields, each field is a collection of
                  field properties, see `Fields`_.
        """
        return self.instruction

    def __repr__(self):
        res = self.__class__.__name__ + '(' + repr(self.addr) + ', ' + \
            repr(self.size) + ', ' + repr(self.instruction) + ', ' + \
            repr(self.opcode) + ')'
        return res

    def __str__(self):
        op = self.opcode
        oplen = len(op)
        res = self.__class__.__name__ + ' [address=' + str(self.addr) + \
            ', size=' + str(self.size) + ', instruction=' + \
            str(self.instruction) + ', opcode=' + \
            ' '.join('%02x' % ord(byte) for byte in op[0:oplen]) + ']'
        return res
