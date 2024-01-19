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

"""Expressions service allows TCF client to perform expression evaluation on
remote target.

The service can be used to retrieve or modify values of variables or any data
structures in remote target memory.

Expressions Properties
----------------------
Context Properties
^^^^^^^^^^^^^^^^^^
+--------------------+--------------+-----------------------------------------+
| Name               | Type         | Description                             |
+====================+==============+=========================================+
| PROP_BITS          | |int|        | Size of expression value in bits.       |
+--------------------+--------------+-----------------------------------------+
| PROP_BIT_OFFS      | |int|        | Bit offset in expression piece.         |
+--------------------+--------------+-----------------------------------------+
| PROP_BIT_SIZE      | |int|        | Bit size of expression piece.           |
+--------------------+--------------+-----------------------------------------+
| PROP_CAN_ASSIGN    | |bool|       | **True** if the expression can be       |
|                    |              | assigned a new value.                   |
+--------------------+--------------+-----------------------------------------+
| PROP_CLASS         | |basestring| | Expression type class. See              |
|                    |              | :class:`~tcf.services.symbols.TypeClass`|
+--------------------+--------------+-----------------------------------------+
| PROP_EXPRESSION    | |basestring| | Expression script.                      |
+--------------------+--------------+-----------------------------------------+
| PROP_HAS_FUNC_CALL | |bool|       | **True** if the expression contains     |
|                    |              | target function call.                   |
+--------------------+--------------+-----------------------------------------+
| PROP_ID            | |basestring| | Expression context ID.                  |
+--------------------+--------------+-----------------------------------------+
| PROP_LANGUAGE      | |basestring| | Language of expression script.          |
+--------------------+--------------+-----------------------------------------+
| PROP_PARENT_ID     | |basestring| | ID of expression's parent context.      |
+--------------------+--------------+-----------------------------------------+
| PROP_PIECES        | |dict|       | Expression piece.                       |
+--------------------+--------------+-----------------------------------------+
| PROP_SIZE          | |int|        | Size in bytes.                          |
+--------------------+--------------+-----------------------------------------+
| PROP_SYMBOL_ID     | |basestring| | Symbol ID if the expression represents a|
|                    |              | symbol.                                 |
+--------------------+--------------+-----------------------------------------+
| PROP_TYPE          | |basestring| | Expression type ID.                     |
+--------------------+--------------+-----------------------------------------+

Value Properties
^^^^^^^^^^^^^^^^
+----------------+------------------------------------------------------------+
| Name           | Description                                                |
+================+============================================================+
| VAL_ADDRESS    | If the value is located in target memory, the address of   |
|                | the value.                                                 |
+----------------+------------------------------------------------------------+
| VAL_BIG_ENDIAN | Expression is big endian.                                  |
+----------------+------------------------------------------------------------+
| VAL_CLASS      | Value type class. See                                      |
|                | :class:`~tcf.services.symbols.TypeClass`.                  |
+----------------+------------------------------------------------------------+
| VAL_REGISTER   | If the value is located in a register, the register ID     |
|                | that holds the value.                                      |
+----------------+------------------------------------------------------------+
| VAL_SYMBOL     | If the value is defined by a symbol, the symbol ID.        |
+----------------+------------------------------------------------------------+
| VAL_TYPE       | The symbol type ID of the value.                           |
+----------------+------------------------------------------------------------+

Service Methods
---------------
.. autodata:: NAME
.. autoclass:: ExpressionsService

addListener
^^^^^^^^^^^
.. automethod:: ExpressionsService.addListener

assign
^^^^^^
.. automethod:: ExpressionsService.assign

create
^^^^^^
.. automethod:: ExpressionsService.create

dispose
^^^^^^^
.. automethod:: ExpressionsService.dispose

evaluate
^^^^^^^^
.. automethod:: ExpressionsService.evaluate

getChildren
^^^^^^^^^^^
.. automethod:: ExpressionsService.getChildren

getContext
^^^^^^^^^^
.. automethod:: ExpressionsService.getContext

getName
^^^^^^^
.. automethod:: ExpressionsService.getName

removeListener
^^^^^^^^^^^^^^
.. automethod:: ExpressionsService.removeListener

Callback Classes
----------------
DoneAssign
^^^^^^^^^^
.. autoclass:: DoneAssign
    :members:

DoneCreate
^^^^^^^^^^
.. autoclass:: DoneCreate
    :members:

DoneDispose
^^^^^^^^^^^
.. autoclass:: DoneDispose
    :members:

DoneEvaluate
^^^^^^^^^^^^
.. autoclass:: DoneEvaluate
    :members:

DoneGetChildren
^^^^^^^^^^^^^^^
.. autoclass:: DoneGetChildren
    :members:

DoneGetContext
^^^^^^^^^^^^^^
.. autoclass:: DoneGetContext
    :members:

Listener
--------
.. autoclass:: ExpressionsListener
    :members:

Helper Classes
--------------
Expression
^^^^^^^^^^
.. autoclass:: Expression
    :members:

Value
^^^^^
.. autoclass:: Value
    :members:

"""

