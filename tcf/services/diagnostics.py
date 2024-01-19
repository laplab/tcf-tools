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

"""This is an optional service that can be implemented by a peer.

.. |cancelTest| replace:: :meth:`DiagnosticsService.cancelTest`
.. |createTestStreams| replace:: :meth:`DiagnosticsService.createTestStreams`
.. |disposeTestStream| replace:: :meth:`DiagnosticsService.disposeTestStream`
.. |echo| replace:: :meth:`DiagnosticsService.echo`
.. |echoERR| replace:: :meth:`DiagnosticsService.echoERR`
.. |echoFP| replace:: :meth:`DiagnosticsService.echoFP`
.. |getSymbol| replace:: :meth:`DiagnosticsService.getSymbol`
.. |getTestList| replace:: :meth:`DiagnosticsService.getTestList`
.. |not_impl_co| replace:: :meth:`DiagnosticsService.not_implemented_command`
.. |runTest| replace:: :meth:`DiagnosticsService.runTest`
.. |DoneCancelTest| replace:: :class:`DoneCancelTest`
.. |DoneCreateTestStreams| replace:: :class:`DoneCreateTestStreams`
.. |DoneDisposeTestStream| replace:: :class:`DoneDisposeTestStream`
.. |DoneEcho| replace:: :class:`DoneEcho`
.. |DoneEchoERR| replace:: :class:`DoneEchoERR`
.. |DoneEchoFP| replace:: :class:`DoneEchoFP`
.. |DoneGetSymbol| replace:: :class:`DoneGetSymbol`
.. |DoneGetTestList| replace:: :class:`DoneGetTestList`
.. |DoneNotImplementedCommand| replace:: :class:`DoneNotImplementedCommand`
.. |DoneRunTest| replace:: :class:`DoneRunTest`
.. |Symbol| replace:: :class:`Symbol`
.. |Symbol.getStorage| replace:: :meth:`Symbol.getStorage`
.. |Symbol.isCommon| replace:: :meth:`Symbol.isCommon`
.. |Symbol.isGlobal| replace:: :meth:`Symbol.isGlobal`
.. |Symbol.isLocal| replace:: :meth:`Symbol.isLocal`
.. |Symbol.isUndef| replace:: :meth:`Symbol.isUndef`

If implemented, the service can be used for testing of the peer and
communication channel functionality and reliability.

Properties
----------
Symbol Properties
^^^^^^^^^^^^^^^^^
Those are the names of the properties used for |Symbol| object creation.

+---------------------+--------------+----------------------------------------+
| Name                | Type         | Description                            |
+=====================+==============+========================================+
| Symbol.ABSOLUTE     | |bool|       | States if the symbol address is        |
|                     |              | absolute.                              |
+---------------------+--------------+----------------------------------------+
| Symbol.SECTION_NAME | |basestring| | Name of the section the symbol belongs |
|                     |              | to                                     |
+---------------------+--------------+----------------------------------------+
| Symbol.STORAGE      | |basestring| | Symbol storage type. May be any of the |
|                     |              | values defined in                      |
|                     |              | `Symbol Storage Properties`_.          |
+---------------------+--------------+----------------------------------------+
| Symbol.VALUE        | |int|        | Value of the symbol (address).         |
+---------------------+--------------+----------------------------------------+

Symbol Storage Properties
^^^^^^^^^^^^^^^^^^^^^^^^^
All symbol storage properties are of type |basestring|. The symbol storage
type can be retrieved with the |Symbol.getStorage| method.

+-----------------------+-----------------------------------------------------+
| Name                  | Description                                         |
+=======================+=====================================================+
| Symbol.STORAGE_COMMON | Symbol is common. See |Symbol.isCommon|.            |
+-----------------------+-----------------------------------------------------+
| Symbol.STORAGE_GLOBAL | Symbol is global. See |Symbol.isGlobal|.            |
+-----------------------+-----------------------------------------------------+
| Symbol.STORAGE_LOCAL  | Symbol is local. See |Symbol.isLocal|.              |
+-----------------------+-----------------------------------------------------+
| Symbol.STORAGE_UNDEF  | Symbol is undefined. See |Symbol.isUndef|.          |
+-----------------------+-----------------------------------------------------+

Service Methods
---------------
.. autodata:: NAME
.. autoclass:: DiagnosticsService

cancelTest
^^^^^^^^^^
.. automethod:: DiagnosticsService.cancelTest

createTestStreams
^^^^^^^^^^^^^^^^^
.. automethod:: DiagnosticsService.createTestStreams

disposeTestStream
^^^^^^^^^^^^^^^^^
.. automethod:: DiagnosticsService.disposeTestStream

echo
^^^^
.. automethod:: DiagnosticsService.echo

echoERR
^^^^^^^
.. automethod:: DiagnosticsService.echoERR

echoFP
^^^^^^
.. automethod:: DiagnosticsService.echoFP

getName
^^^^^^^
.. automethod:: DiagnosticsService.getName

getSymbol
^^^^^^^^^
.. automethod:: DiagnosticsService.getSymbol

getTestList
^^^^^^^^^^^
.. automethod:: DiagnosticsService.getTestList

not_implemented_command
^^^^^^^^^^^^^^^^^^^^^^^
.. automethod:: DiagnosticsService.not_implemented_command

runTest
^^^^^^^
.. automethod:: DiagnosticsService.runTest

Callback Classes
----------------
DoneCancelTest
^^^^^^^^^^^^^^
.. autoclass:: DoneCancelTest
    :members:

DoneCreateTestStreams
^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: DoneCreateTestStreams
    :members:

DoneDisposeTestStream
^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: DoneDisposeTestStream
    :members:

DoneEcho
^^^^^^^^
.. autoclass:: DoneEcho
    :members:

DoneEchoERR
^^^^^^^^^^^
.. autoclass:: DoneEchoERR
    :members:

DoneEchoFP
^^^^^^^^^^
.. autoclass:: DoneEchoFP
    :members:

DoneGetSymbol
^^^^^^^^^^^^^
.. autoclass:: DoneGetSymbol
    :members:

DoneGetTestList
^^^^^^^^^^^^^^^
.. autoclass:: DoneGetTestList
    :members:

DoneNotImplementedCommand
^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: DoneNotImplementedCommand
    :members:

DoneRunTest
^^^^^^^^^^^
.. autoclass:: DoneRunTest
    :members:

Helper Classes
--------------
Symbol
^^^^^^
.. autoclass:: Symbol
    :members:
"""

