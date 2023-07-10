# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import stockbazaar_pb2 as stockbazaar__pb2


class CatalogStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Lookup = channel.unary_unary(
                '/Catalog/Lookup',
                request_serializer=stockbazaar__pb2.lookupStockName.SerializeToString,
                response_deserializer=stockbazaar__pb2.lookupResult.FromString,
                )
        self.Trade = channel.unary_unary(
                '/Catalog/Trade',
                request_serializer=stockbazaar__pb2.tradeStockName.SerializeToString,
                response_deserializer=stockbazaar__pb2.tradeResult.FromString,
                )


class CatalogServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Lookup(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Trade(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_CatalogServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Lookup': grpc.unary_unary_rpc_method_handler(
                    servicer.Lookup,
                    request_deserializer=stockbazaar__pb2.lookupStockName.FromString,
                    response_serializer=stockbazaar__pb2.lookupResult.SerializeToString,
            ),
            'Trade': grpc.unary_unary_rpc_method_handler(
                    servicer.Trade,
                    request_deserializer=stockbazaar__pb2.tradeStockName.FromString,
                    response_serializer=stockbazaar__pb2.tradeResult.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Catalog', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Catalog(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Lookup(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Catalog/Lookup',
            stockbazaar__pb2.lookupStockName.SerializeToString,
            stockbazaar__pb2.lookupResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Trade(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Catalog/Trade',
            stockbazaar__pb2.tradeStockName.SerializeToString,
            stockbazaar__pb2.tradeResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class OrderStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Request = channel.unary_unary(
                '/Order/Request',
                request_serializer=stockbazaar__pb2.requestStockName.SerializeToString,
                response_deserializer=stockbazaar__pb2.requestResult.FromString,
                )


class OrderServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Request(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_OrderServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Request': grpc.unary_unary_rpc_method_handler(
                    servicer.Request,
                    request_deserializer=stockbazaar__pb2.requestStockName.FromString,
                    response_serializer=stockbazaar__pb2.requestResult.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Order', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Order(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Request(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Order/Request',
            stockbazaar__pb2.requestStockName.SerializeToString,
            stockbazaar__pb2.requestResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)