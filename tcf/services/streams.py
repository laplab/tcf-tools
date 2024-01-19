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

"""Streams service is a generic interface to support streaming of data between
host and remote agents.

.. |connect| replace:: :meth:`~StreamsService.connect`
.. |disconnect| replace:: :meth:`~StreamsService.disconnect`
.. |eos| replace:: :meth:`~StreamsService.eos`
.. |processes| replace:: :mod:`~tcf.services.processes`
.. |read| replace:: :meth:`~StreamsService.read`
.. |subscribe| replace:: :meth:`~StreamsService.subscribe`
.. |terminals| replace:: :mod:`~tcf.services.terminals`
.. |unsubscribe| replace:: :meth:`~StreamsService.unsubscribe`
.. |write| replace:: :meth:`~StreamsService.write`
.. |DoneConnect| replace:: :class:`DoneConnect`
.. |DoneDisconnect| replace:: :class:`DoneDisconnect`
.. |DoneEOS| replace:: :class:`DoneEOS`
.. |DoneRead| replace:: :class:`DoneRead`
.. |DoneSubscribe| replace:: :class:`DoneSubscribe`
.. |DoneUnsubscribe| replace:: :class:`DoneUnsubscribe`
.. |DoneWrite| replace:: :class:`DoneWrite`
.. |StreamsListener| replace:: :class:`StreamsListener`

The service supports:
 1. Asynchronous overlapped data streaming: multiple |read| or |write| command
    can be issued at same time, both peers can continue data processing
    concurrently with data transmission.
 2. Multicast: multiple clients can receive data from same stream.
 3. Subscription model: clients are required to expressed interest in
    particular streams by subscribing for the service.
 4. Flow control: peers can throttle data flow of individual streams by
    delaying |read| and |write| commands.

Service Methods
---------------
.. autodata:: NAME
.. autoclass:: StreamsService

connect
^^^^^^^
.. automethod:: StreamsService.connect

disconnect
^^^^^^^^^^
.. automethod:: StreamsService.disconnect

eos
^^^
.. automethod:: StreamsService.eos

getName
^^^^^^^
.. automethod:: StreamsService.getName

read
^^^^
.. automethod:: StreamsService.read

subscribe
^^^^^^^^^
.. automethod:: StreamsService.subscribe

unsubscribe
^^^^^^^^^^^
.. automethod:: StreamsService.unsubscribe

write
^^^^^
.. automethod:: StreamsService.write

Callback Classes
----------------
DoneConnect
^^^^^^^^^^^
.. autoclass:: DoneConnect
    :members:

DoneDisconnect
^^^^^^^^^^^^^^
.. autoclass:: DoneDisconnect
    :members:

DoneEOS
^^^^^^^
.. autoclass:: DoneEOS
    :members:

DoneRead
^^^^^^^^
.. autoclass:: DoneRead
    :members:

DoneSubscribe
^^^^^^^^^^^^^
.. autoclass:: DoneSubscribe
    :members:

DoneUnsubscribe
^^^^^^^^^^^^^^^
.. autoclass:: DoneUnsubscribe
    :members:

DoneWrite
^^^^^^^^^
.. autoclass:: DoneWrite
    :members:

Listener
--------
.. autoclass:: StreamsListener
    :members:
"""

from .. import services

NAME = "Streams"
"""Streams service name."""


