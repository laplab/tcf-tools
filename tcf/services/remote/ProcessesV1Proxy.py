# *****************************************************************************
# * Copyright (c) 2011-2014, 2016 Wind River Systems, Inc. and others.
# * All rights reserved. This program and the accompanying materials
# * are made available under the terms of the Eclipse Public License 2.0
# * which accompanies this distribution, and is available at
# * https://www.eclipse.org/legal/epl-2.0/
# *
# * Contributors:
# *     Wind River Systems - initial API and implementation
# *****************************************************************************

from . import ProcessesProxy
from .. import processes_v1
from ...channel.Command import Command


class ProcessesV1Proxy(ProcessesProxy.ProcessesProxy,
                       processes_v1.ProcessesV1Service):

    def start(self, directory, filePath, command_line, environment, params,
              done):
        done = self._makeCallback(done)
        service = self
        env = ProcessesProxy._toEnvStringArray(environment)

        class StartCommand(Command):
            def __init__(self):
                super(StartCommand, self).__init__(service.channel, service,
                                                   "start",
                                                   (directory, filePath,
                                                    command_line, env, params))

            def done(self, error, args):
                ctx = None
                if not error:
                    assert len(args) == 2
                    error = self.toError(args[0])
                    if args[1]:
                        ctx = ProcessesProxy.ProcessContext(service, args[1])
                done.doneStart(self.token, error, ctx)
        return StartCommand().token

    def getCapabilities(self, contextId, done):
        done = self._makeCallback(done)
        service = self

        class GetCapabilitiesCommand(Command):

            def __init__(self):
                super(GetCapabilitiesCommand, self).__init__(service.channel,
                                                             service,
                                                             "getCapabilities",
                                                             (contextId,))

            def done(self, error, args):
                capabilityData = None
                if not error:
                    # Defect WB4-1784, getting capabilities with a null
                    # context ID does not return the global system capabilities
                    # as it should
                    if len(args) == 1:
                        error = self.toError(args[0])
                        capabilityData = {}
                    else:
                        assert len(args) == 2
                        error = self.toError(args[0])
                        capabilityData = args[1]

                done.doneGetCapabilities(self.token, error, capabilityData)

        return GetCapabilitiesCommand().token
