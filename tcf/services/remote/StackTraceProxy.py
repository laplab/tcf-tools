# *****************************************************************************
# * Copyright (c) 2011, 2013, 2015-2016 Wind River Systems, Inc. and others.
# * All rights reserved. This program and the accompanying materials
# * are made available under the terms of the Eclipse Public License 2.0
# * which accompanies this distribution, and is available at
# * https://www.eclipse.org/legal/epl-2.0/
# *
# * Contributors:
# *     Wind River Systems - initial API and implementation
# *****************************************************************************

from .. import stacktrace
from ...channel.Command import Command


class StackTraceProxy(stacktrace.StackTraceService):
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
                contextIds = None
                if not error:
                    assert len(args) == 2
                    error = self.toError(args[0])
                    contextIds = args[1]
                done.doneGetChildren(self.token, error, contextIds)
        return GetChildrenCommand().token

    def getChildrenRange(self, parent_context_id, range_start, range_end,
                         done):
        done = self._makeCallback(done)
        service = self

        class GetChildrenRangeCommand(Command):
            def __init__(self):
                super(GetChildrenRangeCommand, self).__init__(
                    service.channel,
                    service,
                    "getChildrenRange",
                    (parent_context_id,
                     range_start,
                     range_end,))

            def done(self, error, args):
                contextIds = None
                if not error:
                    assert len(args) == 2
                    error = self.toError(args[0])
                    contextIds = args[1]
                done.doneGetChildren(self.token, error, contextIds)
        return GetChildrenRangeCommand().token

    def getContext(self, ids, done):
        done = self._makeCallback(done)
        service = self

        class GetContextCommand(Command):
            def __init__(self):
                super(GetContextCommand, self).__init__(service.channel,
                                                        service, "getContext",
                                                        (ids,))

            def done(self, error, args):
                ctxs = None
                if not error:
                    assert len(args) == 2
                    error = self.toError(args[1])
                    ctxs = service.toContextArray(args[0])
                done.doneGetContext(self.token, error, ctxs)
        return GetContextCommand().token

    def toContextArray(self, ctxProps):
        if ctxProps is None:
            return None
        ctxs = []
        for props in ctxProps:
            ctxs.append(stacktrace.StackTraceContext(props))
        return ctxs
