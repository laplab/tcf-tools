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

from .. import breakpoints
from ... import channel
from ...channel.Command import Command


class BPCommand(Command):
    def __init__(self, service, cmd, cb, *args):
        super(BPCommand, self).__init__(service.channel, service, cmd, args)
        self.__cb = cb

    def done(self, error, args):
        if not error:
            assert len(args) == 1
            error = self.toError(args[0])
        self.__cb.doneCommand(self.token, error)


class ChannelEventListener(channel.EventListener):
    def __init__(self, service, listener):
        self.service = service
        self.listener = listener

    def event(self, name, data):
        try:
            args = channel.fromJSONSequence(data)
            if name == "status":
                assert len(args) == 2
                self.listener.breakpointStatusChanged(args[0], args[1])
            elif name == "contextAdded":
                assert len(args) == 1
                self.listener.contextAdded(args[0])
            elif name == "contextChanged":
                assert len(args) == 1
                self.listener.contextChanged(args[0])
            elif name == "contextRemoved":
                assert len(args) == 1
                self.listener.contextRemoved(args[0])
            else:
                raise IOError("Breakpoints service: unknown event: " + name)
        except Exception as x:
            import sys
            x.tb = sys.exc_info()[2]
            self.service.channel.terminate(x)


class BreakpointsProxy(breakpoints.BreakpointsService):
    def __init__(self, channel):
        self.channel = channel
        self.listeners = {}

    def set(self, properties, done):
        done = self._makeCallback(done)
        return BPCommand(self, "set", done, properties).token

    def add(self, properties, done):
        done = self._makeCallback(done)
        return BPCommand(self, "add", done, properties).token

    def change(self, properties, done):
        done = self._makeCallback(done)
        return BPCommand(self, "change", done, properties).token

    def disable(self, ids, done):
        done = self._makeCallback(done)
        return BPCommand(self, "disable", done, ids).token

    def enable(self, ids, done):
        done = self._makeCallback(done)
        return BPCommand(self, "enable", done, ids).token

    def remove(self, ids, done):
        done = self._makeCallback(done)
        return BPCommand(self, "remove", done, ids).token

    def getIDs(self, done):
        done = self._makeCallback(done)
        service = self

        class GetIDsCommand(Command):
            def __init__(self):
                super(GetIDsCommand, self).__init__(service.channel, service,
                                                    "getIDs", None)

            def done(self, error, args):
                ids = None
                if not error:
                    assert len(args) == 2
                    error = self.toError(args[0])
                    ids = args[1]
                done.doneGetIDs(self.token, error, ids)
        return GetIDsCommand().token

    def getProperties(self, contextID, done):
        done = self._makeCallback(done)
        service = self

        class GetPropertiesCommand(Command):
            def __init__(self):
                super(GetPropertiesCommand, self).__init__(service.channel,
                                                           service,
                                                           "getProperties",
                                                           (contextID,))

            def done(self, error, args):
                props = None
                if not error:
                    assert len(args) == 2
                    error = self.toError(args[0])
                    props = args[1]
                done.doneGetProperties(self.token, error, props)
        return GetPropertiesCommand().token

    def getStatus(self, contextID, done):
        done = self._makeCallback(done)
        service = self

        class GetStatusCommand(Command):
            def __init__(self):
                super(GetStatusCommand, self).__init__(service.channel,
                                                       service, "getStatus",
                                                       (contextID,))

            def done(self, error, args):
                states = None
                if not error:
                    assert len(args) == 2
                    error = self.toError(args[0])
                    states = args[1]
                done.doneGetStatus(self.token, error, states)
        return GetStatusCommand().token

    def getCapabilities(self, contextID, done):
        done = self._makeCallback(done)
        service = self

        class GetCapabilitiesCommand(Command):
            def __init__(self):
                super(GetCapabilitiesCommand, self).__init__(service.channel,
                                                             service,
                                                             "getCapabilities",
                                                             (contextID,))

            def done(self, error, args):
                capabilities = None
                if not error:
                    assert len(args) == 2
                    error = self.toError(args[0])
                    capabilities = args[1]
                done.doneGetCapabilities(self.token, error, capabilities)
        return GetCapabilitiesCommand().token

    def addListener(self, listener):
        l = ChannelEventListener(self, listener)
        self.channel.addEventListener(self, l)
        self.listeners[listener] = l

    def removeListener(self, listener):
        l = self.listeners.get(listener)
        if l:
            del self.listeners[listener]
            self.channel.removeEventListener(self, l)
