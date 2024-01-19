# *****************************************************************************
# * Copyright (c) 2014, 2016 Wind River Systems, Inc. and others.
# * All rights reserved. This program and the accompanying materials
# * are made available under the terms of the Eclipse Public License 2.0
# * which accompanies this distribution, and is available at
# * https://www.eclipse.org/legal/epl-2.0/
# *
# * Contributors:
# *     Wind River Systems - initial API and implementation
# *****************************************************************************

"""TCF DPrintf service interface.

Service Methods
---------------
.. autodata:: NAME
.. autoclass:: DPrintfService

getName
^^^^^^^
.. automethod:: DPrintfService.getName

open
^^^^^^^^^^^
.. automethod:: DPrintfService.open

close
^^^^^^^^^^^
.. automethod:: DPrintfService.close

"""

from .. import services

NAME = "DPrintf"
"""DPrintf service name."""


class DPrintfService(services.Service):
    def getName(self):
        """Get this service name.

        :returns: The value of string :const:`NAME`
        """
        return NAME

    def open(self):
        """Open a virtual stream to get DPrintf output.

        :returns: The ID of the stream :basestring: `stream_id`
        """
        raise NotImplementedError("Abstract method")

    def close(self):
        """Close DPrintf virtual stream opened by this client.

        :returns: Pending command handle, can be used to cancel the command.
        """
        raise NotImplementedError("Abstract method")


class DoneOpen(object):
    """Call back interface for 'open' command."""
    def doneOpen(self, token, error, stream_id):
        """Called when DPrintf open is done.

        :param token: command handle.
        :param error: error object or None.
        :param stream_id: ID of the DPrintf stream.
        """
        pass


class DoneClose(object):
    """Call back interface for |close| command."""

    def doneClose(self, token, error):
        """Called when DPrintf close is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        """
        pass
