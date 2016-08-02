from asyncio import transports

import io


class BufferDatagramTransport(transports.DatagramTransport):

    buffer = None

    def __init__(self):
        super(BufferDatagramTransport, self).__init__()
        self.buffer = io.BytesIO()

    def sendto(self, data, addr=None):
        self.buffer.write(data)

    @classmethod
    def connect_protocol(cls, protocol):
        transport = cls()

        protocol.connection_made(transport)

        return transport, protocol