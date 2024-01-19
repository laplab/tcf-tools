# *****************************************************************************
# * Copyright (c) 2011, 2013, 2016 Wind River Systems, Inc. and others.
# * All rights reserved. This program and the accompanying materials
# * are made available under the terms of the Eclipse Public License 2.0
# * which accompanies this distribution, and is available at
# * https://www.eclipse.org/legal/epl-2.0/
# *
# * Contributors:
# *     Wind River Systems - initial API and implementation
# *****************************************************************************

from .. import filesystem
from ... import errors, channel
from ...channel.Command import Command


class Status(filesystem.FileSystemException):
    def __init__(self, status_or_exception, message=None, attrs=None):
        if isinstance(status_or_exception, int):
            super(Status, self).__init__(message)
            self.status = status_or_exception
            self.attrs = attrs
        else:
            super(Status, self).__init__(status_or_exception)
            self.status = errors.TCF_ERROR_OTHER
            self.attrs = {}

    def getStatus(self):
        return self.status

    def getErrorCode(self):
        return self.attrs.get(errors.ERROR_CODE, 0)

    def getAltCode(self):
        return self.attrs.get(errors.ERROR_ALT_CODE, 0)

    def getAltOrg(self):
        return self.attrs.get(errors.ERROR_ALT_ORG)

    def getAttributes(self):
        return self.attrs


class FileSystemCommand(Command):
    def __init__(self, service, command, args):
        super(FileSystemCommand, self).__init__(service.channel, service,
                                                command, args)

    def _toSFError(self, data):
        if data is None:
            return None
        error_code = data.get(errors.ERROR_CODE)
        cmd = self.getCommandString()
        if len(cmd) > 72:
            cmd = cmd[0:72] + "..."
        s = Status(error_code,
                   "TCF command exception:" +
                   "\nCommand: " + cmd +
                   "\nException: " + errors.toErrorString(data) +
                   "\nError code: " + str(error_code), data)
        caused_by = data.get(errors.ERROR_CAUSED_BY)
        if caused_by is not None:
            s.initCause(self.toError(caused_by, False))
        return s