from .. import services
from . import symbols

NAME = "Expressions"
"""Expressions service name."""

# Expression context property names.

PROP_ID = "ID"
PROP_PARENT_ID = "ParentID"
PROP_SYMBOL_ID = "SymbolID"
PROP_LANGUAGE = "Language"
PROP_EXPRESSION = "Expression"
PROP_BITS = "Bits"
PROP_SIZE = "Size"
PROP_TYPE = "Type"
PROP_CAN_ASSIGN = "CanAssign"
PROP_HAS_FUNC_CALL = "HasFuncCall"
PROP_CLASS = "Class"  # same as symbols.TypeClass
PROP_PIECES = "Pieces"
PROP_BIT_OFFS = "BitOffs"
PROP_BIT_SIZE = "BitSize"

# Expression value property names.

VAL_CLASS = "Class"  # same as symbols.TypeClass
VAL_TYPE = "Type"
VAL_SYMBOL = "Symbol"
VAL_REGISTER = "Register"
VAL_ADDRESS = "Address"
VAL_BIG_ENDIAN = "BigEndian"


class Expression(object):
    """Expression object represent an expression that can be evaluated by
    remote target.

    It has a unique ID and contains all information necessary to compute a
    value.

    The object data usually includes:

        1. process, thread or stack frame ID that should be used to resolve
           symbol names
        2. a script that can compute a value, like ``x.y + z``

    :param props: Property dictionnary defining the expression.
                  See `Context Properties`_.
    """

    def __init__(self, props):
        self._props = props or {}

    def __str__(self):
        return "[Expression Context %s]" % self._props

    def getID(self):
        """Get context ID.

        :returns: Context ID.
        """
        return self._props.get(PROP_ID)

    def getParentID(self):
        """Get parent context ID.

        :returns: Parent context ID.
        """
        return self._props.get(PROP_PARENT_ID)

    def getLanguage(self):
        """Get expression script language ID.

        :returns: Language ID.
        """
        return self._props.get(PROP_LANGUAGE)

    def getExpression(self):
        """Return expression string - the script part of the context.

        :returns: Expression script string.
        """
        return self._props.get(PROP_EXPRESSION)

    def getSymbolID(self):
        """Return symbol ID if the expression represents a symbol (e.g. local
        variable).

        :returns: Symbol ID.
        """
        return self._props.get(PROP_SYMBOL_ID)

    def getBits(self):
        """Get size of expression value in bits.

        Can be **0** if value size is even number of bytes, use :meth:`getSize`
        in such case.

        :returns: Size in bits.
        """
        return self._props.get(PROP_BITS, 0)

    def getBitSize(self):
        """Get size of expression value in bits.

        Can be **0** if value size is even number of bytes, use :meth:`getSize`
        in such case.

        :returns: Size in bits.
        """
        return self._props.get(PROP_BIT_SIZE, 0)

    def getPieces(self):
        """Get complete dictionary of pieces properties.

        :returns: A |dict| of pieces properties.
        """
        return self._props.get(PROP_PIECES)

    def getBitOffset(self):
        """Get offset of expression value in bits.

        :returns: Offset in bits.
        """
        return self._props.get(PROP_BIT_OFFS, 0)

    def getSize(self):
        """Get size in bytes. The size can include extra (unused) bits.

        This is *static* or *declared* size - as determined by expression type.

        :returns: Size in bytes.
        """
        return self._props.get(PROP_SIZE, 0)

    def getTypeClass(self):
        """Get expression type class.

        :returns: type class

        .. seealso: :class:`~tcf.services.symbols.TypeClass`
        """
        return self._props.get(PROP_CLASS, symbols.TypeClass.unknown)

    def getTypeID(self):
        """Get expression type ID. Symbols service can be used to get type
        properties.

        This is *static* or *declared* type ID, actual type of a value can be
        different - if expression language supports dynamic typing.

        :returns: Type ID.

        .. seealso:: :mod:`~tcf.services.symbols`
        """
        return self._props.get(PROP_TYPE)

    def canAssign(self):
        """Check if the expression can be assigned a new value.

        :returns: **True** if can assign.
        """
        return self._props.get(PROP_CAN_ASSIGN)

    def hasFuncCall(self):
        """Check if the expression contains target function call.

        Such expression can resume the target when evaluated.

        :returns: **True** if has a function call.
        """
        return (self._props.get(PROP_HAS_FUNC_CALL))

    def getProperties(self):
        """Get complete dictionary of context properties.

        :returns: A |dict| of context properties.
        """
        return self._props


