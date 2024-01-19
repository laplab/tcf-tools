# *****************************************************************************
# * Copyright (c) 2012-2014, 2016 Wind River Systems, Inc. and others.
# * All rights reserved. This program and the accompanying materials
# * are made available under the terms of the Eclipse Public License 2.0
# * which accompanies this distribution, and is available at
# * https://www.eclipse.org/legal/epl-2.0/
# *
# * Contributors:
# *     Wind River Systems - initial API and implementation
# *****************************************************************************

from .. import contextquery
from ...channel.Command import Command


class ContextQueryProxy(contextquery.ContextQueryService):
    def __init__(self, channel):
        self.channel = channel
        self.listeners = {}

    def query(self, querystr, done):
        done = self._makeCallback(done)
        service = self

        class QueryCommand(Command):

            def __init__(self):
                super(QueryCommand, self).__init__(service.channel, service,
                                                   "query", (querystr,))

            def done(self, error, args):
                res = None
                if not error:
                    assert len(args) == 2
                    error = self.toError(args[0])
                    res = args[1]
                done.doneQuery(self.token, error, res)
        return QueryCommand().token

    def getAttrNames(self, done):
        done = self._makeCallback(done)
        service = self

        class GetAttrNamesCommand(Command):

            def __init__(self):
                super(GetAttrNamesCommand, self).__init__(service.channel,
                                                          service,
                                                          "getAttrNames", None)

            def done(self, error, args):
                res = None
                if not error:
                    assert len(args) == 2
                    error = self.toError(args[0])
                    res = args[1]
                done.doneGetAttrNames(self.token, error, res)
        return GetAttrNamesCommand().token
