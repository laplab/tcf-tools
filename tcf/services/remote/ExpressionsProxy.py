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

from .. import expressions
from ... import channel
from ...channel.Command import Command


class ExpressionsProxy(expressions.ExpressionsService):
    def __init__(self, channel):
        self.channel = channel
        self.listeners = {}

    def assign(self, contextID, value, done):
        done = self._makeCallback(done)
        service = self
        value = bytearray(value)

        class AssignCommand(Command):
            def __init__(self):
                super(AssignCommand, self).__init__(service.channel, service,
                                                    "assign",
                                                    (contextID, value))

            def done(self, error, args):
                if not error:
                    assert len(args) == 1
                    error = self.toError(args[0])
                done.doneAssign(self.token, error)
        return AssignCommand().token

    def create(self, parent_id, language, expression, done):
        done = self._makeCallback(done)
        service = self

        class CreateCommand(Command):
            def __init__(self):
                super(CreateCommand, self).__init__(service.channel, service,
                                                    "create",
                                                    (parent_id, language,
                                                     expression))

            def done(self, error, args):
                ctx = None
                if not error:
                    assert len(args) == 2
                    error = self.toError(args[0])
                    if args[1]:
                        ctx = expressions.Expression(args[1])
                done.doneCreate(self.token, error, ctx)
        return CreateCommand().token

    def dispose(self, contextID, done):
        done = self._makeCallback(done)
        service = self

        class DisposeCommand(Command):
            def __init__(self):
                super(DisposeCommand, self).__init__(service.channel, service,
                                                     "dispose", (contextID,))

            def done(self, error, args):
                if not error:
                    assert len(args) == 1
                    error = self.toError(args[0])
                done.doneDispose(self.token, error)
        return DisposeCommand().token

    def evaluate(self, contextID, done):
        done = self._makeCallback(done)
        service = self

        class EvalCommand(Command):
            def __init__(self):
                super(EvalCommand, self).__init__(service.channel, service,
                                                  "evaluate", (contextID,))

            def done(self, error, args):
                value = None
                props = {}
                if not error:
                    assert len(args) == 3
                    value = channel.toByteArray(args[0])
                    error = self.toError(args[1])
                    props = args[2]
                done.doneEvaluate(self.token, error,
                                  expressions.Value(value, props))
        return EvalCommand().token

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
                        ctx = expressions.Expression(args[1])
                done.doneGetContext(self.token, error, ctx)
        return GetContextCommand().token

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
            if name == "valueChanged":
                assert len(args) == 1
                self.listener.valueChanged(args[0])
            else:
                raise IOError("Expressions service: unknown event: " + name)
        except Exception as x:
            import sys
            x.tb = sys.exc_info()[2]
            self.service.channel.terminate(x)
