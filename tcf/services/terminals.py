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

"""Terminals Service allows to launch a new terminal on the remote target
system.

.. |addListener| replace:: :meth:`TerminalsService.addListener`
.. |exit| replace:: :meth:`TerminalsService.exit`
.. |getContext| replace:: :meth:`TerminalsService.getContext`
.. |getProperties| replace:: :meth:`TerminalContext.getProperties`
.. |launch| replace:: :meth:`TerminalsService.launch`
.. |removeListener| replace:: :meth:`TerminalsService.removeListener`
.. |setWinSize| replace:: :meth:`TerminalsService.setWinSize`
.. |memory| replace:: :mod:`tcf.services.memory`
.. |streams| replace:: :mod:`tcf.services.streams`
.. |DoneCommand| replace:: :class:`DoneCommand`
.. |DoneGetContext| replace:: :class:`DoneGetContext`
.. |DoneLaunch| replace:: :class:`DoneLaunch`
.. |TerminalContext| replace:: :class:`TerminalContext`
.. |TerminalsListener| replace:: :class:`TerminalsListener`

Terminals service provides access to the target OS's terminal login, allows to
start and exit a terminal login, and allows to set the terminal's window size.

If a terminal is launched by this service, its standard input/output streams
are available for client to read/write using |streams| service. Stream type of
such streams is set to ``Terminals``.

Properties
----------
Terminal Context Properties
^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. seealso:: |TerminalContext|, |getProperties|

+-----------------+--------------+--------------------------------------------+
| Name            | Type         | Description                                |
+=================+==============+============================================+
| PROP_ENCODING   | |basestring| | Terminal encoding.                         |
+-----------------+--------------+--------------------------------------------+
| PROP_HEIGHT     | |int|        | Window height size.                        |
+-----------------+--------------+--------------------------------------------+
| PROP_ID         | |basestring| | The TCF context ID.                        |
+-----------------+--------------+--------------------------------------------+
| PROP_PROCESS_ID | |int|        | The process ID of the login process of the |
|                 |              | terminal.                                  |
+-----------------+--------------+--------------------------------------------+
| PROP_PTY_TYPE   | |basestring| | The PTY type.                              |
+-----------------+--------------+--------------------------------------------+
| PROP_STDERR_ID  | |basestring| | Process standard error stream ID.          |
+-----------------+--------------+--------------------------------------------+
| PROP_STDIN_ID   | |basestring| | Process standard input stream ID.          |
+-----------------+--------------+--------------------------------------------+
| PROP_STDOUT_ID  | |basestring| | Process standard output stream ID.         |
+-----------------+--------------+--------------------------------------------+
| PROP_WIDTH      | |int|        | Window width size.                         |
+-----------------+--------------+--------------------------------------------+

Service Methods
---------------
.. autodata:: NAME
.. autoclass:: TerminalsService

addListener
^^^^^^^^^^^
.. automethod:: TerminalsService.addListener

exit
^^^^
.. automethod:: TerminalsService.exit

getContext
^^^^^^^^^^
.. automethod:: TerminalsService.getContext

getName
^^^^^^^
.. automethod:: TerminalsService.getName

launch
^^^^^^
.. automethod:: TerminalsService.launch

removeListener
^^^^^^^^^^^^^^
.. automethod:: TerminalsService.removeListener

setWinSize
^^^^^^^^^^
.. automethod:: TerminalsService.setWinSize

Callback Classes
----------------
DoneCommand
^^^^^^^^^^^
.. autoclass:: DoneCommand
    :members:

DoneGetContext
^^^^^^^^^^^^^^
.. autoclass:: DoneGetContext
    :members:

DoneLaunch
^^^^^^^^^^
.. autoclass:: DoneLaunch
    :members:

Listener
--------
.. autoclass:: TerminalsListener
    :members:

Helper Classes
--------------
TerminalContext
^^^^^^^^^^^^^^^
.. autoclass:: TerminalContext
    :members:
"""

