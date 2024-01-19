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

"""MemoryMap service provides information about executable modules (files)
mapped (loaded) into target memory.

.. |contextquery| replace:: :mod:`~tcf.services.contextquery`
.. |get| replace:: :meth:`~MemoryMapService.get`
.. |set| replace:: :meth:`~MemoryMapService.set`
.. |DoneGet| replace:: :class:`DoneGet`
.. |DoneSet| replace:: :class:`DoneSet`
.. |MemoryMapListener| replace:: :class:`MemoryMapListener`
.. |MemoryRegion| replace:: :class:`MemoryRegion`


Memory Map Properties
---------------------
Properties
^^^^^^^^^^
+--------------------+--------------+-----------------------------------------+
| Name               | Type         | Description                             |
+====================+==============+=========================================+
| PROP_ADDRESS       | |int|        | Region address in memory.               |
+--------------------+--------------+-----------------------------------------+
| PROP_BSS           | |bool|       | **True** if the region represents BSS.  |
+--------------------+--------------+-----------------------------------------+
| PROP_CONTEXT_QUERY | |basestring| | Memory region context query.            |
+--------------------+--------------+-----------------------------------------+
| PROP_FILE_NAME     | |basestring| | Name of the file.                       |
+--------------------+--------------+-----------------------------------------+
| PROP_FLAGS         | |int|        | Region memory protection flags, see     |
|                    |              | `Flags`_.                               |
+--------------------+--------------+-----------------------------------------+
| PROP_ID            | |basestring| | Memory region ID.                       |
+--------------------+--------------+-----------------------------------------+
| PROP_OFFSET        | |int|        | Region offset in the file.              |
+--------------------+--------------+-----------------------------------------+
| PROP_SECTION_NAME  | |basestring| | Name of the object file section.        |
+--------------------+--------------+-----------------------------------------+
| PROP_SIZE          | |int|        | Region size.                            |
+--------------------+--------------+-----------------------------------------+

Flags
^^^^^
All flags are of type |int|.

+--------------+--------------------------------------------------------------+
| Name         | Description                                                  |
+==============+==============================================================+
| FLAG_EXECUTE | Instruction fetch access is allowed.                         |
+--------------+--------------------------------------------------------------+
| FLAG_READ    | Read access is allowed.                                      |
+--------------+--------------------------------------------------------------+
| FLAG_WRITE   | Write access is allowed.                                     |
+--------------+--------------------------------------------------------------+

Service Methods
---------------
.. autodata:: NAME
.. autoclass:: MemoryMapService

addListener
^^^^^^^^^^^
.. automethod:: MemoryMapService.addListener

get
^^^
.. automethod:: MemoryMapService.get

getName
^^^^^^^
.. automethod:: MemoryMapService.getName

removeListener
^^^^^^^^^^^^^^
.. automethod:: MemoryMapService.removeListener

set
^^^
.. automethod:: MemoryMapService.set

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
MemoryMapListener
^^^^^^^^^^^^^^^^^
.. autoclass:: MemoryMapListener
    :members:

Helper Classes
--------------
MemoryRegion
^^^^^^^^^^^^
.. autoclass:: MemoryRegion
    :members:
"""

from .. import compat
from .. import services

NAME = "MemoryMap"
"""MemoryMap service name."""

# Memory region property names.

PROP_ADDRESS = "Addr"
PROP_CONTEXT_QUERY = "ContextQuery"
PROP_ID = "ID"
PROP_SIZE = "Size"
PROP_OFFSET = "Offs"
PROP_BSS = "BSS"
PROP_FLAGS = "Flags"
PROP_FILE_NAME = "FileName"
PROP_SECTION_NAME = "SectionName"

# Memory region flags.
FLAG_READ = 1
FLAG_WRITE = 2
FLAG_EXECUTE = 4


