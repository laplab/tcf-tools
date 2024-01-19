# *****************************************************************************
# * Copyright (c) 2011, 2013-2014, 2016 Wind River Systems, Inc. and others.
# * All rights reserved. This program and the accompanying materials
# * are made available under the terms of the Eclipse Public License 2.0
# * which accompanies this distribution, and is available at
# * https://www.eclipse.org/legal/epl-2.0/
# *
# * Contributors:
# *     Wind River Systems - initial API and implementation
# ****************************************************************************

"""File System service provides file transfer (and more generally file
system access) functionality in TCF.

.. |close| replace:: :meth:`~FileSystemService.close`
.. |copy| replace:: :meth:`~FileSystemService.copy`
.. |doneRead| replace:: :meth:`~DoneRead.doneRead`
.. |fstat| replace:: :meth:`~FileSystemService.fstat`
.. |fsetstat| replace:: :meth:`~FileSystemService.fsetstat`
.. |lstat| replace:: :meth:`~FileSystemService.lstat`
.. |mkdir| replace:: :meth:`~FileSystemService.mkdir`
.. |open| replace:: :meth:`~FileSystemService.open`
.. |opendir| replace:: :meth:`~FileSystemService.opendir`
.. |read| replace:: :meth:`~FileSystemService.read`
.. |readdir| replace:: :meth:`~FileSystemService.readdir`
.. |readlink| replace:: :meth:`~FileSystemService.readlink`
.. |realpath| replace:: :meth:`~FileSystemService.realpath`
.. |remove| replace:: :meth:`~FileSystemService.remove`
.. |rename| replace:: :meth:`~FileSystemService.rename`
.. |rmdir| replace:: :meth:`~FileSystemService.rmdir`
.. |roots| replace:: :meth:`~FileSystemService.roots`
.. |setstat| replace:: :meth:`~FileSystemService.setstat`
.. |stat| replace:: :meth:`~FileSystemService.stat`
.. |symlink| replace:: :meth:`~FileSystemService.symlink`
.. |user| replace:: :meth:`~FileSystemService.user`
.. |write| replace:: :meth:`~FileSystemService.write`
.. |DoneClose| replace:: :class:`DoneClose`
.. |DoneCopy| replace:: :class:`DoneCopy`
.. |DoneMkDir| replace:: :class:`DoneMkDir`
.. |DoneOpen| replace:: :class:`DoneOpen`
.. |DoneRead| replace:: :class:`DoneRead`
.. |DoneReadDir| replace:: :class:`DoneReadDir`
.. |DoneReadLink| replace:: :class:`DoneReadLink`
.. |DoneRealPath| replace:: :class:`DoneRealPath`
.. |DoneRemove| replace:: :class:`DoneRemove`
.. |DoneRename| replace:: :class:`DoneRename`
.. |DoneRoots| replace:: :class:`DoneRoots`
.. |DoneSetStat| replace:: :class:`DoneSetStat`
.. |DoneStat| replace:: :class:`DoneStat`
.. |DoneSymLink| replace:: :class:`DoneSymLink`
.. |DoneUser| replace:: :class:`DoneUser`
.. |DoneWrite| replace:: :class:`DoneWrite`
.. |FileAttrs| replace:: :class:`FileAttrs`
.. |FileHandle| replace:: :class:`FileHandle`

The service design is derived from SSH File Transfer Protocol specifications.

Request Synchronization and Reordering
--------------------------------------
The protocol and implementations **must** process requests relating to the same
file in the order in which they are received.  In other words, if an
application submits multiple requests to the server, the results in the
responses will be the same as if it had sent the requests one at a time and
waited for the response in each case.  For example, the server may process
non-overlapping read/write requests to the same file in parallel, but
overlapping reads and writes cannot be reordered or parallelized.  However,
there are no ordering restrictions on the server for processing requests from
two different file transfer connections.  The server may interleave and
parallelize them at will.

There are no restrictions on the order in which responses to outstanding
requests are delivered to the client, except that the server must ensure
fairness in the sense that processing of no request will be indefinitely
delayed even if the client is sending other requests so that there are multiple
outstanding requests all the time.

There is no limit on the number of outstanding (non-acknowledged) requests that
the client may send to the server.  In practice this is limited by the
buffering available on the data stream and the queuing performed by the server.
If the server's queues are full, it should not read any more data from the
stream, and flow control will prevent the client from sending more requests.

File Names
----------
This protocol represents file names as strings.  File names are assumed to use
the slash (``/``) character as a directory separator.

File names starting with a slash are **absolute**, and are relative to the root
of the file system.  Names starting with any other character are relative to
the user's default directory (home directory). Client can use
:meth:`~FileSystemService.user` command to retrieve current user home
directory.

Servers **should** interpret a path name component ``..`` as referring to the
parent directory, and ``.`` as referring to the current directory. If the
server implementation limits access to certain parts of the file system, it
must be extra careful in parsing file names when enforcing such restrictions.
There have been numerous reported security bugs where a ``..`` in a path name
has allowed access outside the intended area.

An empty path name is valid, and it refers to the user's default directory
(usually the user's home directory).

Otherwise, no syntax is defined for file names by this specification.

Clients should not make any other assumptions however, they can splice path
name components returned by :meth:`~FileSystemService.readdir` together using a
slash (``/``) as the separator, and that will work as expected.

FileSystem Properties
---------------------
Attributes
^^^^^^^^^^
Flags to be used together with |FileAttrs|.
The flags specify which of the fields are present.  Those fields for which the
corresponding flag is not set are not present (not included in the message).
Aff flags are of type |int|.

+------------------+----------------------------------------------------------+
| Name             | Description                                              |
+==================+==========================================================+
| ATTR_ACMODTIME   | The access and modification times of the file are        |
|                  | present in the |FileAttrs| object.                       |
+------------------+----------------------------------------------------------+
| ATTR_PERMISSIONS | The file permissons are present in the |FileAttrs|       |
|                  | objects.                                                 |
+------------------+----------------------------------------------------------+
| ATTR_SIZE        | File size is present in the |FileAttrs| object.          |
+------------------+----------------------------------------------------------+
| ATTR_UIDGID      | User ID and Group ID are present in the |FileAttrs|      |
|                  | object.                                                  |
+------------------+----------------------------------------------------------+

Status
^^^^^^
Status error codes are of type |int|.

+--------------------------+--------------------------------------------------+
| Name                     | Description                                      |
+==========================+==================================================+
| STATUS_EOF               | Indicates end-of-file condition for |read|. It   |
|                          | means that no more data is available in the file,|
|                          | and for |readdir| it indicates that no more files|
|                          | are contained in the directory.                  |
+--------------------------+--------------------------------------------------+
| STATUS_NO_SUCH_FILE      | This code is returned when a reference is made to|
|                          | a file which should exist but doesn't.           |
+--------------------------+--------------------------------------------------+
| STATUS_PERMISSION_DENIED | This code is returned when the authenticated user|
|                          | does not have sufficient permissions to perform  |
|                          | the operation.                                   |
+--------------------------+--------------------------------------------------+

Permissions
^^^^^^^^^^^
File permission is an ored value of the following |int| values:

+----------+-------------------------------------------------+
| Name     | Description                                     |
+==========+=================================================+
| S_IFBLK  | Block device.                                   |
+----------+-------------------------------------------------+
| S_IFCHR  | Character device.                               |
+----------+-------------------------------------------------+
| S_IFDIR  | Directory.                                      |
+----------+-------------------------------------------------+
| S_IFIFO  | Fifo.                                           |
+----------+-------------------------------------------------+
| S_IFLNK  | Symbolic link.                                  |
+----------+-------------------------------------------------+
| S_IFMT   | Bitmask for the file type bitfields.            |
+----------+-------------------------------------------------+
| S_IFREG  | Regular file.                                   |
+----------+-------------------------------------------------+
| S_IFSOCK | Socket.                                         |
+----------+-------------------------------------------------+
| S_IRGRP  | Group has read permission.                      |
+----------+-------------------------------------------------+
| S_IROTH  | Others have read permission.                    |
+----------+-------------------------------------------------+
| S_IRUSR  | Owner has read permission.                      |
+----------+-------------------------------------------------+
| S_IRWXG  | Mask for group permissions.                     |
+----------+-------------------------------------------------+
| S_IRWXO  | Mask for permissions for others (not in group). |
+----------+-------------------------------------------------+
| S_IRWXU  | Mask for file owner permissions.                |
+----------+-------------------------------------------------+
| S_ISGID  | Set GID bit.                                    |
+----------+-------------------------------------------------+
| S_ISUID  | Set UID bit.                                    |
+----------+-------------------------------------------------+
| S_ISVTX  | Sticky bit.                                     |
+----------+-------------------------------------------------+
| S_IWGRP  | Group has write permission.                     |
+----------+-------------------------------------------------+
| S_IWOTH  | Others have write permission.                   |
+----------+-------------------------------------------------+
| S_IWUSR  | Owner has write permission.                     |
+----------+-------------------------------------------------+
| S_IXGRP  | Group has execute permission.                   |
+----------+-------------------------------------------------+
| S_IXOTH  | Others have execute permission.                 |
+----------+-------------------------------------------------+
| S_IXUSR  | Owner has execute permission.                   |
+----------+-------------------------------------------------+

Open Flags
^^^^^^^^^^
Flags to be used with the |open| method. All flags are of type |int|.

+--------------+--------------------------------------------------------------+
| Name         | Description                                                  |
+==============+==============================================================+
| TCF_O_APPEND | Force all writes to append data at the end of the file.      |
| TCF_O_CREAT  | If this flag is specified, then a new file will be created   |
|              | if one does not already exist (if **TCF_O_TRUNC** is         |
|              | specified, the new file will be truncated to zero length if  |
|              | it previously exists).                                       |
+--------------+--------------------------------------------------------------+
| TCF_O_EXCL   | Causes the request to fail if the named file already exists. |
|              | **TCF_O_CREAT** **must** also be specified if this flag is   |
|              | used.                                                        |
+--------------+--------------------------------------------------------------+
| TCF_O_READ   | Open the file for reading.                                   |
+--------------+--------------------------------------------------------------+
| TCF_O_TRUNC  | Forces an existing file with the same name to be truncated   |
|              | to zero length when creating a file by specifying            |
|              | **TCF_O_CREAT**. **TCF_O_CREAT** **must** also be specified  |
|              | if this flag is used.                                        |
+--------------+--------------------------------------------------------------+
| TCF_O_WRITE  | Open the file for writing. If both this and **TCF_O_READ**   |
|              | are specified, the file is opened for both reading and       |
|              | writing.                                                     |
+--------------+--------------------------------------------------------------+

Service Methods
---------------
.. autodata:: NAME
.. autoclass:: FileSystemService

close
^^^^^
.. automethod:: FileSystemService.close

copy
^^^^
.. automethod:: FileSystemService.copy

fsetstat
^^^^^^^^
.. automethod:: FileSystemService.fsetstat

fstat
^^^^^
.. automethod:: FileSystemService.fstat

getName
^^^^^^^
.. automethod:: FileSystemService.getName

lstat
^^^^^
.. automethod:: FileSystemService.lstat

mkdir
^^^^^
.. automethod:: FileSystemService.mkdir

open
^^^^
.. automethod:: FileSystemService.open

opendir
^^^^^^^
.. automethod:: FileSystemService.opendir

read
^^^^
.. automethod:: FileSystemService.read

readdir
^^^^^^^
.. automethod:: FileSystemService.readdir

readlink
^^^^^^^^
.. automethod:: FileSystemService.readlink

realpath
^^^^^^^^
.. automethod:: FileSystemService.realpath

remove
^^^^^^
.. automethod:: FileSystemService.remove

rename
^^^^^^
.. automethod:: FileSystemService.rename

rmdir
^^^^^
.. automethod:: FileSystemService.rmdir

roots
^^^^^
.. automethod:: FileSystemService.roots

setstat
^^^^^^^
.. automethod:: FileSystemService.setstat

stat
^^^^
.. automethod:: FileSystemService.stat

symlink
^^^^^^^
.. automethod:: FileSystemService.symlink

user
^^^^
.. automethod:: FileSystemService.user

write
^^^^^
.. automethod:: FileSystemService.write

Callback Classes
----------------
DoneClose
^^^^^^^^^
.. autoclass:: DoneClose
    :members:

DoneCopy
^^^^^^^^
.. autoclass:: DoneCopy
    :members:

DoneMkDir
^^^^^^^^^
.. autoclass:: DoneMkDir
    :members:

DoneOpen
^^^^^^^^
.. autoclass:: DoneOpen
    :members:

DoneRead
^^^^^^^^
.. autoclass:: DoneRead
    :members:

DoneReadDir
^^^^^^^^^^^
.. autoclass:: DoneReadDir
    :members:

DoneReadLink
^^^^^^^^^^^^
.. autoclass:: DoneReadLink
    :members:

DoneRealPath
^^^^^^^^^^^^
.. autoclass:: DoneRealPath
    :members:

DoneRemove
^^^^^^^^^^
.. autoclass:: DoneRemove
    :members:

DoneRename
^^^^^^^^^^
.. autoclass:: DoneRename
    :members:

DoneRoots
^^^^^^^^^
.. autoclass:: DoneRoots
    :members:

DoneSetStat
^^^^^^^^^^^
.. autoclass:: DoneSetStat
    :members:

DoneStat
^^^^^^^^
.. autoclass:: DoneStat
    :members:

DoneSymLink
^^^^^^^^^^^
.. autoclass:: DoneSymLink
    :members:

DoneUser
^^^^^^^^
.. autoclass:: DoneUser
    :members:

DoneWrite
^^^^^^^^^
.. autoclass:: DoneWrite
    :members:

Helper Classes
--------------
DirEntry
^^^^^^^^
.. autoclass:: DirEntry
    :members:

FileAttrs
^^^^^^^^^
.. autoclass:: FileAttrs
    :members:

FileHandle
^^^^^^^^^^
.. autoclass:: FileHandle
    :members:

FileSystemException
^^^^^^^^^^^^^^^^^^^
.. autoclass:: FileSystemException
    :members:
"""

