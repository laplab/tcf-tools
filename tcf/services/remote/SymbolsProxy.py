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

from .. import symbols
from ... import channel
from ...channel.Command import Command


class SymbolWithValue(symbols.Symbol):
    def __init__(self, props):
        super(SymbolWithValue, self).__init__(props)
        self.value = channel.toByteArray(props.get(symbols.PROP_VALUE))

    def __str__(self):
        res = symbols.Symbol.__str__(self).rstrip(']')
        res += ', value=' + str(self.value) + ']'
        return res

    def getValue(self):
        return self.value


class SymbolsProxy(symbols.SymbolsService):

    def __init__(self, channel):
        self.channel = channel

    def getContext(self, contextID, done):
        done = self._makeCallback(done)
        service = self

        class GetContextCommand(Command):
            def __init__(self):
                super(GetContextCommand, self).__init__(service.channel,
                                                        service, "getContext",
                                                        (contextID,))

            def done(self, error, args):
                ctx = None
                if not error:
                    assert len(args) == 2
                    error = self.toError(args[0])
                    if args[1]:
                        ctx = SymbolWithValue(args[1])
                done.doneGetContext(self.token, error, ctx)
        return GetContextCommand().token

    def getChildren(self, parent_context_id, done):
        done = self._makeCallback(done)
        service = self

        class GetChildrenCommand(Command):

            def __init__(self):
                super(GetChildrenCommand, self).__init__(service.channel,
                                                         service,
                                                         "getChildren",
                                                         (parent_context_id,))

            def done(self, error, args):
                contexts = None
                if not error:
                    assert len(args) == 2
                    error = self.toError(args[0])
                    contexts = args[1]
                done.doneGetChildren(self.token, error, contexts)
        return GetChildrenCommand().token

    def getLocationInfo(self, symbolID, done):
        """Retrieve symbol location information.
        @param symbol_id - symbol ID.
        @param done - call back interface called when operation is completed.
        @return - pending command handle.
        """
        done = self._makeCallback(done)
        service = self

        class GetLocationInfoCommand(Command):
            def __init__(self):
                super(GetLocationInfoCommand, self).__init__(service.channel,
                                                             service,
                                                             "getLocationInfo",
                                                             (symbolID,))

            def done(self, error, args):
                props = None
                if not error:
                    assert len(args) == 2
                    error = self.toError(args[0])
                    props = args[1]
                done.doneGetLocationInfo(self.token, error, props)
        return GetLocationInfoCommand().token

    def getSymFileInfo(self, contextID, address, done):
        """Get symbol file info for a module that contains given address in a
        memory space.
        @param contextID - a memory space (process) ID.
        @param address - an address in the memory space.
        @param done - call back interface called when operation is completed.
        @return - pending command handle.
        """
        done = self._makeCallback(done)
        service = self

        class GetSymFileInfoCommand(Command):
            def __init__(self):
                super(GetSymFileInfoCommand, self).__init__(service.channel,
                                                            service,
                                                            "getSymFileInfo",
                                                            (contextID,
                                                             address,))

            def done(self, error, args):
                props = None
                if not error:
                    assert len(args) == 2
                    error = self.toError(args[0])
                    props = args[1]
                done.doneGetSymFileInfo(self.token, error, props)
        return GetSymFileInfoCommand().token

    def find(self, context_id, ip, name, done):
        done = self._makeCallback(done)
        service = self

        class FindCommand(Command):

            def __init__(self):
                super(FindCommand, self).__init__(service.channel, service,
                                                  "find", (context_id, ip,
                                                           name))

            def done(self, error, args):
                symbolID = None
                if not error:
                    assert len(args) == 2
                    error = self.toError(args[0])
                    symbolID = args[1]
                done.doneFind(self.token, error, symbolID)
        return FindCommand().token

    def findByName(self, context_id, ip, name, done):
        done = self._makeCallback(done)
        service = self

        class FindByNameCommand(Command):

            def __init__(self):
                super(FindByNameCommand, self).__init__(service.channel,
                                                        service, "findByName",
                                                        (context_id, ip, name))

            def done(self, error, args):
                ids = []
                if not error:
                    assert len(args) >= 2
                    error = self.toError(args[0])
                    if not error:
                        ids = args[1]
                done.doneFind(self.token, error, ids)
        return FindByNameCommand().token

    def findInScope(self, context_id, ip, scope_id, name, done):
        done = self._makeCallback(done)
        service = self

        class FindInScopeCommand(Command):

            def __init__(self):
                super(FindInScopeCommand, self).__init__(service.channel,
                                                         service,
                                                         "findInScope",
                                                         (context_id, ip,
                                                          scope_id, name))

            def done(self, error, args):
                ids = []
                if not error:
                    assert len(args) >= 2
                    error = self.toError(args[0])
                    if not error:
                        ids = args[1:]
                done.doneFind(self.token, error, ids)
        return FindInScopeCommand().token

    def findByAddr(self, context_id, addr, done):
        done = self._makeCallback(done)
        service = self

        class FindByAddrCommand(Command):

            def __init__(self):
                super(FindByAddrCommand, self).__init__(service.channel,
                                                        service, "findByAddr",
                                                        (context_id, addr))

            def done(self, error, args):
                symbolID = None
                if not error:
                    assert len(args) == 2
                    error = self.toError(args[0])
                    symbolID = args[1]
                done.doneFind(self.token, error, symbolID)
        return FindByAddrCommand().token

    def list(self, context_id, done):  # @ReservedAssignment
        done = self._makeCallback(done)
        service = self

        class ListCommand(Command):

            def __init__(self):
                super(ListCommand, self).__init__(service.channel, service,
                                                  "list", (context_id,))

            def done(self, error, args):
                lst = None
                if not error:
                    assert len(args) == 2
                    error = self.toError(args[0])
                    lst = args[1]
                done.doneList(self.token, error, lst)
        return ListCommand().token

    def getArrayType(self, type_id, length, done):
        done = self._makeCallback(done)
        service = self

        class GetArrayTypeCommand(Command):

            def __init__(self):
                super(GetArrayTypeCommand, self).__init__(service.channel,
                                                          service,
                                                          "getArrayType",
                                                          (type_id, length))

            def done(self, error, args):
                symbolID = None
                if not error:
                    assert len(args) == 2
                    error = self.toError(args[0])
                    symbolID = args[1]
                done.doneGetArrayType(self.token, error, symbolID)
        return GetArrayTypeCommand().token

    def findFrameInfo(self, context_id, address, done):
        done = self._makeCallback(done)
        service = self

        class FindFrameInfoCommand(Command):

            def __init__(self):
                super(FindFrameInfoCommand, self).__init__(service.channel,
                                                           service,
                                                           "findFrameInfo",
                                                           (context_id,
                                                            address))

            def done(self, error, args):
                address = None
                size = None
                fp_cmds = None
                reg_cmds = None
                if not error:
                    assert len(args) == 5
                    error = self.toError(args[0])
                    address, size, fp_cmds, reg_cmds = args[1:5]
                done.doneFindFrameInfo(self.token, error, address, size,
                                       fp_cmds, reg_cmds)
        return FindFrameInfoCommand().token