class FileSystemProxy(filesystem.FileSystemService):
    def __init__(self, channel):
        self.channel = channel

    def close(self, handle, done):
        assert handle.getService() is self
        done = self._makeCallback(done)
        _id = handle.id
        service = self

        class CloseCommand(FileSystemCommand):
            def __init__(self):
                super(CloseCommand, self).__init__(service, "close", (_id,))

            def done(self, error, args):
                s = None
                if error:
                    s = Status(error)
                else:
                    assert len(args) == 1
                    s = self._toSFError(args[0])
                done.doneClose(self.token, s)
        return CloseCommand().token

    def setstat(self, path, attrs, done):
        done = self._makeCallback(done)
        dt = _toObject(attrs)
        service = self

        class SetStatCommand(FileSystemCommand):
            def __init__(self):
                super(SetStatCommand, self).__init__(service, "setstat",
                                                     (path, dt))

            def done(self, error, args):
                s = None
                if error:
                    s = Status(error)
                else:
                    assert len(args) == 1
                    s = self._toSFError(args[0])
                done.doneSetStat(self.token, s)
        return SetStatCommand().token

    def fsetstat(self, handle, attrs, done):
        done = self._makeCallback(done)
        assert handle.getService() is self
        _id = handle.id
        dt = _toObject(attrs)
        service = self

        class FSetStatCommand(FileSystemCommand):
            def __init__(self):
                super(FSetStatCommand, self).__init__(service, "fsetstat",
                                                      (_id, dt))

            def done(self, error, args):
                s = None
                if error:
                    s = Status(error)
                else:
                    assert len(args) == 1
                    s = self._toSFError(args[0])
                done.doneSetStat(self.token, s)
        return FSetStatCommand().token

    def stat(self, path, done):
        done = self._makeCallback(done)
        service = self

        class StatCommand(FileSystemCommand):
            def __init__(self):
                super(StatCommand, self).__init__(service, "stat", (path,))

            def done(self, error, args):
                s = None
                a = None
                if error:
                    s = Status(error)
                else:
                    assert len(args) == 2
                    s = self._toSFError(args[0])
                    if not s:
                        a = _toFileAttrs(args[1])
                done.doneStat(self.token, s, a)
        return StatCommand().token

    def fstat(self, handle, done):
        done = self._makeCallback(done)
        assert handle.getService() is self
        _id = handle.id
        service = self

        class FStatCommand(FileSystemCommand):
            def __init__(self):
                super(FStatCommand, self).__init__(service, "fstat", (_id,))

            def done(self, error, args):
                s = None
                a = None
                if error:
                    s = Status(error)
                else:
                    assert len(args) == 2
                    s = self._toSFError(args[0])
                    if not s:
                        a = _toFileAttrs(args[1])
                done.doneStat(self.token, s, a)
        return FStatCommand().token

    def lstat(self, path, done):
        done = self._makeCallback(done)
        service = self

        class LStatCommand(FileSystemCommand):
            def __init__(self):
                super(LStatCommand, self).__init__(service, "lstat", (path,))

            def done(self, error, args):
                s = None
                a = None
                if error:
                    s = Status(error)
                else:
                    assert len(args) == 2
                    s = self._toSFError(args[0])
                    if not s:
                        a = _toFileAttrs(args[1])
                done.doneStat(self.token, s, a)
        return LStatCommand().token

    def mkdir(self, path, attrs, done):
        done = self._makeCallback(done)
        dt = _toObject(attrs)
        service = self

        class MkDirCommand(FileSystemCommand):
            def __init__(self):
                super(MkDirCommand, self).__init__(service, "mkdir",
                                                   (path, dt,))

            def done(self, error, args):
                s = None
                if error:
                    s = Status(error)
                else:
                    assert len(args) == 1
                    s = self._toSFError(args[0])
                done.doneMkDir(self.token, s)
        return MkDirCommand().token

    def open(self, file_name, flags, attrs, done):
        done = self._makeCallback(done)
        dt = _toObject(attrs)
        service = self

        class OpenCommand(FileSystemCommand):
            def __init__(self):
                super(OpenCommand, self).__init__(service, "open",
                                                  (file_name, flags, dt))

            def done(self, error, args):
                s = None
                h = None
                if error:
                    s = Status(error)
                else:
                    assert len(args) == 2
                    s = self._toSFError(args[0])
                    if not s:
                        h = service._toFileHandle(args[1])
                done.doneOpen(self.token, s, h)
        return OpenCommand().token

    def opendir(self, path, done):
        done = self._makeCallback(done)
        service = self

        class OpenDirCommand(FileSystemCommand):
            def __init__(self):
                super(OpenDirCommand, self).__init__(service, "opendir",
                                                     (path,))

            def done(self, error, args):
                s = None
                h = None
                if error:
                    s = Status(error)
                else:
                    assert len(args) == 2
                    s = self._toSFError(args[0])
                    if not s:
                        h = service._toFileHandle(args[1])
                done.doneOpen(self.token, s, h)
        return OpenDirCommand().token

    def read(self, handle, offset, length, done):
        assert handle.getService() is self
        done = self._makeCallback(done)
        handleID = handle.id
        service = self

        class ReadCommand(FileSystemCommand):
            def __init__(self):
                super(ReadCommand, self).__init__(service, "read",
                                                  (handleID, offset, length))

            def done(self, error, args):
                s = None
                b = None
                eof = False
                if error:
                    s = Status(error)
                else:
                    assert len(args) == 3
                    s = self._toSFError(args[1])
                    if not s:
                        b = channel.toByteArray(args[0])
                        eof = args[2]
                done.doneRead(self.token, s, b, eof)
        return ReadCommand().token

    def readdir(self, handle, done):
        assert handle.getService() is self
        done = self._makeCallback(done)
        _id = handle.id
        service = self

        class ReadDirCommand(FileSystemCommand):
            def __init__(self):
                super(ReadDirCommand, self).__init__(service, "readdir",
                                                     (_id,))

            def done(self, error, args):
                s = None
                b = None
                eof = False
                if error:
                    s = Status(error)
                else:
                    assert len(args) == 3
                    s = self._toSFError(args[1])
                    if not s:
                        b = _toDirEntryArray(args[0])
                        eof = args[2]
                done.doneReadDir(self.token, s, b, eof)
        return ReadDirCommand().token

    def roots(self, done):
        done = self._makeCallback(done)
        service = self

        class RootCommand(FileSystemCommand):
            def __init__(self):
                super(RootCommand, self).__init__(service, "roots", None)

            def done(self, error, args):
                s = None
                b = None
                if error:
                    s = Status(error)
                else:
                    assert len(args) == 2
                    s = self._toSFError(args[1])
                    if not s:
                        b = _toDirEntryArray(args[0])
                done.doneRoots(self.token, s, b)
        return RootCommand().token

    def readlink(self, path, done):
        done = self._makeCallback(done)
        service = self

        class ReadLinkCommand(FileSystemCommand):
            def __init__(self):
                super(ReadLinkCommand, self).__init__(service, "readlink",
                                                      (path,))

            def done(self, error, args):
                s = None
                p = None
                if error:
                    s = Status(error)
                else:
                    assert len(args) == 2
                    s = self._toSFError(args[0])
                    if not s:
                        p = args[1]
                done.doneReadLink(self.token, s, p)
        return ReadLinkCommand().token

    def realpath(self, path, done):
        done = self._makeCallback(done)
        service = self

        class RealPathCommand(FileSystemCommand):
            def __init__(self):
                super(RealPathCommand, self).__init__(service, "realpath",
                                                      (path,))

            def done(self, error, args):
                s = None
                p = None
                if error:
                    s = Status(error)
                else:
                    assert len(args) == 2
                    s = self._toSFError(args[0])
                    if not s:
                        p = args[1]
                done.doneRealPath(self.token, s, p)
        return RealPathCommand().token

    def remove(self, file_name, done):
        done = self._makeCallback(done)
        service = self

        class RemoveCommand(FileSystemCommand):
            def __init__(self):
                super(RemoveCommand, self).__init__(service, "remove",
                                                    (file_name,))

            def done(self, error, args):
                s = None
                if error:
                    s = Status(error)
                else:
                    assert len(args) == 1
                    s = self._toSFError(args[0])
                done.doneRemove(self.token, s)
        return RemoveCommand().token

    def rename(self, old_path, new_path, done):
        done = self._makeCallback(done)
        service = self

        class RenameCommand(FileSystemCommand):
            def __init__(self):
                super(RenameCommand, self).__init__(service, "rename",
                                                    (old_path, new_path))

            def done(self, error, args):
                s = None
                if error:
                    s = Status(error)
                else:
                    assert len(args) == 1
                    s = self._toSFError(args[0])
                done.doneRename(self.token, s)
        return RenameCommand().token

    def rmdir(self, path, done):
        done = self._makeCallback(done)
        service = self

        class RmDirCommand(FileSystemCommand):
            def __init__(self):
                super(RmDirCommand, self).__init__(service, "rmdir", (path,))

            def done(self, error, args):
                s = None
                if error:
                    s = Status(error)
                else:
                    assert len(args) == 1
                    s = self._toSFError(args[0])
                done.doneRemove(self.token, s)
        return RmDirCommand().token

    def symlink(self, link_path, target_path, done):
        done = self._makeCallback(done)
        service = self

        class SymLinkCommand(FileSystemCommand):
            def __init__(self):
                super(SymLinkCommand, self).__init__(service, "symlink",
                                                     (link_path, target_path))

            def done(self, error, args):
                s = None
                if error:
                    s = Status(error)
                else:
                    assert len(args) == 1
                    s = self._toSFError(args[0])
                done.doneSymLink(self.token, s)
        return SymLinkCommand().token

    def write(self, handle, offset, data, data_pos, data_size, done):
        assert handle.getService() is self
        done = self._makeCallback(done)
        _id = handle.id
        binary = bytearray(data[data_pos:data_pos + data_size])
        service = self

        class WriteCommand(FileSystemCommand):
            def __init__(self):
                super(WriteCommand, self).__init__(service, "write",
                                                   (_id, offset, binary))

            def done(self, error, args):
                s = None
                if error:
                    s = Status(error)
                else:
                    assert len(args) == 1
                    s = self._toSFError(args[0])
                done.doneWrite(self.token, s)
        return WriteCommand().token

    def copy(self, src_path, dst_path, copy_permissions, copy_uidgid, done):
        done = self._makeCallback(done)
        service = self

        class CopyCommand(FileSystemCommand):
            def __init__(self):
                copyparams = (src_path, dst_path, copy_permissions,
                              copy_uidgid)
                super(CopyCommand, self).__init__(service, "copy", copyparams)

            def done(self, error, args):
                s = None
                if error:
                    s = Status(error)
                else:
                    assert len(args) == 1
                    s = self._toSFError(args[0])
                done.doneCopy(self.token, s)
        return CopyCommand().token

    def user(self, done):
        done = self._makeCallback(done)
        service = self

        class UserCommand(FileSystemCommand):
            def __init__(self):
                super(UserCommand, self).__init__(service, "user", None)

            def done(self, error, args):
                s = None
                r_uid = 0
                e_uid = 0
                r_gid = 0
                e_gid = 0
                home = None
                if error:
                    s = Status(error)
                else:
                    assert len(args) == 5
                    r_uid, e_uid, r_gid, e_gid, home = args
                done.doneUser(self.token, s, r_uid, e_uid, r_gid, e_gid, home)
        return UserCommand().token

    def _toFileHandle(self, o):
        if o is None:
            return None
        return filesystem.FileHandle(self, o)