class Value(object):
    """Value represents result of expression evaluation.

    Note that same expression can be evaluated multiple times with different
    results.

    :param value: Expression value.
    :param props: Property dictionary defining the value.
    """

    def __init__(self, value, props):
        self._value = value
        self._props = props or {}

    def __str__(self):
        if isinstance(self._value, bytearray):
            valuestr = ' '.join([hex(b) for b in self._value])
        else:
            valuestr = str(self._value)
        return '[Expression Value %s %s]' % (valuestr, self._props)

    def getTypeClass(self):
        """Get value type class.

        :returns: type class

        .. seealso: :class:`~tcf.services.symbols.TypeClass`
        """
        return self._props.get(VAL_CLASS, symbols.TypeClass.unknown)

    def getTypeID(self):
        """Get value type ID. Symbols service can be used to get type
        properties.

        :returns: Type ID.
        """
        return self._props.get(VAL_TYPE)

    def isBigEndian(self):
        """Check endianness of the values.

        Big-endian means decreasing numeric significance with increasing
        byte number.

        :returns: **True** if big-endian.
        """
        return self._props.get(VAL_BIG_ENDIAN, False)

    def getAddress(self):
        """Get the value address if one exists.

        :returns: The value address or **None** if none address exists for the
                  value.
        """
        return self._props.get(VAL_ADDRESS)

    def getRegisterID(self):
        """Return register ID if the value represents register variable.

        :returns: Register ID or **None**.
        """
        return self._props.get(VAL_REGISTER)

    def getSymbolID(self):
        """Return symbol ID if the value represents a symbol.

        :returns: Symbol ID or **None** if value is not a symbol.
        """
        return self._props.get(VAL_SYMBOL)

    def getValue(self):
        """Get a 'packed binary data' encoded value.

        :returns: value as 'packed binary data'.

        .. seealso:: :mod:`struct`
        """
        return self._value

    def getProperties(self):
        """Get complete dictionary of value properties.

        :returns: A |dict| of value properties.
        """
        return self._props


