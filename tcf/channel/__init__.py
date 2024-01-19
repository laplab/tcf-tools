# *****************************************************************************
# * Copyright (c) 2011, 2013, 2016 Wind River Systems, Inc. and others.
# * All rights reserved. This program and the accompanying materials
# * are made available under the terms of the Eclipse Public License 2.0
# * which accompanies this distribution, and is available at
# * https://www.eclipse.org/legal/epl-2.0/
# *
# * Contributors:
# *     Wind River Systems - initial API and implementation
# *****************************************************************************

import binascii
import json
import types

# channel states
STATE_OPENING = 0
STATE_OPEN = 1
STATE_CLOSED = 2


class TraceListener(object):
    def onMessageReceived(self, t, token, service, name, data):
        pass

    def onMessageSent(self, t, token, service, name, data):
        pass

    def onChannelClosed(self, error):
        pass


class Proxy(object):
    def onCommand(self, token, service, name, data):
        pass

    def onEvent(self, service, name, data):
        pass

    def onChannelClosed(self, error):
        pass

_token_cnt = 0


class Token(object):
    def __init__(self, tokenID=None, listener=None):
        if tokenID is None:
            global _token_cnt
            tokenID = str(_token_cnt)
            _token_cnt += 1
        else:
            if isinstance(tokenID, bytearray):
                tokenID = tokenID.decode('utf-8')
            else:
                tokenID = str(tokenID)
        self.id = tokenID
        self.listener = listener

    def getID(self):
        return self.id

    def getListener(self):
        return self.listener

    def cancel(self):
        return False


class ChannelListener(object):
    """
    Channel listener interface.
    """

    def onChannelOpened(self):
        """
        Called when a channel is opened or redirected.
        """
        pass

    def onChannelClosed(self, error):
        """
        Called when channel closed. If it is closed because of an error,
        'error' parameter will describe the error. 'error' is None if channel
        is closed normally by calling Channel.close().
        @param error - channel exception or None
        """
        pass

    def congestionLevel(self, level):
        """
        Notifies listeners about channel out-bound traffic congestion level
        changes.
        When level > 0 client should delay sending more messages.
        @param level - current congestion level
        """
        pass


class EventListener(object):
    """
    A generic interface for service event listener.
    Services usually define a service specific event listener interface,
    which is implemented using this generic listener.
    Clients should user service specific listener interface,
    unless no such interface is defined.
    """
    svc_name = "<unknown>"

    def event(self, name, data):
        """
        Called when service event message is received
        @param name - event name
        @param data - event arguments encoded as bytearray
        """
        pass


class CommandServer(object):
    """
    Command server interface.
    This interface is to be implemented by service providers.
    """
    def command(self, token, name, data):
        """
        Called every time a command is received from remote peer.
        @param token - command handle
        @param name - command name
        @param data - command arguments encoded into array of bytes
        """
        pass


class CommandListener(object):
    """
    Command listener interface. Clients implement this interface to
    receive command results.
    """
    def progress(self, token, data):
        """
        Called when progress message (intermediate result) is received
        from remote peer.
        @param token - command handle
        @param data - progress message arguments encoded into array of bytes
        """
        pass

    def result(self, token, data):
        """
        Called when command result received from remote peer.
        @param token - command handle
        @param data - command result message arguments encoded into array of
                      bytes
        """
        pass

    def terminated(self, token, error):
        """
        Called when command is terminated because communication channel was
        closed or command is not recognized by remote peer.
        @param token - command handle
        @param error - exception that forced the channel to close
        """
        pass


def toJSONSequence(args):
    if args is None:
        return None
    sequence = []
    for arg in args:
        sequence.append(json.dumps(arg, separators=(',', ':'),
                                   cls=TCFJSONEncoder))
    if sequence:
        res = '\0'.join(sequence) + '\0'
    else:
        res = ''
    # print('DEBUG: translated ', repr(args), ' into ', repr(res))
    return res


def fromJSONSequence(byteArray):
    if byteArray[-1] == 0:
        del byteArray[-1]
    jsonStr = byteArray.decode("UTF-8")
    parts = jsonStr.split('\0')
    objects = []
    for part in parts:
        if part:
            objects.append(json.loads(part))
        else:
            objects.append(None)
    return objects


def dumpJSONObject(obj):
    return json.dumps(obj, separators=(',', ':'), cls=TCFJSONEncoder)


def toByteArray(data):
    if data is None:
        return None
    t = type(data)
    if t is bytearray:
        return data
    else:
        return bytearray(binascii.a2b_base64(data))
    raise TypeError(str(t))


class TCFJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, bytearray):
            return binascii.b2a_base64(o)[:-1]
        elif isinstance(o, bytes):
            return o.decode('utf-8')
        elif hasattr(o, '__json__'):
            return o.__json__()
        elif hasattr(o, '__iter__'):
            return tuple(o)
        else:
            json.JSONEncoder.default(self, o)
