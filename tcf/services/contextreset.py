# *****************************************************************************
# * Copyright (c) 2019.
# * All rights reserved. This program and the accompanying materials
# * are made available under the terms of the Eclipse Public License 2.0
# * which accompanies this distribution, and is available at
# * https://www.eclipse.org/legal/epl-2.0/
# *****************************************************************************

"""TCF ContextReset service interface.

ContextReset Properties
-----------------------
Parameters
^^^^^^^^^^
+------------------+--------------+-------------------------------------------+
| Name             | Type         | Description                               |
+==================+==============+===========================================+
| PARAM_SUSPEND    | |bool|       | If **true**, the context should be        |
|                  |              | suspended after reset.                    |
+------------------+--------------+-------------------------------------------+

Capabilities
^^^^^^^^^^^^
+------------------------+--------------+-------------------------------------+
| Name                   | Type         | Description                         |
+========================+==============+=====================================+
| CAPABILITY_TYPE        | |str|        | The name of the reset.              |
+------------------------+--------------+-------------------------------------+
| CAPABILITY_DESCRIPTION | |str|        | Brief description of the reset      |
+------------------------+--------------+-------------------------------------+
| CAPABILITY_SUSPEND     | |bool|       | If **True**, context suspend is     |
|                        |              | supported.                          |
+------------------------+--------------+-------------------------------------+

Service Methods
---------------
.. autodata:: NAME
.. autoclass:: ContextResetService

reset
^^^^^
.. automethod:: ContextResetService.reset

getCapabilities
^^^^^^^^^^^^^^^
.. automethod:: ContextResetService.getCapabilities

Callback Classes
----------------
DoneReset
^^^^^^^^^
.. autoclass:: DoneReset
    :members:

DoneGetCapabilities
^^^^^^^^^^^^^^^^^^^
.. autoclass:: DoneGetCapabilities
    :members:
"""

from .. import services

NAME = "ContextReset"
"""ContextReset service name."""

CAPABILITY_TYPE = "Type"
CAPABILITY_DESCRIPTION = "Description"

# context reset parameters
PARAM_SUSPEND = "Suspend"


class ContextResetService(services.Service):
    def getName(self):
        """Get this service name.

        :returns: The value of string :const:`NAME`
        """
        return NAME

    def getCapabilities(self, context_id, done):
        """Retrieve context reset service capabilities a given context-id.

        :param context_id: a context ID, usually one returned by Run Control
                            or Memory services.
        :param done: command result call back object.
        :type done: :class:`DoneGetCapabilities`

        :returns: pending command handle.
        """
        raise NotImplementedError("Abstract method")

    def reset(self, context_id, type, params, done):
        """Reset a specified context.

        :param context_id: a context ID, usually one returned by Run Control.
        :param type: the reset type.
        :param params: parameteres to control the reset.
        :param done: command result call back object.
        :type done: :class:`DoneReset`

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


class DoneReset(object):
    """Call back interface for 'reset' command."""
    def doneReset(self, token, error):
        """Called when reset is done.

        :param token: command handle.
        :param error: error object or None.
        """
        pass