from .. import services

NAME = "Diagnostics"
"""Diagnostics service name."""


class DiagnosticsService(services.Service):
    def getName(self):
        """Get this service name.

        :returns: A |basestring| representing this service name, which is the
                  value of :const:`NAME`
        """
        return NAME

    def echo(self, s, done):
        """The |echo| command result returns same string that was given as
        command argument.

        The command is used to test communication channel ability to transmit
        arbitrary strings in both directions.

        :param s: Any string.
        :type s: |basestring|
        :param done: Command result call back object.
        :type done: |DoneEcho|

        :returns: Pending command handle.
        """
        return NotImplementedError("Abstract method")

    def echoFP(self, n, done):
        """The |echoFP| command result returns same floating point number that
        was given as command argument.

        The command is used to test communication channel ability to transmit
        arbitrary floating point numbers in both directions.

        :param n: Any floating point number.
        :type n: |float|
        :param done: Command result call back object.
        :type done: |DoneEchoFP|

        :returns: Pending command handle.
        """
        return NotImplementedError("Abstract method")

    def echoERR(self, error, done):
        """The |echoERR| command result returns same error report that was
        given as command argument.

        The command is used to test remote agent ability to receive and
        transmit TCF error reports.

        :param error: An error object.
        :type error: |Exception|
        :param done: Command result call back object.
        :type done: |DoneEchoERR|

        :returns: pending command handle.
        """
        return NotImplementedError("Abstract method")

    def getTestList(self, done):
        """Get list of test names that are implemented by the service.

        Clients can request remote peer to run a test from the list.
        When started, a test performs a predefined set actions.
        Nature of test actions is uniquely identified by test name.
        Exact description of test actions is a contract between client and
        remote peer, and it is not part of Diagnostics service specifications.
        Clients should not attempt to run a test if they don't recognize the
        test name.

        :param done: Command result call back object.
        :type done: |DoneGetTestList|

        :returns: Pending command handle.
        """
        return NotImplementedError("Abstract method")

    def runTest(self, name, done):
        """Run a test.

        When started, a test performs a predefined set actions.
        Nature of test actions is uniquely identified by test name.
        Running test usually has associated execution context ID.
        Depending on the test, the ID can be used with services RunControl
        and/or Processes services to control test execution, and to obtain
        test results.

        :param name: Test name. Must be one of the names returned by
                     |getTestList|.
        :type name: |basestring|
        :param done: Command result call back object.
        :type done: |DoneRunTest|

        :returns: Pending command handle.
        """
        return NotImplementedError("Abstract method")

    def cancelTest(self, context_id, done):
        """Cancel execution of a test.

        :param context_id: Test execution context ID. Must be the TCF ID
                           returned by a |runTest| command.
        :type context_id: |basestring|
        :param done: Command result call back object.
        :type done: |DoneCancelTest|

        :returns: Pending command handle.
        """
        return NotImplementedError("Abstract method")

    def getSymbol(self, context_id, symbol_name, done):
        """Get information about a symbol in text execution context.

        There is a set of predefined symbols for a diagnostics test. For the
        opensource agent, those are :

            - ``tcf_test_array``
            - ``tcf_test_char``
            - ``tcf_test_func0``
            - ``tcf_test_func1``
            - ``tcf_test_func2``
            - ``tcf_test_func3``

        :param context_id: Test context ID. Must be the TCF ID returned by a
                           |runTest| command.
        :param symbol_name: Name of the symbol to retrieve.
        :param done: Command result call back object.
        :type done: |DoneGetSymbol|

        :returns: A |Symbol| matching *context_id* and *name*.
        """
        return NotImplementedError("Abstract method")

    def createTestStreams(self, inp_buf_size, out_buf_size, done):
        """Create a pair of virtual streams

        Remote ends of the streams are connected, so any data sent into *input*
        stream will become for available for reading from *output* stream.
        The command is used for testing virtual streams.

        :param inp_buf_size: Buffer size in bytes of the input stream.
        :type inp_buf_size: |int|
        :param out_buf_size: Buffer size in bytes of the output stream.
        :type out_buf_size: |int|
        :param done: Command result call back object.
        :type done: |DoneCreateTestStreams|

        :returns: Pending command handle.

        :seealso: :class:`tcf.services.streams` service.
        """
        return NotImplementedError("Abstract method")

    def disposeTestStream(self, streamID, done):
        """Dispose a virtual stream that was created by |createTestStreams|
        command.

        :param streamID: The stream ID. Must be one of the IDs returned by
                         |createTestStreams|.
        :type streamID: |basestring|
        :param done: Command result call back object.
        :type done: |DoneDisposeTestStream|

        :returns: Pending command handle.
        """
        return NotImplementedError("Abstract method")

    def not_implemented_command(self, done):
        """Send a command that is not implemented by peer.

        :param done: Command result call back object
        :type done: |DoneNotImplementedCommand|

        :returns: Pending command handle.
        """
        return NotImplementedError("Abstract method")