class StreamsService(services.Service):
    """TCF Streams service interface."""

    def getName(self):
        """Get this service name.

        :returns: A |basestring| representing this service name, which is the
                  value of :const:`NAME`
        """
        return NAME

    def subscribe(self, stream_type, listener, done):
        """Clients must subscribe for one or more stream types to be able to
        send or receive stream data.

        Subscribers receive notifications when a stream of given type is
        created or disposed.

        Subscribers are required to respond with |read| or |disconnect|
        commands as necessary.

        .. note:: It is up to each service to implement its stream type if
                  required. For opensource services, |processes| uses
                  ``Processes`` for stream type, and |terminals| uses
                  ``Terminals``

        :param stream_type: The stream source type.
        :type stream_type: |basestring|
        :param listener: Client implementation of StreamsListener interface.
        :type listener: |StreamsListener|
        :param done: Call back interface called when operation is completed.
        :type done: |DoneSubscribe|

        :returns: Pending command handle, can be used to cancel the command.
        """
        raise NotImplementedError("Abstract method")

    def unsubscribe(self, stream_type, listener, done):
        """Unsubscribe the client from given stream source type.

        .. note:: It is up to each service to implement its stream type if
                  required. For opensource services, |processes| uses
                  ``Processes`` for stream type, and |terminals| uses
                  ``Terminals``

        :param stream_type: The stream source type.
        :param listener: Client implementation of StreamsListener interface.
        :type listener: |StreamsListener|
        :param done: Call back interface called when operation is completed.
        :type done: |DoneUnsubscribe|

        :returns: Pending command handle, can be used to cancel the command.
        """
        raise NotImplementedError("Abstract method")

    def read(self, stream_id, size, done):
        """Read data from a stream. If stream buffer is empty, the command will
        wait until data is available.

        Remote peer will continue to process other commands while |read|
        command is pending.

        Client can send more |read| commands without waiting for the first
        command to complete.

        Doing that improves communication channel bandwidth utilization.
        Pending |read| commands will be executed in same order as issued.

        Client can delay sending of |read| command if it is not ready to
        receive more data, however, delaying for too long can cause stream
        buffer overflow and lost of data.

        :param stream_id: ID of the stream to read from.
        :type stream_id: |basestring|
        :param size: Max number of bytes to read.
        :type size: |int|
        :param done: Call back interface called when operation is completed.
        :type done: |DoneRead|

        :returns: Pending command handle, can be used to cancel the command.
        """
        raise NotImplementedError("Abstract method")

    def write(self, stream_id, buf, offset, size, done):
        """Write data to a stream. If stream buffer is full, the command will
        wait until space is available.

        Remote peer will continue to process other commands while |write|
        command is pending.

        Client can send more |write| commands without waiting for the first
        command to complete. Doing that improves communication channel
        bandwidth utilization.

        Pending |write| commands will be executed in same order as issued.

        :param stream_id: ID of the stream to write to.
        :type stream_id: |basestring|
        :param buf: Buffer that contains stream data.
        :type buf: |bytearray|
        :param offset: Byte offset in the buffer.
        :type offset: |int|
        :param size: Number of bytes to write.
        :type size: |int|
        :param done: Call back interface called when operation is completed.
        :type done: |DoneWrite|

        :returns: Pending command handle, can be used to cancel the command.
        """
        raise NotImplementedError("Abstract method")

    def eos(self, stream_id, done):
        """Send End Of Stream marker to a stream.

        No more writing to the stream is allowed after that.

        :param stream_id: ID of the stream to senf EOS to.
        :type stream_id: |basestring|
        :param done: Call back interface called when operation is completed.
        :type done: |DoneEOS|

        :returns: Pending command handle, can be used to cancel the command.
        """
        raise NotImplementedError("Abstract method")

    def connect(self, stream_id, done):
        """Connect client to a stream.

        Some data might be dropped from the stream by the time |connect|
        command is executed.

        Client should be able to re-sync with stream data if it wants to read
        from such stream.

        If a client wants to read a stream from the beginning it should use
        |subscribe| command instead of |connect|.

        :param stream_id: ID of the stream to connect to.
        :type stream_id: |basestring|
        :param done: Call back interface called when operation is completed.
        :type done: |DoneConnect|

        :returns: Pending command handle, can be used to cancel the command.
        """
        raise NotImplementedError("Abstract method")

    def disconnect(self, stream_id, done):
        """Disconnect client from a stream.

        :param stream_id: ID of the stream to disconnect from.
        :type stream_id: |basestring|
        :param done: Call back interface called when operation is completed.
        :type done: |DoneDisconnect|

        :returns: Pending command handle, can be used to cancel the command.
        """
        raise NotImplementedError("Abstract method")


class StreamsListener(object):
    """Clients can implement StreamsListener interface to be notified
    when a stream is created or disposed.

    The interface is registered with |subscribe| command.

    When new stream is created, client must decide if it is interested in that
    particular stream instance.

    If not interested, client should send |disconnect| command to allow remote
    peer to free resources and bandwidth.

    If not disconnected, client is required to send |read| commands as
    necessary to prevent stream buffer overflow.
    """

    def created(self, stream_type, stream_id, context_id):
        """Called when a new stream is created.

        .. note:: It is up to each service to implement its stream type if
                  required. For opensource services, |processes| uses
                  ``Processes`` for stream type, and |terminals| uses
                  ``Terminals``

        :param stream_type: Source type of the stream.
        :type stream_type: |basestring|
        :param stream_id: ID of the created stream.
        :type stream_id: |basestring|
        :param context_id: a context ID that is associated with the stream,
                           or **None**. Exact meaning of the context ID depends
                           on stream type. Stream types and context IDs are
                           defined by services that use Streams service to
                           transmit data
        """
        pass

    def disposed(self, stream_type, stream_id):
        """Called when a stream is disposed.

        .. note:: It is up to each service to implement its stream type if
                  required. For opensource services, |processes| uses
                  ``Processes`` for stream type, and |terminals| uses
                  ``Terminals``

        :param stream_type: Source type of the stream.
        :type stream_type: |basestring|
        :param stream_id: ID of the disposed stream.
        :type stream_id: |basestring|
        """
        pass


class DoneSubscribe(object):
    """Call back interface for |subscribe| command."""

    def doneSubscribe(self, token, error):
        """Called when stream subscription is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        """
        pass


class DoneUnsubscribe(object):
    """Call back interface for |unsubscribe| command."""

    def doneUnsubscribe(self, token, error):
        """Called when stream unsubscription is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        """
        pass


class DoneRead(object):
    """Call back interface for |read| command."""

    def doneRead(self, token, error, lost_size, data, eos):
        """Called when |read| command is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        :param lost_size: Number of bytes that were lost because of buffer
                          overflow. A *lost_size* of **-1** means unknown
                          number of bytes were lost. If both *lost_size* and
                          *data.length* are non-zero then lost bytes are
                          considered located right before read bytes.
        :type lost_size: |int|
        :param data: Bytes read from the stream.
        :type data: |bytearray|
        :param eos: **True** if end of stream was reached.
        :type eos: |bool|
        """
        pass


class DoneWrite(object):
    """Call back interface for |write| command."""

    def doneWrite(self, token, error):
        """Called when |write| command is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        """
        pass


class DoneEOS(object):
    """Call back interface for |eos| command."""

    def doneEOS(self, token, error):
        """Called when |eos| command is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        """
        pass


class DoneConnect(object):
    """Call back interface for |connect| command."""

    def doneConnect(self, token, error):
        """Called when |connect| command is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        """
        pass


class DoneDisconnect(object):
    """Call back interface for |disconnect| command."""

    def doneDisconnect(self, token, error):
        """Called when |disconnect| command is done.

        :param token: Pending command handle.
        :param error: Error description if operation failed, **None** if
                      succeeded.
        """
        pass
