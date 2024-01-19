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

from .. import pathmap
from ... import channel
from ...channel.Command import Command


class ChannelEventListener(channel.EventListener):
    def __init__(self, service, listener):
        self.service = service
        self.listener = listener

    def event(self, name, data):
        try:
            if name == "changed":
                self.listener.changed()
        except Exception as x:
            import sys
            x.tb = sys.exc_info()[2]
            self.service.channel.terminate(x)


class PathMapProxy(pathmap.PathMapService):
    def __init__(self, channel):
        self.channel = channel
        self.listeners = {}

    def get(self, done):
        done = self._makeCallback(done)
        service = self

        class GetCommand(Command):
            def __init__(self):
                super(GetCommand, self).__init__(service.channel, service,
                                                 "get", None)

            def done(self, error, args):
                pmMap = None
                if not error:
                    assert len(args) == 2
                    error = self.toError(args[0])
                    if args[1]:
                        pmMap = _toPathMap(args[1])
                done.doneGet(self.token, error, pmMap)
        return GetCommand().token

    def set(self, pmMap, done):
        if isinstance(pmMap, pathmap.PathMapRule) or isinstance(pmMap, dict):
            pmMap = (pmMap,)
        done = self._makeCallback(done)
        service = self

        class SetCommand(Command):
            def __init__(self):
                super(SetCommand, self).__init__(service.channel, service,
                                                 "set", (pmMap,))

            def done(self, error, args):
                if not error:
                    assert len(args) == 1
                    error = self.toError(args[0])
                done.doneSet(self.token, error)
        return SetCommand().token

    def addListener(self, listener):
        """Add a pathmap listener to the connected channel."""
        l = ChannelEventListener(self, listener)
        self.channel.addEventListener(self, l)
        self.listeners[listener] = l

    def removeListener(self, listener):
        """Remove given pathmap listener from the connected channel."""
        l = self.listeners.get(listener)
        if l:
            del self.listeners[listener]
            self.channel.removeEventListener(self, l)


def _toPathMap(o):
    if o is None:
        return None
    return list(map(_toPathMapRule, o))


def _toPathMapRule(o):
    if o is None:
        return None
    return pathmap.PathMapRule(o)