class DoneEcho(object):
    """Call back interface for |echo| command."""

    def doneEcho(self, token, error, s):
        """Called when |echo| command is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param s: Same string as the command argument.
        :type s: |basestring|
        """
        pass


class DoneEchoFP(object):
    """Call back interface for |echoFP| command."""

    def doneEchoFP(self, token, error, n):
        """Called when :meth:`~.DiagnosticsService.echoFP` command is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param n: Same number as the command argument.
        :type n: |int|
        """
        pass


class DoneEchoERR(object):
    """Call back interface for |echoERR| command."""

    def doneEchoERR(self, token, error, error_obj, error_msg):
        """Called when |echoERR| command is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param error_obj: Error object, should be equal to the command
                          argument.
        :type error_obj: |Exception|
        :param error_msg: Error object converted to a human readable string.
        :type error_msg: |basestring|
        """
        pass


class DoneGetTestList(object):
    """Call back interface for |getTestList| command."""

    def doneGetTestList(self, token, error, testList):
        """Called when |getTestList| command is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param testList: Names of tests that are supported by the peer.
        :type testList: |list|
        """
        pass


class DoneRunTest(object):
    """Call back interface for |runTest| command."""

    def doneRunTest(self, token, error, context_id):
        """Called when |runTest| command is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param context_id: Test execution contest ID.
        :type context_id: |basestring|
        """
        pass