from .. import services

NAME = "Terminals"
"""Terminals service name."""

# Context property names.
PROP_ID = "ID"
PROP_PROCESS_ID = "ProcessID"
PROP_PTY_TYPE = "PtyType"
PROP_ENCODING = "Encoding"
PROP_WIDTH = "Width"
PROP_HEIGHT = "Height"
PROP_STDIN_ID = "StdInID"
PROP_STDOUT_ID = "StdOutID"
PROP_STDERR_ID = "StdErrID"


class TerminalContext(object):
    """Terminal context object."""

    def __init__(self, props):
        self._props = props or {}

    def __str__(self):
        return "[Terminals Context %s]" % str(self._props)

    def getID(self):
        """Get context ID.

        :returns: A |basestring| representing the TCF ID of this terminal, or
                  an empty string if it is not known.
        """
        return self._props.get(PROP_ID, '')

    def getProcessID(self):
        """Get process ID of the login process of the terminal.

        :returns: A |basestring| representing the process ID of this terminal,
                  or an empty string if it is not known.
        """
        return self._props.get(PROP_PROCESS_ID, '')

    def getPtyType(self):
        """Get terminal PTY type.

        :returns: A |basestring| representing the PTY type of this terminal, or
                  an empty string if it is not known.
        """
        return self._props.get(PROP_PTY_TYPE, '')

    def getEncoding(self):
        """Get terminal encoding.

        :returns: A |basestring| representing the encoding of this terminal, or
                  an empty string if it is not known.
        """
        return self._props.get(PROP_ENCODING, '')

    def getWidth(self):
        """Get terminal width.

        Terminal width is the number of characters printable on one line in the
        terminal.

        :returns: An |int| representing the width of this terminal, or **0**
                  if it is not known.
        """
        return self._props.get(PROP_WIDTH, 0)

    def getHeight(self):
        """Get Terminal height.

        Terminal height is the number of lines printable in the terminal.

        :returns: An |int| representing the height of this terminal, or **0**
                  if it is not known.
        """
        return self._props.get(PROP_HEIGHT, 0)

    def getStdErrID(self):
        """Get standard error stream ID of the terminal.

        :returns: A |basestring| representing the standard error stream ID of
                  this terminal, or an empty string if it is not known.
        """
        return self._props.get(PROP_STDERR_ID, '')

    def getStdInID(self):
        """Get standard input stream ID of the terminal.

        :returns: A |basestring| representing the standard input stream ID of
                  this terminal, or an empty string if it is not known.
        """
        return self._props.get(PROP_STDIN_ID, '')

    def getStdOutID(self):
        """Get standard output stream ID of the terminal.

        :returns: A |basestring| representing the standard output stream ID of
                  this terminal, or an empty string if it is not known.
        """
        return self._props.get(PROP_STDOUT_ID, '')

    def getProperties(self):
        """Get all available context properties.

        :returns: A |dict| of properties definit this system monitor context.

        .. seealso:: `Terminal Context Properties`_
        """
        return self._props

    def exit(self, done):  # @ReservedAssignment
        """Exit the terminal.

        :param done: Call back interface called when operation is completed.
        :type done: |DoneCommand|

        :returns: Pending command handle, can be used to cancel the command.
        """
        raise NotImplementedError("Abstract method")