from .. import services

NAME = "FileSystem"
"""FileSystem service name."""

# Flags to be used with open() method.

TCF_O_READ = 0x00000001
TCF_O_WRITE = 0x00000002
TCF_O_APPEND = 0x00000004
TCF_O_CREAT = 0x00000008
TCF_O_TRUNC = 0x00000010
TCF_O_EXCL = 0x00000020

ATTR_SIZE = 0x00000001
ATTR_UIDGID = 0x00000002
ATTR_PERMISSIONS = 0x00000004
ATTR_ACMODTIME = 0x00000008


class FileAttrs(object):
    """FileAttrs is used both when returning file attributes from the server
    and when sending file attributes to the server.

    When sending it to the server, the flags field specifies which attributes
    are included, and the server will use default values for the remaining
    attributes (or will not modify the values of remaining attributes). When
    receiving attributes from the server, the flags specify which attributes
    are included in the returned data.  The server normally returns all
    attributes it knows about.

    :param flags: Specifies which of the fields are present. See `Attributes`_.
    :type flags: |int|
    :param size: Specifies the size of the file in bytes.
    :type size: |int|
    :param uid: Contains numeric Unix-like user identifiers.
    :type uid: |int|
    :param gid: Contains numeric Unix-like group identifiers.
    :type gid: |int|
    :param permissions: Contains a bit mask of file permissions as defined by
                        posix.
    :type permissions: |int|
    :param atime: Contains the access time of the file. It is represented as
                  milliseconds from midnight Jan 1, 1970 in UTC.
    :type atime: |int|
    :param mtime: Contains the modification time of the file. It is represented
                  as milliseconds from midnight Jan 1, 1970 in UTC
    :type mtime: |int|
    :param attributes: Contains additional (non-standard) attributes.
    :type attributes: |dict|

    **Fields**
        - **flags** : Specifies which fields are present (see `Attributes`_).
        - **size** : File size in bytes.
        - **uid** : User ID (|int|)
        - **gid** : Group ID (|int|)
        - **permissions** : File permissions (see `Permissions`_).
        - **atime** : Last access time.
        - **mtime** : Last modification time.
        - **attributes** : A |dict| of non-standard attributes.
    """
    def __init__(self, flags, size, uid, gid, permissions, atime, mtime,
                 attributes):
        self.flags = flags
        self.size = size
        self.uid = uid
        self.gid = gid
        self.permissions = permissions
        self.atime = atime
        self.mtime = mtime
        self.attributes = attributes

    def __repr__(self):
        """Representation for these file attributes."""
        res = self.__class__.__name__ + '('
        res += 'flags=' + str(self.flags)
        res += ', size=' + str(self.size)
        res += ', uid=' + str(self.uid)
        res += ', gid=' + str(self.gid)
        res += ', permissions=' + str(self.permissions)
        res += ', atime=' + str(self.atime)
        res += ', mtime=' + str(self.mtime)
        res += ', attributes=' + str(self.attributes)
        res += ')'
        return res

    def __str__(self):
        """String representation for these file attributes."""
        res = self.__class__.__name__ + ' ['
        flags = []

        if self.flags & ATTR_SIZE:
            flags.append('ATTR_SIZE')
        if self.flags & ATTR_UIDGID:
            flags.append('ATTR_UIDGID')
        if self.flags & ATTR_PERMISSIONS:
            flags.append('ATTR_PERMISSIONS')
        if self.flags & ATTR_ACMODTIME:
            flags.append('ATTR_ACMODTIME')

        res += 'flags=' + '|'.join(flags)

        if self.flags & ATTR_SIZE:
            res += ', size=' + str(self.size)

        if self.flags & ATTR_UIDGID:
            res += ', uid=' + str(self.uid)
            res += ', gid=' + str(self.gid)

        # Compute the permissions string

        if self.flags & ATTR_PERMISSIONS:
            perms = []
            if self.permissions & S_IFMT:
                perms.append('S_IFMT')
            if self.permissions & S_IFSOCK:
                perms.append('S_IFSOCK')
            if self.permissions & S_IFLNK:
                perms.append('S_IFLNK')
            if self.permissions & S_IFREG:
                perms.append('S_IFREG')
            if self.permissions & S_IFBLK:
                perms.append('S_IFBLK')
            if self.permissions & S_IFDIR:
                perms.append('S_IFDIR')
            if self.permissions & S_IFCHR:
                perms.append('S_IFCHR')
            if self.permissions & S_IFIFO:
                perms.append('S_IFIFO')
            if self.permissions & S_ISUID:
                perms.append('S_ISUID')
            if self.permissions & S_ISGID:
                perms.append('S_ISGID')
            if self.permissions & S_ISVTX:
                perms.append('S_ISVTX')
            if self.permissions & S_IRWXU:
                perms.append('S_IRWXU')
            if self.permissions & S_IRUSR:
                perms.append('S_IRUSR')
            if self.permissions & S_IWUSR:
                perms.append('S_IWUSR')
            if self.permissions & S_IXUSR:
                perms.append('S_IXUSR')
            if self.permissions & S_IRWXG:
                perms.append('S_IRWXG')
            if self.permissions & S_IRGRP:
                perms.append('S_IRGRP')
            if self.permissions & S_IWGRP:
                perms.append('S_IWGRP')
            if self.permissions & S_IXGRP:
                perms.append('S_IXGRP')
            if self.permissions & S_IRWXO:
                perms.append('S_IRWXO')
            if self.permissions & S_IROTH:
                perms.append('S_IROTH')
            if self.permissions & S_IWOTH:
                perms.append('S_IWOTH')
            if self.permissions & S_IXOTH:
                perms.append('S_IXOTH')

            res += ', permissions=' + '|'.join(perms)

        if self.flags & ATTR_ACMODTIME:
            res += ', atime=' + str(self.atime)
            res += ', mtime=' + str(self.mtime)

        res += ', attributes=' + str(self.attributes)
        res += ']'
        return res

    def isFile(self):
        """Determines if the file system object is a file on the remote file
        system.

        :returns: **True** if and only if the object on the remote system can
                  be considered to have *contents* that have the potential to
                  be read and written as a byte stream.
        """
        if (self.flags & ATTR_PERMISSIONS) == 0:
            return False
        return (self.permissions & S_IFMT) == S_IFREG

    def isDirectory(self):
        """Determines if the file system object is a directory on the remote
        file system.

        :returns: True if and only if the object on the remote system is a
                  directory. That is, it contains entries that can be
                  interpreted as other files.
        """
        if (self.flags & ATTR_PERMISSIONS) == 0:
            return False
        return (self.permissions & S_IFMT) == S_IFDIR

    def __eq__(self, other):
        if not isinstance(other, FileAttrs):
            return False
        return (self.flags == other.flags and self.size == other.size and
                self.uid == other.uid and self.gid == other.gid and
                self.permissions == other.permissions and
                self.mtime == other.mtime and
                self.attributes == other.attributes)

    def __ne__(self, other):
        return (not self.__eq__(other))