class DoneCancelTest(object):
    """Call back interface for |cancelTest| command."""

    def doneCancelTest(self, token, error):
        """Called when |cancelTest| command is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        """
        pass


class DoneGetSymbol(object):
    """Call back interface for |getSymbol| command."""

    def doneGetSymbol(self, token, error, symbol):
        """Called when |getSymbol| command is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param symbol: The so-retrieved symbol.
        :type symbol: |Symbol|
        """
        pass


class Symbol(object):
    """Represents result value of |getSymbol| command.

    :param props: Properties to initialise this symbol with. See
                  `Symbol Properties`_.
    :type props: |dict|
    """

    ABSOLUTE = 'Abs'
    SECTION_NAME = 'Section'
    STORAGE = 'Storage'
    VALUE = 'Value'

    STORAGE_COMMON = 'COMMON'
    STORAGE_GLOBAL = 'GLOBAL'
    STORAGE_LOCAL = 'LOCAL'
    STORAGE_UNDEF = 'UNDEF'

    def __init__(self, props):
        self._props = props or {}

    def __str__(self):
        return (str(self._props))

    def getSectionName(self):
        """Get this symbol section name.

        :returns: A |basestring| representing this symbol section name or
                  **None**.
        """
        return self._props.get(self.SECTION_NAME)

    def getStorage(self):
        """Get this symbol storage type.

        The returned vaue is one of :

            - ``Symbol.STORAGE_COMMON`` (see |Symbol.isCommon|)
            - ``Symbol.STORAGE_GLOBAL`` (see |Symbol.isGlobal|)
            - ``Symbol.STORAGE_LOCAL`` (see |Symbol.isLocal|)
            - ``Symbol.STORAGE_UNDEF`` (see |Symbol.isUndef|)
            - **None** if unknown

        :returns: A |basestring| representing this symbol storage type or
                  **None**.
        """
        return self._props.get(self.STORAGE)

    def getValue(self):
        """Get this symbol value (address).

        :returns: An |int| representing this symbol value (address) or **0**.
        """
        return self._props.get(self.VALUE)

    def isUndef(self):
        """Check if this symbol storage type is ``UNDEF``.

        :returns: A |bool| stating if this symbol's storage is undefined.
        """
        val = self._props.get(self.STORAGE)
        return val == self.STORAGE_UNDEF

    def isCommon(self):
        """Check if this symbol storage type is ``COMMON``.

        :returns: A |bool| stating if this symbol's storage is common.
        """
        val = self._props.get(self.STORAGE)
        return val == self.STORAGE_COMMON

    def isGlobal(self):
        """Check if this symbol storage type is ``GLOBAL``.

        :returns: A |bool| stating if this symbol's storage is global.
        """
        val = self._props.get(self.STORAGE)
        return val == self.STORAGE_GLOBAL

    def isLocal(self):
        """Check if this symbol storage type is ``LOCAL``.

        :returns: A |bool| stating if this symbol's storage is local.
        """
        val = self._props.get(self.STORAGE)
        return val == self.STORAGE_LOCAL

    def isAbs(self):
        """Check if this symbol is absolute.

        :returns: A |bool| stating if this symbol is absolute.
        """
        return self._props.get(self.ABSOLUTE, False)


class DoneCreateTestStreams(object):
    """Call back interface for |createTestStreams| command."""

    def doneCreateTestStreams(self, token, error, inp_id, out_id):
        """Called when |createTestStreams| command is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param inp_id: The input stream ID.
        :type inp_id: |basestring|
        :param out_id: The output stream ID.
        :type out_id: |basestring|
        """
        pass


class DoneDisposeTestStream(object):
    """Call back interface for |disposeTestStream| command."""

    def doneDisposeTestStream(self, token, error):
        """Called when |createTestStreams| command is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        """
        pass


class DoneNotImplementedCommand(object):
    """Call back interface for |not_impl_co| command."""

    def doneNotImplementedCommand(self, token, error):
        """Called when |not_impl_co| command is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        """
        pass