def _toObject(attrs):
    if attrs is None:
        return None
    m = {}
    if attrs.attributes is not None:
        m.update(attrs.attributes)
    if (attrs.flags & filesystem.ATTR_SIZE) != 0:
        m["Size"] = attrs.size
    if (attrs.flags & filesystem.ATTR_UIDGID) != 0:
        m["UID"] = attrs.uid
        m["GID"] = attrs.gid
    if (attrs.flags & filesystem.ATTR_PERMISSIONS) != 0:
        m["Permissions"] = attrs.permissions
    if (attrs.flags & filesystem.ATTR_ACMODTIME) != 0:
        m["ATime"] = attrs.atime
        m["MTime"] = attrs.mtime
    return m


def _toFileAttrs(m):
    if m is None:
        return None
    flags = 0
    size = 0
    uid = 0
    gid = 0
    permissions = 0
    atime = 0
    mtime = 0
    n = m.pop("Size", None)
    if n is not None:
        size = n
        flags |= filesystem.ATTR_SIZE
    n1 = m.pop("UID", None)
    n2 = m.pop("GID", None)
    if n1 is not None and n2 is not None:
        uid = n1
        gid = n2
        flags |= filesystem.ATTR_UIDGID
    n = m.pop("Permissions", None)
    if n is not None:
        permissions = n
        flags |= filesystem.ATTR_PERMISSIONS
    n1 = m.pop("ATime", None)
    n2 = m.pop("MTime", None)
    if n1 is not None and n2 is not None:
        atime = n1
        mtime = n2
        flags |= filesystem.ATTR_ACMODTIME
    return filesystem.FileAttrs(flags, size, uid, gid,
                                permissions, atime, mtime, m)


def _toDirEntryArray(o):
    if o is None:
        return None
    res = []
    for m in o:
        entry = filesystem.DirEntry(m.get("FileName"), m.get("LongName"),
                                    _toFileAttrs(m.get("Attrs")))
        res.append(entry)
    return res