# The following flags are defined for the 'permissions' field:
S_IFMT = 0o170000
S_IFSOCK = 0o140000
S_IFLNK = 0o120000
S_IFREG = 0o100000
S_IFBLK = 0o060000
S_IFDIR = 0o040000
S_IFCHR = 0o020000
S_IFIFO = 0o010000
S_ISUID = 0o004000
S_ISGID = 0o002000
S_ISVTX = 0o001000
S_IRWXU = 0o0700
S_IRUSR = 0o0400
S_IWUSR = 0o0200
S_IXUSR = 0o0100
S_IRWXG = 0o0070
S_IRGRP = 0o0040
S_IWGRP = 0o0020
S_IXGRP = 0o0010
S_IRWXO = 0o0007
S_IROTH = 0o0004
S_IWOTH = 0o0002
S_IXOTH = 0o0001


class DirEntry(object):
    """Directory entry.

    :param filename: Is a file name being returned. It is a relative name
                     within the directory, without any path components.
    :type filename: |basestring|
    :param longname: Is an expanded format for the file name, similar to what
                     is returned by ``ls -l`` on Unix systems. The format of
                     the *longname* parameter is unspecified by this protocol.
                     It **must** be suitable for use in the output of a
                     directory listing command (in fact, the recommended
                     operation for a directory listing command is to simply
                     display this data).  However, clients **should not**
                     attempt to parse the longname field for file attributes
                     they **should** use the *attrs* field instead.
    :type longname: |basestring|
    :param attrs: Directory entry attributes.
    :type attrs: |FileAttrs|
    """
    def __init__(self, filename, longname, attrs):
        self.filename = filename
        self.longname = longname
        self.attrs = attrs


