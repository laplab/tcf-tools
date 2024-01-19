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

"""PathMap service manages file path translation across systems.

.. |get| replace:: :meth:`~PathMapService.get`
.. |set| replace:: :meth:`~PathMapService.set`
.. |DoneGet| replace:: :class:`DoneGet`
.. |DoneSet| replace:: :class:`DoneSet`
.. |PathMapRule| replace:: :class:`PathMapRule`
.. |PathMapListener| replace:: :class:`PathMapListener`
.. |Properties| replace:: :ref:`Tcf-Path-Mapping-Properties`
.. |Protocols| replace:: :ref:`Tcf-Path-Mapping-Protocols`


.. _Tcf-Path-Mapping-Properties:

Path Mapping Properties
-----------------------
Properties
^^^^^^^^^^
All properties are of type |basestring|.

+--------------------+--------------------------------------------------------+
| Name               | Description                                            |
+====================+========================================================+
| PROP_CONTEXT       | Symbols context group ID or name. **deprecated** - use |
|                    | ``PROP_CONTEXT_QUERY``.                                |
+--------------------+--------------------------------------------------------+
| PROP_CONTEXT_QUERY | Contexts query.                                        |
+--------------------+--------------------------------------------------------+
| PROP_DESTINATION   | Destination, or run-time file path.                    |
+--------------------+--------------------------------------------------------+
| PROP_HOST          | Host name.                                             |
+--------------------+--------------------------------------------------------+
| PROP_ID            | Rule ID.                                               |
+--------------------+--------------------------------------------------------+
| PROP_PROTOCOL      | File access protocol, see |Protocols|                  |
+--------------------+--------------------------------------------------------+
| PROP_SOURCE        | Source, or compile-time file path.                     |
+--------------------+--------------------------------------------------------+

.. _Tcf-Path-Mapping-Protocols:

Path Mapping Protocols
^^^^^^^^^^^^^^^^^^^^^^
All protocols are of type |basestring|.

+-----------------+-----------------------------------------------------------+
| Name            | Description                                               |
+=================+===========================================================+
| PROTOCOL_FILE   | Regular file access using system calls.                   |
+-----------------+-----------------------------------------------------------+
| PROTOCOL_HOST   | File should be accessed using File System service on host.|
+-----------------+-----------------------------------------------------------+
| PROTOCOL_TARGET | File should be accessed using File System service on.     |
|                 | target.                                                   |
+-----------------+-----------------------------------------------------------+

Service Methods
---------------
.. autodata:: NAME
.. autoclass:: PathMapService

addListener
^^^^^^^^^^^
.. automethod:: PathMapService.addListener

get
^^^
.. automethod:: PathMapService.get

getName
^^^^^^^
.. automethod:: PathMapService.getName

removeListener
^^^^^^^^^^^^^^
.. automethod:: PathMapService.removeListener

set
^^^
.. automethod:: PathMapService.set

Callback Classes
----------------
DoneGet
^^^^^^^
.. autoclass:: DoneGet
    :members:

DoneSet
^^^^^^^
.. autoclass:: DoneSet
    :members:

Listener
--------
PathMapListener
^^^^^^^^^^^^^^^
.. autoclass:: PathMapListener
    :members:

Helper Classes
--------------
PathMapRule
^^^^^^^^^^^
.. autoclass:: PathMapRule
    :members:
"""

from .. import services

NAME = "PathMap"
"""PathMap service name."""

# Path mapping rule property names.

PROP_CONTEXT_QUERY = "ContextQuery"
PROP_DESTINATION = "Destination"
PROP_HOST = "Host"
PROP_ID = "ID"
PROP_PROTOCOL = "Protocol"
PROP_SOURCE = "Source"

# @deprecated
PROP_CONTEXT = "Context"

# PROP_PROTOCOL values.
PROTOCOL_FILE = "file"
PROTOCOL_HOST = "host"
PROTOCOL_TARGET = "target"


class PathMapListener(object):
    """Pathmap event listener is notified when pathmap changes."""

    def changed(self):
        """Called when a pathmap has been changed."""
        pass


class PathMapRule(object):
    """PathMapRule represents a single file path mapping rule.

    :param props: The properties to initialise this pathmap rule with. See
                  |Properties|.
    :type props: |dict|
    """
    def __init__(self, props):
        self._props = props or {}

    def __repr__(self):
        return self.__class__.__name__ + '(' + str(self._props) + ')'

    def __json__(self):
        return self._props

    def getContextQuery(self):
        """Get context query that defines scope of the mapping rule.

        :returns: This PathMap Rule context query expression, or **None**.
        """
        return self._props.get(PROP_CONTEXT_QUERY, None)

    def getProperties(self):
        """Get rule properties.

        See |Properties| definitions for property names.

        Context properties are read only, clients should not try to modify
        them.

        :returns: A |dict| class of this rule's properties.
        """
        return self._props

    def getID(self):
        """Get rule unique ID.

        :returns: A |basestring| representing this rule's ID or **None**.
        """
        return self._props.get(PROP_ID, None)

    def getSource(self):
        """Get compile-time file path.

        :returns: A |basestring| representing compile-time file path or
                  **None**.
        """
        return self._props.get(PROP_SOURCE, None)

    def getDestination(self):
        """Get run-time file path.

        :returns: A |basestring| representing run-time file path or **None**.
        """
        return self._props.get(PROP_DESTINATION, None)

    def getHost(self):
        """Get host name of this rule.

        :returns: A |basestring| representing the host name this rule applies
                  to or **None**.
        """
        return self._props.get(PROP_HOST, None)

    def getProtocol(self):
        """Get file access protocol name.

        See |Protocols| for path mapping protocol values.

        :returns: A |basestring| representing protocol name or **None**.
        """
        return self._props.get(PROP_PROTOCOL, None)


class PathMapService(services.Service):
    """TCF PathMap service interface."""

    def addListener(self, listener):
        """Add a pathmap listener.

        A |PathMapListener| is added to the TCF pathmap service.

        :param listener: Instance of the pathmap listener to add to service.
        :type listener: |PathMapListener|
        """
        return NotImplementedError("Abstract method")

    def getName(self):
        """Get this service name.

        :returns: The value of string :const:`NAME`
        """
        return NAME

    def get(self, done):
        """Retrieve file path mapping rules.

        :param done: Call back interface called when operation is completed.
        :type done: |DoneGet|
        """
        return NotImplementedError("Abstract method")

    def set(self, pathMap, done):  # @ReservedAssignment
        """Set file path mapping rules.

        :param pathMap: File path mapping rules.
        :type pathMap: |PathMapRule|
        :param done: Call back interface called when operation is completed.
        :type done: |DoneSet|
        """
        return NotImplementedError("Abstract method")

    def removeListener(self, listener):
        """Remove pathmap event listener.

        The PathMapListener is removed from the TCF pathmap service.

        :param listener: instance of the pathmap listener to remove from
                         service.
        :type listener: |PathMapListener|
        """
        return NotImplementedError("Abstract method")


class DoneGet(object):
    """Client call back interface for |get|."""
    def doneGet(self, token, error, pathMap):
        """Called when file path mapping retrieval is done.

        :param token: Command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param pathMap: File path mapping data.
        :type pathMap: |list| of |PathMapRule|
        """
        pass


class DoneSet(object):
    """Client call back interface for |set|."""

    def doneSet(self, token, error):
        """Called when file path mapping transmission is done.

        :param token: Command handle
        :param error: Error description if operation failed, **None** if
                      succeeded.
        """
        pass
