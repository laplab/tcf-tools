# *****************************************************************************
# * Copyright (c) 2019.
# * All rights reserved. This program and the accompanying materials
# * are made available under the terms of the Eclipse Public License 2.0
# * which accompanies this distribution, and is available at
# * https://www.eclipse.org/legal/epl-2.0/
# *****************************************************************************

from .. import contextreset
from ...channel.Command import Command


class ContextResetProxy(contextreset.ContextResetService):

    def __init__(self, channel):
        self.channel = channel

    def getCapabilities(self, context_id, done):
        done = self._makeCallback(done)
        service = self

        class GetCapabilitiesCommand(Command):

            def __init__(self):
                super(GetCapabilitiesCommand, self).__init__(service.channel,
                                                             service,
                                                             "getCapabilities",
                                                             (context_id,))

            def done(self, error, args):
                arr = None
                if not error:
                    assert len(args) == 2
                    error = self.toError(args[0])
                    arr = args[1]
                done.doneGetCapabilities(self.token, arr, error)
        return GetCapabilitiesCommand().token

    def reset(self, context_id, type, params, done):
        done = self._makeCallback(done)
        service = self

        class ResetCommand(Command):

            def __init__(self):
                super(ResetCommand, self).__init__(service.channel,
                                                   service,
                                                   reset",
                                                   (context_id, type,
                                                    params))

            def done(self, error, args):
                arr = None
                if not error:
                    assert len(args) == 2
                    error = self.toError(args[0])
                done.doneReset(self.token, error)
        return DisassembleCommand().token
