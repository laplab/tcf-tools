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

from .. import memorymap
from ... import channel
from ...channel.Command import Command


class MemoryMapProxy(memorymap.MemoryMapService):
    def __init__(self, channel):
        self.channel = channel
        self.listeners = {}

    def get(self, contextID, done):
        done = self._makeCallback(done)
        service = self

        class GetCommand(Command):
            def __init__(self):
                super(GetCommand, self).__init__(service.channel, service,
                                                 "get", (contextID,))

            def done(self, error, args):
                memMap = None
                if not error:
                    assert len(args) == 2
                    error = self.toError(args[0])
                    if args[1]:
                        memMap = _toMemoryMap(args[1])
                done.doneGet(self.token, error, memMap)
        return GetCommand().token

    def set(self, contextID, memMap, done):
        if isinstance(memMap, memorymap.MemoryRegion) or \
           isinstance(memMap, dict):
            memMap = (memMap,)
        done = self._makeCallback(done)
        service = self

        class SetCommand(Command):
            def __init__(self):
                super(SetCommand, self).__init__(service.channel, service,
                                                 "set", (contextID, memMap))

            def done(self, error, args):
                if not error:
                    assert len(args) == 1
                    error = self.toError(args[0])
                done.doneSet(self.token, error)
        return SetCommand().token

    def addListener(self, listener):
        l = ChannelEventListener(self, listener)
        self.channel.addEventListener(self, l)
        self.listeners[listener] = l

    def removeListener(self, listener):
        l = self.listeners.pop(listener, None)
        if l:
            self.channel.removeEventListener(self, l)


class ChannelEventListener(channel.EventListener):
    def __init__(self, service, listener):
        self.service = service
        self.listener = listener

    def event(self, name, data):
        try:
            args = channel.fromJSONSequence(data)
            if name == "changed":
                assert len(args) == 1
                self.listener.changed(args[0])
            else:
                raise IOError("MemoryMap service: unknown event: " + name)
        except Exception as x:
            import sys
            x.tb = sys.exc_info()[2]
            self.service.channel.terminate(x)


def _toMemoryMap(o):
    if o is None:
        return None
    return list(map(_toMemoryRegion, o))


def _toMemoryRegion(o):
    if o is None:
        return None
    return memorymap.MemoryRegion(o)
