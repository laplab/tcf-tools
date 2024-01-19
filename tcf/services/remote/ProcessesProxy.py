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

from .. import processes
from ... import channel
from ...channel.Command import Command


class ProcessContext(processes.ProcessContext):
    def __init__(self, service, props):
        super(ProcessContext, self).__init__(props)
        self.service = service

    def attach(self, done):
        return self._command("attach", done)

    def detach(self, done):
        return self._command("detach", done)

    def terminate(self, done):
        return self._command("terminate", done)

    def _command(self, command, done):
        service = self.service
        done = service._makeCallback(done)
        contextID = self.getID()

        class _Command(Command):
            def __init__(self):
                super(_Command, self).__init__(service.channel, service,
                                               command, (contextID,))

            def done(self, error, args):
                if not error:
                    assert len(args) == 1
                    error = self.toError(args[0])
                done.doneCommand(self.token, error)
        return _Command().token


class ProcessesProxy(processes.ProcessesService):
    def __init__(self, channel):
        self.channel = channel
        self.listeners = {}

    def getChildren(self, parent_context_id, attached_only, done):
        done = self._makeCallback(done)
        service = self

        class GetChildrenCommand(Command):
            def __init__(self):
                super(GetChildrenCommand, self).__init__(service.channel,
                                                         service,
                                                         "getChildren",
                                                         (parent_context_id,
                                                          attached_only))

            def done(self, error, args):
                contexts = None
                if not error:
                    assert len(args) == 2
                    error = self.toError(args[0])
                    contexts = args[1]
                done.doneGetChildren(self.token, error, contexts)
        return GetChildrenCommand().token

    def getContext(self, context_id, done):
        done = self._makeCallback(done)
        service = self

        class GetContextCommand(Command):
            def __init__(self):
                super(GetContextCommand, self).__init__(service.channel,
                                                        service, "getContext",
                                                        (context_id,))

            def done(self, error, args):
                ctx = None
                if not error:
                    assert len(args) == 2
                    error = self.toError(args[0])
                    if args[1]:
                        ctx = ProcessContext(service, args[1])
                done.doneGetContext(self.token, error, ctx)
        return GetContextCommand().token

    def getEnvironment(self, done):
        done = self._makeCallback(done)
        service = self

        class GetEnvCommand(Command):
            def __init__(self):
                super(GetEnvCommand, self).__init__(service.channel, service,
                                                    "getEnvironment", None)

            def done(self, error, args):
                env = None
                if not error:
                    assert len(args) == 2
                    error = self.toError(args[0])
                    env = _toEnvMap(args[1])
                done.doneGetEnvironment(self.token, error, env)
        return GetEnvCommand().token

    def start(self, directory, filePath, command_line, environment, attach,
              done):
        done = self._makeCallback(done)
        service = self
        env = _toEnvStringArray(environment)

        class StartCommand(Command):
            def __init__(self):
                super(StartCommand, self).__init__(service.channel, service,
                                                   "start",
                                                   (directory, filePath,
                                                    command_line, env, attach))

            def done(self, error, args):
                ctx = None
                if not error:
                    assert len(args) == 2
                    error = self.toError(args[0])
                    if args[1]:
                        ctx = ProcessContext(service, args[1])
                done.doneStart(self.token, error, ctx)
        return StartCommand().token

    def getSignalList(self, context_id, done):
        done = self._makeCallback(done)
        service = self

        class GetSignalsCommand(Command):
            def __init__(self):
                super(GetSignalsCommand, self).__init__(service.channel,
                                                        service,
                                                        "getSignalList",
                                                        (context_id,))

            def done(self, error, args):
                lst = None
                if not error:
                    assert len(args) == 2
                    error = self.toError(args[0])
                    lst = args[1]
                done.doneGetSignalList(self.token, error, lst)
        return GetSignalsCommand().token

    def getSignalMask(self, context_id, done):
        done = self._makeCallback(done)
        service = self

        class GetSignalMaskCommand(Command):
            def __init__(self):
                super(GetSignalMaskCommand, self).__init__(service.channel,
                                                           service,
                                                           "getSignalMask",
                                                           (context_id,))

            def done(self, error, args):
                dont_stop = 0
                dont_pass = 0
                pending = 0
                if not error:
                    assert len(args) == 4
                    error = self.toError(args[0])
                    dont_stop, dont_pass, pending = args[1:4]
                done.doneGetSignalMask(self.token, error, dont_stop, dont_pass,
                                       pending)
        return GetSignalMaskCommand().token

    def setSignalMask(self, context_id, dont_stop, dont_pass, done):
        done = self._makeCallback(done)
        service = self

        class SetSignalMaskCommand(Command):
            def __init__(self):
                super(SetSignalMaskCommand, self).__init__(service.channel,
                                                           service,
                                                           "setSignalMask",
                                                           (context_id,
                                                            dont_stop,
                                                            dont_pass))

            def done(self, error, args):
                if not error:
                    assert len(args) == 1
                    error = self.toError(args[0])
                done.doneCommand(self.token, error)
        return SetSignalMaskCommand().token

    def signal(self, context_id, signal, done):
        done = self._makeCallback(done)
        service = self

        class SignalCommand(Command):
            def __init__(self):
                super(SignalCommand, self).__init__(service.channel,
                                                    service, "signal",
                                                    (context_id, signal))

            def done(self, error, args):
                if not error:
                    assert len(args) == 1
                    error = self.toError(args[0])
                done.doneCommand(self.token, error)
        return SignalCommand().token

    def addListener(self, listener):
        l = ChannelEventListener(self, listener)
        self.channel.addEventListener(self, l)
        self.listeners[listener] = l

    def removeListener(self, listener):
        l = self.listeners.get(listener)
        if l:
            del self.listeners[listener]
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
            else:
                raise IOError("Processes service: unknown event: " + name)
        except Exception as x:
            import sys
            x.tb = sys.exc_info()[2]
            self.service.channel.terminate(x)


def _toEnvStringArray(envVars):
    arr = []
    if not envVars:
        return arr
    for name, value in list(envVars.items()):
        arr.append("%s=%s" % (name, value))
    return arr


def _toEnvMap(arr):
    envVars = {}
    if not arr:
        return envVars
    for env in arr:
        i = env.find('=')
        if i >= 0:
            envVars[env[:i]] = env[i + 1:]
        else:
            envVars[env] = ""
    return envVars
