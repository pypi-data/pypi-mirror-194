import grpc
import arizon_usb_apiserver.grpc.force_packet_pb2 as force_packet_pb2
import arizon_usb_apiserver.grpc.force_packet_pb2_grpc as force_packet_pb2_grpc

class Client:
    endpoint: str
    channel: grpc.Channel = None
    stub: force_packet_pb2_grpc.ForcePacketServiceStub = None
    def __init__(self, endpoint: str) -> None:
        self.endpoint = endpoint
        self.channel = grpc.insecure_channel(self.endpoint)
        self.stub = force_packet_pb2_grpc.ForcePacketServiceStub(self.channel)

    def reconnect(self):
        if self.channel is not None:
            self.channel.close()
        self.channel = grpc.insecure_channel(self.endpoint)
        self.stub = force_packet_pb2_grpc.ForcePacketServiceStub(self.channel)

def get_client(endpoint: str) -> Client:
    return Client(endpoint)