class MemoryRegion(object):
    """Memory region object.

     It is possible to check that an address belongs to a memory map with
     code like:

     .. code-block:: python

         # <address> is an integer, <region> is a MemoryRegion object

         if address in region:
             print(address)

    :param props: Properties to initialise memory region with. See
                  `Properties`_.
    :type props: |dict|
    """
    def __init__(self, props):
        self._props = props or {}

    def __contains__(self, address):
        """Check if *address* belongs to this memory region.

        :param address: The address to check.
        :type addess: |int|

        :returns: A |bool| set to **True** if *address* belongs to this memory
                  region, **False** else.
        """
        rAddr = self.getAddress()
        rOffs = self.getOffset()
        rSize = self.getSize()
        if address >= rAddr + rOffs and address < rAddr + rOffs + rSize:
            return True
        return False

    def getProperties(self):
        """Get region properties.

        See `Properties`_ definitions for property names.
        Properties are read only, clients should not try to modify them.

        :returns: A |dict| of memory region properties.
        """
        return (self._props)

    def getAddress(self):
        """Get memory region address.

        :returns: An |int| representing the memory region address.
        """
        return self._props.get(PROP_ADDRESS, 0)

    def getContextQuery(self):
        """Get context query that defines scope of the region.

        Only user-defined regions can have a context query property.

        :returns: A context query expression, or **None**.

        .. seealso:: |contextquery|
        """
        return self._props.get(PROP_CONTEXT_QUERY, None)

    def getSize(self):
        """Get memory region size.

        :returns: An |int| representing the memory region size.
        """
        return self._props.get(PROP_SIZE, 0)

    def getOffset(self):
        """Get memory region file offset.

        :returns: An |int| representing the memory region file offset.
        """
        return self._props.get(PROP_OFFSET, 0)

    def getFlags(self):
        """Get memory region flags.

        See `Flags`_.

        :returns: An |int| representing the memory region flags.
        """
        return self._props.get(PROP_FLAGS, 0)

    def getFileName(self):
        """Get memory region file name.

        :returns: A |basestring| representing the memory region file name.
        """
        return self._props.get(PROP_FILE_NAME, '')

    def getID(self):
        """Get memory region ID.

        :returns: A |basestring| representing this memory region ID.
        """
        return self._props.get(PROP_ID, '')

    def getSectionName(self):
        """Get memory region section name.

        :returns: A |basestring| representing this memory region section name.
        """
        return self._props.get(PROP_SECTION_NAME, '')

    def isBss(self):
        """Check if this memory region represents a BSS section.

        :returns: A |bool| stating if this region is a BSS section
        """
        return (self._props.get(PROP_BSS, False))

    def __json__(self):
        # This makes it serializable using JSON serializer
        return self._props

    def __repr__(self):
        return "MemoryRegion(%s)" % str(self._props)

    def __str__(self):
        """String representation of this Instruction Set Architecture."""
        res = self.__class__.__name__ + '['
        res += PROP_FILE_NAME + '=' + str(self._props.get(PROP_FILE_NAME))
        res += ', ' + PROP_ID + '=' + str(self._props.get(PROP_ID))
        addr = self._props.get(PROP_ADDRESS)
        if isinstance(addr, compat.inttype):
            res += ', ' + PROP_ADDRESS + '=0x{0:08x}'.format(addr)
        elif isinstance(addr, compat.longtype):
            res += ', ' + PROP_ADDRESS + '=0x{0:016x}'.format(addr)
        else:
            res += ', ' + PROP_ADDRESS + '=' + str(addr)
        res += ', ' + PROP_SIZE + '=' + str(self._props.get(PROP_SIZE))
        offset = self._props.get(PROP_OFFSET)
        if isinstance(offset, int):
            res += ', ' + PROP_OFFSET + '=0x{0:x}'.format(offset)
        else:
            res += ', ' + PROP_OFFSET + '=' + str(offset)
        res += ', ' + PROP_SECTION_NAME + '=' + \
               str(self._props.get(PROP_SECTION_NAME))
        res += ', ' + PROP_FLAGS + '='
        flags = self._props.get(PROP_FLAGS)
        if isinstance(flags, int):
            if flags & FLAG_READ:
                res += 'r'
            else:
                res += '-'
            if flags & FLAG_WRITE:
                res += 'w'
            else:
                res += '-'
            if flags & FLAG_EXECUTE:
                res += 'x'
            else:
                res += '-'
        else:
            res += '---'
        res += ', ' + PROP_BSS + '=' + str(self._props.get(PROP_BSS) or False)
        res += ']'
        return res


class MemoryMapService(services.Service):

    def getName(self):
        """Get this service name.

        :returns: The value of string :const:`NAME`
        """
        return NAME

    def get(self, contextID, done):
        """Retrieve memory map for given context ID.

        :param contextID: The context ID of the memory map to retrieve.
        :type contextID: |basestring|
        :param done: Call back interface called when operation is completed.
        :type done: |DoneGet|
        """
        return NotImplementedError("Abstract method")

    def set(self, contextID, memoryMap, done):  # @ReservedAssignment
        """Set memory map for given context ID.

        :param contextID: The context ID of the memory map to set.
        :type contextID: |basestring|
        :param memoryMap: The list of |MemoryRegion| to set.
        :type memoryMap: |list|
        :param done: Call back interface called when operation is completed.
        :type done: |DoneSet|
        """
        return NotImplementedError("Abstract method")

    def addListener(self, listener):
        """Add memory map event listener.

        :param listener: The Memory map event listener to add
        :type listener: |MemoryMapListener|
        """
        return NotImplementedError("Abstract method")

    def removeListener(self, listener):
        """Remove memory map event listener.

        :param listener: The memory map event listener to remove.
        :type listener: |MemoryMapListener|
        """
        return NotImplementedError("Abstract method")


class DoneGet(object):
    """Client call back interface for |get| method."""

    def doneGet(self, token, error, memoryMap):
        """Called when memory map data retrieval is done.

        :param token: Command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param memoryMap: A list of |MemoryRegion| data.
        :type memoryMap: |list|
        """
        pass


class DoneSet(object):
    """Client call back interface for |set| method."""

    def doneSet(self, token, error):
        """Called when memory map set command is done.

        :param token: Command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        """
        pass


class MemoryMapListener(object):
    """Service events listener interface."""

    def changed(self, context_id):
        """Called when context memory map changes.

        :param context_id: Changed context ID.
        :type context_id: |basestring|
        """
        pass