class FileHandle(object):
    """TCF filesystem file handle.

    :param service: The TCF file system this service is associated to.
    :param fileID: The file ID of this file handle.
    :type fileID: |basestring|
    """
    def __init__(self, service, fileID):
        self.service = service
        self.id = fileID

    def getID(self):
        """Get the ID of this handle.

        :returns: The ID of this file handle
        """
        return (self.id)

    def getService(self):
        """Get the TCF filesystem service for this handle.

        :returns: The TCF filesystem service this file hanlde is associated to
        """
        return self.service

    def __str__(self):
        return "[File Handle '%s']" % self.id

# Service specific error codes.

STATUS_EOF = 0x10001
STATUS_NO_SUCH_FILE = 0x10002
STATUS_PERMISSION_DENIED = 0x10003


class FileSystemException(IOError):
    """The class to represent File System error reports.

    :param message_or_exception: A string describing the file system error, or
                                 an :exc:`~exceptions.Exception` to
                                 initialise this exception with
    """
    def __init__(self, message_or_exception):
        if isinstance(message_or_exception, str):
            super(FileSystemException, self).__init__(message_or_exception)
        elif isinstance(message_or_exception, Exception):
            self.caused_by = message_or_exception

    def getStatus(self):
        """Get error code.

        The code can be standard TCF error code or one of service specific
        codes, see `Status`_.

        :returns: This Exception error code.
        """
        raise NotImplementedError("Abstract methods")


