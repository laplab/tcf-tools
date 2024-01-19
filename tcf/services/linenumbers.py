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

"""Line numbers service associates locations in the source files with the
corresponding machine instruction addresses in the executable object.

Service Methods
---------------
.. autodata:: NAME
.. autoclass:: LineNumbersService

getName
^^^^^^^
.. automethod:: LineNumbersService.getName

mapToMemory
^^^^^^^^^^^
.. automethod:: LineNumbersService.mapToMemory

mapToSource
^^^^^^^^^^^
.. automethod:: LineNumbersService.mapToSource

Callback Classes
----------------
DoneMapToMemory
^^^^^^^^^^^^^^^
.. autoclass:: DoneMapToMemory
    :members:

DoneMapToSource
^^^^^^^^^^^^^^^
.. autoclass:: DoneMapToSource
    :members:

Helper Classes
--------------
CodeArea
^^^^^^^^
.. autoclass:: CodeArea
    :members:
"""

from .. import services

NAME = "LineNumbers"
"""LineNumbers service name."""


class CodeArea(object):
    """A CodeArea represents a continues area in source text mapped to
    continues range of code addresses.

    Line and columns are counted starting from 1.

    File name can be a relative path, in this case the client should use the
    CodeArea directory name as origin for the path.

    File and directory names are valid on a host where code was compiled.

    It is client responsibility to map names to local host file system.
    """
    def __init__(self, directory, file, start_line,  # @ReservedAssignment
                 start_column, end_line, end_column, start_address,
                 end_address, isa, is_statement, basic_block, prologue_end,
                 epilogue_begin):
        self.directory = directory
        self.file = file
        self.start_line = start_line
        self.start_column = start_column
        self.end_line = end_line
        self.end_column = end_column
        self.start_address = start_address
        self.end_address = end_address
        self.isa = isa
        self.is_statement = is_statement
        self.basic_block = basic_block
        self.prologue_end = prologue_end
        self.epilogue_begin = epilogue_begin

    def __eq__(self, o):
        if self is o:
            return True
        if not isinstance(o, CodeArea):
            return False
        if self.start_line != o.start_line:
            return False
        if self.start_column != o.start_column:
            return False
        if self.end_line != o.end_line:
            return False
        if self.end_column != o.end_column:
            return False
        if self.isa != o.isa:
            return False
        if self.is_statement != o.is_statement:
            return False
        if self.basic_block != o.basic_block:
            return False
        if self.prologue_end != o.prologue_end:
            return False
        if self.epilogue_begin != o.epilogue_begin:
            return False
        if self.start_address != o.start_address:
            return False
        if self.end_address != o.end_address:
            return False
        if self.file != o.file:
            return False
        if self.directory != o.directory:
            return False
        return True

    def __hash__(self):
        h = 0
        if self.file:
            h += hash(self.file)
        return h + self.start_line + self.start_column + self.end_line + \
            self.end_column

    def __str__(self):
        res = '['
        if self.directory:
            res += str(self.directory) + ':'
        if self.file:
            res += str(self.file) + ':'
        res += str(self.start_line)
        if self.start_column:
            res += '.' + str(self.start_column)
        res += '..' + str(self.end_line)
        if self.end_column:
            res += '.' + str(self.end_column)
        res += ' -> '
        if self.start_address:
            res += '0x' + str(hex(self.start_address))
        else:
            res += '0'
        res += '..'
        if self.end_address:
            res += '0x' + str(hex(self.end_address))
        else:
            res += '0'
        if self.isa:
            res += ',isa ' + str(self.isa)
        if self.is_statement:
            res += ',statement'
        if self.basic_block:
            res += ',basic block'
        if self.prologue_end:
            res += ',prologue end'
        if self.epilogue_begin:
            res += ',epilogue begin'
        res += ']'
        return res


class LineNumbersService(services.Service):
    """TCF LineNumbers service interface."""

    def getName(self):
        """Get this service name.

        :returns: The value of string :const:`NAME`
        """
        return NAME

    def mapToSource(self, context_id, start_address, end_address, done):
        """Get the line numbers source for a context ID and a memory address.

        :param context_id: ID of the context to get source map for.
        :type context_id: |basestring|
        :param start_address: Memory start address to get source map for.
        :type start_address: |int|
        :param end_address: Memory end address to get source map for.
        :type end_address: |int|
        :param done: Call back interface called when operation is completed
        :type done: :class:`DoneMapToSource`
        """
        raise NotImplementedError("Abstract method")

    def mapToMemory(self, context_id, fileName, line, column, done):
        """Get the the memory address of a context ID for a given file and line
        number.

        :param context_id: ID of the context to get source map for.
        :type context_id: |basestring|
        :param fileName: Name of the file to map memory for.
        :type fileName: |basestring|
        :param line: Source file line to map to a memory address.
        :type line: |int|
        :param column: Source file column to map to a memory address.
        :type column: |int|
        :param done: Call back interface called when operation is completed.
        :type done: :class:`DoneMapToMemory`
        """
        raise NotImplementedError("Abstract method")


class DoneMapToSource(object):
    """
    Client callback interface for :meth:`~LineNumbersService.mapToSource`.
    """

    def doneMapToSource(self, token, error, areas):
        """Called when context data retrieval is done.

        :param token: pending command handle
        :param error: error description if operation failed, **None** if
                      succeeded.
        :param areas: A |list| of :class:`CodeArea` objects.
        """
        pass


class DoneMapToMemory(object):
    """
    Client callback interface for :meth:`~LineNumbersService.mapToMemory`.
    """
    def doneMapToMemory(self, token, error, areas):
        """Called when context data retrieval is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param areas: A |list| of :class:`CodeArea` objects.
        """
        pass
