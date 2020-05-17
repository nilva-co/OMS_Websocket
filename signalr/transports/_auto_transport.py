from ._transport import Transport
from ._sse_transport import ServerSentEventsTransport
from ._ws_transport import WebSocketsTransport


class AutoTransport(Transport):
    def __init__(self, session, connection, token):
        Transport.__init__(self, session, connection, token)
        self.__available_transports = [
            WebSocketsTransport(session, connection, token),
            ServerSentEventsTransport(session, connection, token)
        ]
        self.__transport = None

    def negotiate(self, **kwargs):
        negotiate_data = Transport.negotiate(self)
        self.__transport = self.__get_transport(negotiate_data)

        return negotiate_data

    def __get_transport(self, negotiate_data):
        for transport in self.__available_transports:
            if transport.accept(negotiate_data):
                return transport
        raise Exception('Cannot find suitable transport')

    def start(self, **kwargs):
        return self.__transport.start(**kwargs)

    def send(self, data):
        self.__transport.send(data)

    def close(self):
        self.__transport.close()

    def _get_name(self):
        return 'auto'