class FileSystemService(services.Service):
    """TCF filesystem service interface"""

    def getName(self):
        """Get this service name.

        :returns: This service name, which is the value of :const:`NAME`
        """
        return NAME

    def open(self, file_name, flags, attrs, done):  # @ReservedAssignment
        """Open or create a file on a remote system.

        :param file_name: Specifies the file name.  See **File Names** for more
                          information.
        :type file_name: |basestring|
        :param flags: Is a bit mask of `Open Flags`_.
        :type flags: |int|
        :param attrs: Specifies the initial attributes for the file. Default
                      values will be used for those attributes that are not
                      specified.
        :type attrs: |FileAttrs|
        :param done: Is call back object.
        :type done: |DoneOpen|

        :returns: Pending command handle.
        """
        raise NotImplementedError("Abstract methods")

    def close(self, handle, done):
        """Close a file on a remote system.

        :param handle: Is a handle previously returned in the response to
                       |open| or |opendir|.
        :type handle: |FileHandle|
        :param done: is call back object.
        :type done: |DoneClose|

        :returns: Pending command handle.
        """
        raise NotImplementedError("Abstract methods")

    def read(self, handle, offset, length, done):
        """Read bytes from an open file.

        In response to this request, the server will read as many bytes as it
        can from the file (up to *length*), and return them in a byte array.

        If an error occurs or **EOF** is encountered, the server may return
        fewer bytes than requested. Call back method |doneRead| argument
        *error* will not be **None** in case of error, and argument *eof* will
        be **True** in case of **EOF**.

        For normal disk files, it is guaranteed that this will read the
        specified number of bytes, or up to end of file or error. For e.g.
        device files this may return fewer bytes than requested.

        :param handle: Is an open file handle returned by |open|.
        :type handle: |FileHandle|
        :param offset: Is the offset (in bytes) relative to the beginning of
                       the file from where to start reading. If offset
                       negative, then reading starts from current position in
                       the file.
        :type offset: |int|
        :param length: Is the maximum number of bytes to read.
        :type length: |int|
        :param done: Is call back object.
        :type done: |DoneRead|

        :returns: Pending command handle.
        """
        raise NotImplementedError("Abstract methods")

    def write(self, handle, offset, data, data_pos, data_size, done):
        """Write bytes into an open file.

        The write will extend the file if writing beyond the end of the file.

        It is legal to write way beyond the end of the file the semantics
        are to write zeroes from the end of the file to the specified offset
        and then the data.

        :param handle: Is an open file handle returned by |open|.
        :type handle: |FileHandle|
        :param offset: The offset (in bytes) relative to the beginning of the
                       file from where to start writing. If offset is negative
                       then writing starts from current position in the file.
        :type offset: |int|
        :param data: Byte array that contains data for writing.
        :type data: |bytearray|
        :param data_pos: Offset in *data* of first byte to write.
        :type data_pos: |int|
        :param data_size: Number of bytes to write.
        :type data_size: |int|
        :param done: Call back object.
        :type done: |DoneWrite|

        :returns: Pending command handle.
        """
        raise NotImplementedError("Abstract methods")

    def stat(self, path, done):
        """Retrieve file attributes.

        :param path: Specifies the file system object for which status is to be
                     returned.
        :type path: |basestring|
        :param done: Call back object.
        :type done: |DoneStat|

        :returns: Pending command handle.
        """
        raise NotImplementedError("Abstract methods")

    def lstat(self, path, done):
        """Retrieve file attributes.

        Unlike |stat|, |lstat| does not follow symbolic links.

        :param path: Specifies the file system object for which status is to be
                     returned.
        :type path: |basestring|
        :param done: Call back object
        :type done: |DoneStat|

        :returns: Pending command handle.
        """
        raise NotImplementedError("Abstract methods")

    def fstat(self, handle, done):
        """Retrieve file attributes for an open file (identified by the file
        handle).

        :param handle: A file handle returned by |open|.
        :type handle: |FileHandle|
        :param done: Call back object.
        :type done: |DoneStat|

        :returns: Pending command handle.
        """
        raise NotImplementedError("Abstract methods")

    def setstat(self, path, attrs, done):
        """Set file attributes.

        This request is used for operations such as changing the ownership,
        permissions or access times, as well as for truncating a file.

        An error will be returned if the specified file system object does
        not exist or the user does not have sufficient rights to modify the
        specified attributes.

        :param path: Specifies the file system object (e.g. file or directory)
                     whose attributes are to be modified.
        :type path: |basestring|
        :param attrs: Modifications to be made to file attributes.
        :type attrs: |FileAttrs|
        :param done: Call back object.
        :type done: |DoneSetStat|

        :returns: Pending command handle.
        """
        raise NotImplementedError("Abstract methods")

    def fsetstat(self, handle, attrs, done):
        """Set file attributes for an open file (identified by the file
        handle).

        This request is used for operations such as changing the ownership,
        permissions or access times, as well as for truncating a file.

        :param handle: is a file handle returned by |open|.
        :type handle: |FileHandle|
        :param attrs: Modifications to be made to file attributes.
        :type attrs: |FileAttrs|
        :param done: Call back object.
        :type done: |DoneSetStat|

        :returns: Pending command handle.
        """
        raise NotImplementedError("Abstract methods")

    def opendir(self, path, done):
        """This command opens a directory for reading.

        Once the directory has been successfully opened, files (and
        directories) contained in it can be listed using |readdir| requests.

        When the client no longer wishes to read more names from the directory,
        it **should** call |close| for the handle. The handle should be closed
        regardless of whether an error has occurred or not.

        :param path: Name of the directory to be listed (without any trailing
                     slash).
        :type path: |basestring|
        :param done: Call back object.
        :type done: |DoneOpen|

        :returns: Pending command handle.
        """
        raise NotImplementedError("Abstract methods")

    def readdir(self, handle, done):
        """The files in a directory can be listed using the |opendir| and
        |readdir| requests.

        Each |readdir| request returns one or more file names with full file
        attributes for each file. The client should call |readdir| repeatedly
        until it has found the file it is looking for or until the server
        responds with a message indicating an error or end of file. The client
        should then close the handle using the |close| request.

        .. note:: directory entries ``.`` and ``..`` are **not** included into
                  |readdir| response.

        :param handle: File handle created by |opendir|.
        :type handle: |FileHandle|
        :param done: Call back object.
        :type done: |DoneReadDir|

        :returns: Pending command handle.
        """
        raise NotImplementedError("Abstract methods")

    def mkdir(self, path, attrs, done):
        """Create a directory on the server.

        :param path: Specifies the directory to be created.
        :type path: |basestring|
        :param attrs: New directory attributes.
        :type attrs: |FileAttrs|
        :param done: Call back object.
        :type done: |DoneMkDir|

        :returns: Pending command handle.
        """
        raise NotImplementedError("Abstract methods")

    def rmdir(self, path, done):
        """Remove a directory.

        An error will be returned if no directory with the specified path
        exists, or if the specified directory is not empty, or if the path
        specified a file system object other than a directory.

        :param path: Specifies the directory to be removed.
        :type path: |basestring|
        :param done: Call back object
        :type done: |DoneRemove|

        :returns: pending command handle
        """
        raise NotImplementedError("Abstract methods")

    def roots(self, done):
        """Retrieve file system roots - top level file system objects.

        UNIX file system can report just one root with path ``/``. Other types
        of systems can have more the one root. For example, Windows server can
        return multiple roots: one per disc (e.g. ``/C:/``, ``/D:/``, etc.).

        .. note:: even Windows implementation of the service must use forward
                  slash as directory separator, and must start absolute path
                  with ``/``. Server should implement proper translation of
                  protocol file names to OS native names and back.

        :param done: Call back object
        :type done: |DoneRoots|

        :returns: Pending command handle.
        """
        raise NotImplementedError("Abstract methods")

    def remove(self, file_name, done):
        """Remove a file or symbolic link.

        This request cannot be used to remove directories.

        :param file_name: The name of the file to be removed.
        :type file_name: |basestring|
        :param done: Call back object.
        :type done: |DoneRemove|

        :returns: Pending command handle.
        """
        raise NotImplementedError("Abstract methods")

    def realpath(self, path, done):
        """Canonicalize any given path name to an absolute path.

        This is useful for converting path names containing ``..`` components
        or relative pathnames without a leading slash into absolute paths.

        :param path: The path name to be canonicalized.
        :type path: |basestring|
        :param done: Call back object.
        :type done: |DoneRealPath|

        :returns: pending command handle.
        """
        raise NotImplementedError("Abstract methods")

    def rename(self, old_path, new_path, done):
        """Rename a file.

        It is an error if there already exists a file with the name specified
        by *new_path*.  The server may also fail rename requests in other
        situations, for example if *old_path* and *new_path* point to different
        file systems on the server.

        :param old_path: The name of an existing file or directory.
        :type old_path: |basestring|
        :param new_path: The new name for the file or directory.
        :type new_path: |basestring|
        :param done: Call back object.
        :type done: |DoneRename|

        :returns: Pending command handle.
        """
        raise NotImplementedError("Abstract methods")

    def readlink(self, path, done):
        """Read the target of a symbolic link.

        :param path: The path name of the symbolic link to be read.
        :type path: |basestring|
        :param done: Call back object.
        :type done: |DoneReadLink|

        :returns: Pending command handle.
        """
        raise NotImplementedError("Abstract methods")

    def symlink(self, link_path, target_path, done):
        """Create a symbolic link on the server.

        :param link_path: The path name of the symbolic link to be created.
        :type link_path: |basestring|
        :param target_path: The target of the symbolic link.
        :type target_path: |basestring|
        :param done: Call back object.
        :type done: |DoneSymLink|

        :returns: Pending command handle.
        """
        raise NotImplementedError("Abstract methods")

    def copy(self, src_path, dst_path, copy_permissions, copy_ownership, done):
        """Copy a file on remote system.

        :param src_path: The path name of the file to be copied.
        :type src_path: |basestring|
        :param dst_path: Destination file name.
        :type dst_path: |basestring|
        :param copy_permissions: If **True** then copy source file permissions.
        :type copy_permissions: |bool|
        :param copy_ownership: If **True** then copy source file UID and GID.
        :type copy_ownership: |bool|
        :param done: Call back object.
        :type done: |DoneCopy|

        :returns: Pending command handle.
        """
        raise NotImplementedError("Abstract methods")

    def user(self, done):
        """Retrieve information about user account, which is used by server
        to access file system on behalf of the client.

        :param done: Call back object
        :type done: |DoneUser|

        :returns: Pending command handle.
        """
        raise NotImplementedError("Abstract methods")


