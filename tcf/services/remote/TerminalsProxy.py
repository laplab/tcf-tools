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

from .. import terminals
from ... import channel
from ...channel.Command import Command


class TerminalContext(terminals.TerminalContext):
    def __init__(self, service, props):
        super(TerminalContext, self).__init__(props)
        self.service = service

    def exit(self, done):
        service = self.service
        done = service._makeCallback(done)
        context_id = self.getID()

        class ExitCommand(Command):
            def __init__(self):
                super(ExitCommand, self).__init__(
                    service.channel, service, "exit", (context_id,))

            def done(self, error, args):
                if not error:
                    assert len(args) == 1
                    error = self.toError(args[0])
                done.doneCommand(self.token, error)
        return ExitCommand().token


class TerminalsProxy(terminals.TerminalsService):
    def __init__(self, channel):
        self.channel = channel
        self.listeners = {}

    def getContext(self, contextID, done):
        done = self._makeCallback(done)
        service = self

        class GetContextCommand(Command):
            def __init__(self):
                super(GetContextCommand, self).__init__(
                    service.channel, service, "getContext", (contextID,))

            def done(self, error, args):
                ctx = None
                if not error:
                    assert len(args) == 2
                    error = self.toError(args[0])
                    if args[1]:
                        ctx = TerminalContext(service, args[1])
                done.doneGetContext(self.token, error, ctx)
        return GetContextCommand().token

    def launch(self, terminal_type, encoding, environment, done):
        done = self._makeCallback(done)
        service = self

        class LaunchCommand(Command):
            def __init__(self):
                super(LaunchCommand, self).__init__(service.channel, service,
                                                    "launch",
                                                    (terminal_type, encoding,
                                                     environment))

            def done(self, error, args):
                ctx = None
                if not error:
                    assert len(args) == 2
                    error = self.toError(args[0])
                    if args[1]:
                        ctx = TerminalContext(service, args[1])
                done.doneLaunch(self.token, error, ctx)
        return LaunchCommand().token

    def setWinSize(self, context_id, newWidth, newHeight, done):
        done = self._makeCallback(done)
        service = self

        class SetWinSizeCommand(Command):
            def __init__(self):
                super(SetWinSizeCommand, self).__init__(service.channel,
                                                        service, "setWinSize",
                                                        (context_id, newWidth,
                                                         newHeight))

            def done(self, error, args):
                if not error:
                    assert len(args) == 1
                    error = self.toError(args[0])
                done.doneCommand(self.token, error)
        return SetWinSizeCommand().token

    def exit(self, context_id, done):
        done = self._makeCallback(done)
        service = self

        class ExitCommand(Command):
            def __init__(self):
                super(ExitCommand, self).__init__(service.channel, service,
                                                  "exit", (context_id,))

            def done(self, error, args):
                if not error:
                    assert len(args) == 1
                    error = self.toError(args[0])
                done.doneCommand(self.token, error)
        return ExitCommand().token

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
            if name == "exited":
                assert len(args) == 2
                self.listener.exited(args[0], args[1])
            elif name == "winSizeChanged":
                assert len(args) == 3
                self.listener.winSizeChanged(args[0], args[1], args[2])
            else:
                raise IOError("Terminals service: unknown event: " + name)
        except Exception as x:
            import sys
            x.tb = sys.exc_info()[2]
            self.service.channel.terminate(x)
