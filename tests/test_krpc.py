import asyncio

import pytest

from aiomdht import krpc

from .utils import BufferDatagramTransport


def describe_generate_transaction_id():

    def is_bytes():
        transaction_id = krpc.generate_transaction_id()

        assert isinstance(transaction_id, bytes)


def describe_krpc_protocol():

    def describe_query():

        krpc.generate_transaction_id = lambda: b'aa'

        @pytest.mark.asyncio
        async def request_is_properly_encoded(event_loop):
            transport, protocol = BufferDatagramTransport.connect_protocol(
                krpc.KRPCProtocol(loop=event_loop)
            )

            with pytest.raises(asyncio.TimeoutError):
                await protocol.query(('127.0.0.1', 1234), 'ping', timeout=0.1, id=b'abcdefghij0123456789')

            assert transport.buffer.getvalue() == b'd1:ad2:id20:abcdefghij0123456789e1:q4:ping1:t2:aa1:y1:qe'

        @pytest.mark.asyncio
        async def received_response_to_request(event_loop):
            transport, protocol = BufferDatagramTransport.connect_protocol(
                krpc.KRPCProtocol(loop=event_loop)
            )

            event_loop.call_later(
                1,
                protocol.datagram_received,
                b'd1:rd2:id20:mnopqrstuvwxyz123456e1:t2:aa1:y1:re',
                ('192.168.0.1', 8973)
            )

            result = await protocol.query(('127.0.0.1', 1234), 'ping', timeout=2, id=b'abcdefghij0123456789')

            assert result == {b'id': b'mnopqrstuvwxyz123456'}

        @pytest.mark.asyncio
        async def received_error_to_request(event_loop):
            transport, protocol = BufferDatagramTransport.connect_protocol(
                krpc.KRPCProtocol(loop=event_loop)
            )

            event_loop.call_later(
                1,
                protocol.datagram_received,
                b'd1:eli201e23:A Generic Error Ocurrede1:t2:aa1:y1:ee',
                ('192.168.0.1', 8973)
            )

            with pytest.raises(krpc.KRPCError):
                await protocol.query(('127.0.0.1', 1234), 'ping', timeout=2, id=b'abcdefghij0123456789')

        @pytest.mark.asyncio
        async def received_query_with_invalid_method(event_loop):
            transport, protocol = BufferDatagramTransport.connect_protocol(
                krpc.KRPCProtocol(loop=event_loop)
            )

            protocol.datagram_received(
                b'd1:ad2:id20:abcdefghij0123456789e1:q4:ping1:t2:aa1:y1:qe',
                ('192.168.0.1', 8973)
            )

            assert transport.buffer.getvalue() == b'd1:eli204e14:Method Unknowne1:t2:aa1:y1:ee'

        @pytest.mark.asyncio
        async def received_query_with_valid_method(event_loop):

            class TestKRPCProtocol(krpc.KRPCProtocol):

                def on_test(self):
                    return {
                        b'foo': b'bar'
                    }

            transport, protocol = BufferDatagramTransport.connect_protocol(
                TestKRPCProtocol(loop=event_loop)
            )

            protocol.datagram_received(
                b'd1:ade1:q4:test1:t2:aa1:y1:qe',
                ('192.168.0.1', 8973)
            )

            assert transport.buffer.getvalue() == b'd1:rd3:foo3:bare1:t2:aa1:y1:re'

        @pytest.mark.asyncio
        async def received_query_with_valid_method_and_args(event_loop):

            class TestKRPCProtocol(krpc.KRPCProtocol):

                def on_test(self, id):
                    return {
                        b'id': id
                    }

            transport, protocol = BufferDatagramTransport.connect_protocol(
                TestKRPCProtocol(loop=event_loop)
            )

            protocol.datagram_received(
                b'd1:ad2:id20:abcdefghij0123456789e1:q4:test1:t2:aa1:y1:qe',
                ('192.168.0.1', 8973)
            )

            assert transport.buffer.getvalue() == b'd1:rd2:id20:abcdefghij0123456789e1:t2:aa1:y1:re'

        @pytest.mark.asyncio
        async def protocol_error_on_bad_args(event_loop):

            class TestKRPCProtocol(krpc.KRPCProtocol):

                def on_test(self, id):
                    return {
                        b'id': id
                    }

            transport, protocol = BufferDatagramTransport.connect_protocol(
                TestKRPCProtocol(loop=event_loop)
            )

            protocol.datagram_received(
                b'd1:ad2:ie20:abcdefghij0123456789e1:q4:test1:t2:aa1:y1:qe',
                ('192.168.0.1', 8973)
            )

            assert transport.buffer.getvalue() == b'd1:eli203e14:Protocol Errore1:t2:aa1:y1:ee'

        @pytest.mark.asyncio
        async def server_error_on_exception(event_loop):

            class TestKRPCProtocol(krpc.KRPCProtocol):

                def on_test(self):
                    raise ValueError

            transport, protocol = BufferDatagramTransport.connect_protocol(
                TestKRPCProtocol(loop=event_loop)
            )

            protocol.datagram_received(
                b'd1:ade1:q4:test1:t2:aa1:y1:qe',
                ('192.168.0.1', 8973)
            )

            assert transport.buffer.getvalue() == b'd1:eli202e12:Server Errore1:t2:aa1:y1:ee'