class DoneOpen(object):
    """Client call back interface for |open|."""

    def doneOpen(self, token, error, handle):
        """Called when file open is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param handle: Handle of the opened file.
        :type handle: |FileHandle|
        """
        pass


class DoneClose(object):
    """Client call back interface for |close|."""

    def doneClose(self, token, error):
        """Called when file close is done.

        :param token: Pending command handle
        :param error: Error description if operation failed, **None** if
                      succeeded.
        """
        pass


class DoneRead(object):
    """Client call back interface for |read|."""

    def doneRead(self, token, error, data, eof):
        """Called when file read is done.

        :param token: {ending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param data: data read from file.
        :type data: |bytearray|
        :param eof: **True** if end of file is reached by this read action.
        :type eof: |bool|
        """
        pass


class DoneWrite(object):
    """Client call back interface for |write|."""

    def doneWrite(self, token, error):
        """Called when file write is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        """
        pass


class DoneStat(object):
    """Client call back interface for |stat|, |fstat| or |lstat| methods."""

    def doneStat(self, token, error, attrs):
        """Called when file stat is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param attrs: Retrieved file attributes.
        :type attrs: |FileAttrs|
        """
        pass


class DoneSetStat(object):
    """Client call back interface for |setstat| or |fsetstat|.
    """

    def doneSetStat(self, token, error):
        """Called when file stat is set.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        """
        pass