class ExpressionsService(services.Service):
    def getName(self):
        """Get this service name.

        :returns: The value of string :const:`NAME`
        """
        return NAME

    def getContext(self, contextID, done):
        """Retrieve expression context info for given context ID.

        :param contextID: Context ID.
        :param done: Call back interface called when operation is completed.
        :type done: :class:`DoneGetContext`

        :returns: pending command handle.

        .. seealso:: :class:`Expression`
        """
        raise NotImplementedError("Abstract method")

    def getChildren(self, parent_context_id, done):
        """Retrieve children IDs for given parent ID.

        Meaning of the operation depends on parent kind:

        1. expression with type of a struct, union, or class - fields
        2. expression with type of an enumeration - enumerators
        3. expression with type of an array - array elements
        4. stack frame - function arguments and local variables
        5. thread - top stack frame function arguments and local variables
        6. process - global variables

        Children list *does not* include IDs of expressions that were created
        by clients using "create" command.

        :param parent_context_id: parent context ID.
        :param done: call back interface called when operation is completed.
        :type done: :class:`DoneGetChildren`

        :returns: Pending command handle.
        """
        raise NotImplementedError("Abstract method")

    def create(self, parent_id, language, expression, done):
        """Create an expression context.

        The context should be disposed after use.

        :param parent_id: A context ID that can be used to resolve symbol
                          names.
        :param language: Language of expression script, **None** means default
                         language.
        :param expression: Expression script
        :param done: Call back interface called when operation is completed.
        :type done: :class:`DoneCreate`

        :returns: pending command handle.
        """
        raise NotImplementedError("Abstract method")

    def dispose(self, contextID, done):
        """Dispose an expression context that was created by
        :meth:`~ExpressionsService.create`

        :param contextID: The expression context ID.
        :param done: Call back interface called when operation is completed.
        :type done: :class:`DoneDispose`

        :returns: Pending command handle.
        """
        raise NotImplementedError("Abstract method")

    def evaluate(self, contextID, done):
        """Evaluate value of an expression context.

        :param contextID: The expression context ID
        :param done: Call back interface called when operation is completed.
        :type done: :class:`DoneEvaluate`

        :returns: Pending command handle.
        """
        raise NotImplementedError("Abstract method")

    def assign(self, contextID, value, done):
        """Assign a value to memory location determined by an expression.

        :param contextID: Expression ID.
        :param value: Value as an array of bytes.
        :param done: Call back interface called when operation is completed.
        :type done: :class:`DoneAssign`

        :returns: pending command handle.
        """
        raise NotImplementedError("Abstract method")

    def addListener(self, listener):
        """Add expressions service event listener.

        :param listener: Event listener implementation.
        :type listener: :class:`ExpressionsListener`
        """
        raise NotImplementedError("Abstract method")

    def removeListener(self, listener):
        """Remove expressions service event listener.

        :param listener: Event listener implementation.
        :type listener: :class:`ExpressionsListener`
        """
        raise NotImplementedError("Abstract method")


class DoneGetContext(object):
    """Client call back interface for :meth:`~ExpressionsService.getContext`.
    """
    def doneGetContext(self, token, error, context):
        """Called when context data retrieval is done.

        :param token: Command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param context: Context properties.
        """
        pass


class DoneGetChildren(object):
    """Client call back interface for :meth:`~ExpressionsService.getChildren`.
    """
    def doneGetChildren(self, token, error, context_ids):
        """Called when context list retrieval is done.

        :param token: Command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param context_ids: An iterable of available context IDs.
        """
        pass


class DoneCreate(object):
    """Client call back interface for :meth:`~ExpressionsService.create`.
    """
    def doneCreate(self, token, error, context):
        """Called when context create context command is done.

        :param token: Command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param context: Context properties.
        """
        pass


class DoneDispose(object):
    """Client call back interface for :meth:`~ExpressionsService.dispose`."""

    def doneDispose(self, token, error):
        """Called when context dispose command is done.

        :param token: Command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        """
        pass


class DoneEvaluate(object):
    """Client call back interface for :meth:`~ExpressionsService.evaluate`."""

    def doneEvaluate(self, token, error, value):
        """Called when context dispose command is done.

        :param token: Command handle.
        :param error: Error description if operation failed, None if
                      succeeded.
        :param value: Expression evaluation result. See :class:`Value`.
        """
        pass


class DoneAssign(object):
    """Client call back interface for :meth:`~ExpressionsService.assign`."""

    def doneAssign(self, token, error):
        """Called when assign command is done.

        :param token: Command handle
        :param error: Error description if operation failed, **None** if
                      succeeded.
        """
        pass


class ExpressionsListener(object):
    """Registers event listener is notified when registers context hierarchy
    changes, and when a register is modified by the service commands.
    """

    def valueChanged(self, contextID):
        """Called when expression value was changed and clients need to update
        themselves.

        Clients, at least, should invalidate corresponding cached expression
        data.

        .. note:: Not every change is notified - it is not possible, only those
                  which are not caused by normal execution of the debuggee. At
                  least, changes caused by :meth:`~ExpressionsService.assign`
                  command should be notified.

        :param contextID: Expression context ID.
        """
        pass
