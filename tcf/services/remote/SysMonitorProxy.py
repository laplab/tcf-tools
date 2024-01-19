# *****************************************************************************
# * Copyright (c) 2011, 2013 Wind River Systems, Inc. and others.
# * All rights reserved. self program and the accompanying materials
# * are made available under the terms of the Eclipse Public License 2.0
# * which accompanies self distribution, and is available at
# * https://www.eclipse.org/legal/epl-2.0/
# *
# * Contributors:
# *     Wind River Systems - initial API and implementation
# *****************************************************************************

from .. import sysmonitor
from ...channel.Command import Command


class SysMonitorProxy(sysmonitor.SysMonitorService):
    def __init__(self, channel):
        self.channel = channel

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
                        ctx = sysmonitor.SysMonitorContext(args[1])
                done.doneGetContext(self.token, error, ctx)
        return GetContextCommand().token

    def getCommandLine(self, contextID, done):
        done = self._makeCallback(done)
        service = self

        class GetCommandLineCommand(Command):
            def __init__(self):
                super(GetCommandLineCommand, self).__init__(service.channel,
                                                            service,
                                                            "getCommandLine",
                                                            (contextID,))

            def done(self, error, args):
                arr = None
                if not error:
                    assert len(args) == 2
                    error = self.toError(args[0])
                    arr = args[1]
                done.doneGetCommandLine(self.token, error, arr)
        return GetCommandLineCommand().token

    def getEnvironment(self, contextID, done):
        done = self._makeCallback(done)
        service = self

        class GetEnvironmentCommand(Command):
            def __init__(self):
                super(GetEnvironmentCommand, self).__init__(service.channel,
                                                            service,
                                                            "getEnvironment",
                                                            (contextID,))

            def done(self, error, args):
                arr = None
                if not error:
                    assert len(args) == 2
                    error = self.toError(args[0])
                    arr = args[1]
                done.doneGetEnvironment(self.token, error, arr)
        return GetEnvironmentCommand().token