class DoneReadDir(object):
    """Client call back interface for |readdir|."""

    def doneReadDir(self, token, error, entries, eof):
        """Called when directory read is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param entries: Entries in directory.
        :type entries: |list|
        :param eof: **True** if there are no more entries in that directory.
        :type eof: |bool|
        """
        pass


class DoneMkDir(object):
    """Client call back interface for |mkdir|."""

    def doneMkDir(self, token, error):
        """Called when mkdir command is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        """
        pass


class DoneRemove(object):
    """Client call back interface for |remove| or |rmdir|.
    """

    def doneRemove(self, token, error):
        """Called when rmdir or remove command is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        """
        pass


class DoneRoots(object):
    """Client call back interface for |roots|."""

    def doneRoots(self, token, error, entries):
        """Called when filesystem roots are retrieved.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param entries: A list of roots of the filesystem.
        :type entries: |list|
        """
        pass


class DoneRealPath(object):
    """Client call back interface for |realpath|."""

    def doneRealPath(self, token, error, path):
        """Called when realpath command is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param path: Real path of the input file path.
        :type path: |basestring|
        """
        pass


class DoneRename(object):
    """Client call back interface for |rename|."""

    def doneRename(self, token, error):
        """Called when rename command is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        """
        pass


class DoneReadLink(object):
    """Client call back interface for |readlink|."""

    def doneReadLink(self, token, error, path):
        """Called when readlink command is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param path: Target path of the input link path.
        :type path: |basestring|
        """
        pass


class DoneSymLink(object):
    """Client call back interface for |symlink|."""

    def doneSymLink(self, token, error):
        """Called when symlink command is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        """
        pass


class DoneCopy(object):
    """Client call back interface for |copy|."""

    def doneCopy(self, token, error):
        """Called when copy command is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        """
        pass


class DoneUser(object):
    """Client call back interface for |user|."""

    def doneUser(self, token, error, real_uid, effective_uid, real_gid,
                 effective_gid, home):
        """Called when user command is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param real_uid: real user ID.
        :type real_uid: |int|
        :param effective_uid: effective user ID.
        :type effective_uid: |int|
        :param real_gid: user's real group ID.
        :type real_gid: |int|
        :param effective_gid: user's effective group ID
        :type effective_gid: |int|
        :param home: user's home path.
        :type home: |basestring|
        """
        pass