class TerminalsService(services.Service):
    """TCF terminals service interface"""

    def getName(self):
        """Get this service name.

        :returns: A |basestring| representing this service name, which is the
                  value of :const:`NAME`
        """
        return NAME

    def getContext(self, contextID, done):
        """Retrieve context info for given context ID.

        A context corresponds to an terminal.

        Context IDs are valid across TCF services, so it is allowed to issue
        |getContext| command with a context that was obtained, for example,
        from |memory| service.

        However, |getContext| is supposed to return only terminal specific
        data, if the ID is not a terminal ID,|getContext| may not return any
        useful information

        :param contextID: TCF ID of the terminal context to get.
        :type contextID: |basestring|
        :param done: Call back interface called when operation is completed.
        :type done: |DoneGetContext|

        :returns: Pending command handle, can be used to cancel the command.
        """
        raise NotImplementedError("Abstract method")

    def launch(self, termType, encoding, environment, done):
        """Launch a new terminal to remote machine.

        :param termType: Requested terminal type for the new terminal.
        :type termType: |basestring| or **None**
        :param encoding: Requested encoding for the new terminal.
        :type encoding: |basestring| or **None**
        :param environment: Array of environment variable strings. If **None**
                            then default set of environment variables will be
                            used.
        :type environment: |dict|
        :param done: Call back interface called when operation is completed.
        :type done: |DoneLaunch|

        :returns: Pending command handle, can be used to cancel the command.
        """
        raise NotImplementedError("Abstract method")

    def setWinSize(self, context_id, newWidth, newHeight, done):
        """Set the terminal windows size.

        :param context_id: TCF ID of the terminal to set size for.
        :type context_id: |basestring|
        :param newWidth: New terminal width.
        :type newWidth: |int|
        :param newHeight: New terminal height.
        :type newHeight: |int|
        :param done: Call back interface called when operation is completed.
        :type done: |DoneCommand|

        :returns: Pending command handle, can be used to cancel the command.
        """
        raise NotImplementedError("Abstract method")

    def exit(self, context_id, done):  # @ReservedAssignment
        """Exit a terminal.

        :param context_id: TCF ID of the terminal to terminate.
        :type context_id: |basestring|
        :param done: Call back interface called when operation is completed.
        :type done: |DoneCommand|

        :returns: Pending command handle, can be used to cancel the command.
        """
        raise NotImplementedError("Abstract method")

    def addListener(self, listener):
        """Add terminals service event listener.

        :param listener: Terminal event listener implementation to add to
                         channel.
        :type listener: |TerminalsListener|

        :returns: **None**, always.
        """
        raise NotImplementedError("Abstract method")

    def removeListener(self, listener):
        """Remove terminals service event listener.

        :param listener: Terminal event listener implementation to remove from
                         channel.
        :type listener: |TerminalsListener|

        :returns: **None**, always.
        """
        raise NotImplementedError("Abstract method")


class DoneGetContext(object):
    """Client call back interface for |getContext|."""

    def doneGetContext(self, token, error, context):
        """Called when contexts data retrieval is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param context: Retrieved context data.
        :type context: |TerminalContext| or **None**
        """
        pass


class DoneCommand(object):
    """Client call back interface for |exit| or |setWinSize|."""

    def doneCommand(self, token, error):
        """Called when command is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        """
        pass


class DoneLaunch(object):
    """Client call back interface for |launch|."""

    def doneLaunch(self, token, error, terminal):
        """Called when terminal launch is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param terminal: Started terminal context.
        :type terminal: |TerminalContext|
        """
        pass


class TerminalsListener(object):
    """Terminals event listener is notified when a terminal exits or is
    resized.

    Events are reported only for terminals that were started by |launch|
    command.
    """

    def exited(self, terminal_id, exit_code):
        """Called when a terminal exits.

        :param terminal_id: TCF ID of the exited terminal.
        :type terminal_id: |basestring|
        :param exit_code: Terminal exit code.
        :type exit_code: |int|

        :returns: **None**, always.
        """
        pass

    def winSizeChanged(self, terminal_id, newWidth, newHeight):
        """Called when a terminal has been resized.

        :param terminal_id: TCF ID of the resized terminal.
        :type terminal_id: |basestring|
        :param newWidth: New terminal width.
        :type newWidth: |int|
        :param newHeight: New terminal height.
        :type newHeight: |int|

        :returns: **None**, always.
        """
        pass
