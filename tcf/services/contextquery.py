# *****************************************************************************
# * Copyright (c) 2012-2014 Wind River Systems, Inc. and others.
# * All rights reserved. This program and the accompanying materials
# * are made available under the terms of the Eclipse Public License 2.0
# * which accompanies this distribution, and is available at
# * https://www.eclipse.org/legal/epl-2.0/
# *
# * Contributors:
# *     Wind River Systems - initial API and implementation
# *****************************************************************************

"""TCF ContextQuery service interface.

.. |getAttrNames| replace:: :meth:`ContextQueryService.getAttrNames`
.. |query| replace:: :meth:`ContextQueryService.query`
.. |DoneGetAttrNames| replace:: :class:`DoneGetAttrNames`
.. |DoneQuery| replace:: :class:`DoneQuery`

Service Methods
---------------
.. autodata:: NAME
.. autoclass:: ContextQueryService

getAttrNames
^^^^^^^^^^^^
.. automethod:: ContextQueryService.getAttrNames

getName
^^^^^^^
.. automethod:: ContextQueryService.getName

query
^^^^^
.. automethod:: ContextQueryService.query

Callback Classes
----------------
DoneGetAttrNames
^^^^^^^^^^^^^^^^
.. autoclass:: DoneGetAttrNames
    :members:

DoneQuery
^^^^^^^^^
.. autoclass:: DoneQuery
    :members:
"""

from .. import services

NAME = "ContextQuery"
"""ContextQuery service name."""


class ContextQueryService(services.Service):
    """TCF context query service interface."""

    def getName(self):
        """Get this service name.

        :returns: A |basestring| representing this service name, which is the
                  value of :const:`NAME`
        """
        return NAME

    def query(self, querystr, done):
        """Get the list of contexts matching a given query.

        :param querystr: Context query to be executed.
        :type querystr: |basestring|
        :param done: Command result call back object.
        :type done: |DoneQuery|

        :returns: Pending command handle.
        """
        raise NotImplementedError("Abstract method")

    def getAttrNames(self, done):
        """Get the list of Attributes registered with the context query
        service.

        :param done: Command result call back object.
        :type done: |DoneGetAttrNames|

        :return: Pending command handle.
        """
        raise NotImplementedError("Abstract method")


class DoneQuery(object):
    "Call back interface for |query| command."

    def doneQuery(self, token, error, ctxList):
        """Called when |query| command is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param ctxList: IDs of contexts matching the query.
        :type ctxList: |list|
        """
        pass


class DoneGetAttrNames(object):
    "Call back interface for |getAttrNames| command."

    def doneGetAttrNames(self, token, error, attrNameList):
        """Called when |getAttrNames| command is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param attrNameList: List of the attributes supported by the agent.
        :type attrNamesList: |list|
        """
        pass
