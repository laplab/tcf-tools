# *****************************************************************************
# * Copyright (c) 2014 Wind River Systems, Inc. and others.
# * All rights reserved. This program and the accompanying materials
# * are made available under the terms of the Eclipse Public License 2.0
# * which accompanies this distribution, and is available at
# * https://www.eclipse.org/legal/epl-2.0/
# *
# * Contributors:
# *     Wind River Systems - initial API and implementation
# *****************************************************************************

from .. import dprintf
from ...channel.Command import Command


class DPrintfProxy(dprintf.DPrintfService):
    def __init__(self, channel):
        self.channel = channel
        self.listeners = {}

    def getName(self):
        return (dprintf.NAME)

    def open(self, done, arg=None):
        done = self._makeCallback(done)
        service = self

        class OpenCommand(Command):
            def __init__(self):
                super(OpenCommand, self).__init__(service.channel, service,
                                                  "open", (arg,))

            def done(self, error, args):
                if not error:
                    assert len(args) == 2
                    error = self.toError(args[0])
                    vs = args[1]

                done.doneOpen(self.token, error, vs)

        return OpenCommand().token

    def close(self, done):
        done = self._makeCallback(done)
        service = self

        class CloseCommand(Command):
            def __init__(self):
                super(CloseCommand, self).__init__(service.channel, service,
                                                   "close", None)

            def done(self, error, args):
                if not error:
                    assert len(args) == 1
                    error = self.toError(args[0])

                done.doneClose(self.token, error)

        return CloseCommand().token
