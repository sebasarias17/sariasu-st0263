import grpc
import Service_pb2
import Service_pb2_grpc
from concurrent import futures

class ClientCallService(Service_pb2_grpc.ClientCallServiceServicer):
    def sendFile(self, request, context):
        variable = request.content
        return Service_pb2.Request(requestFile = "Enviado!")

def iniciar_servidor():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Service_pb2_grpc.add_ClientCallServiceServicer_to_server(ClientCallService(), server)
    server.add_insecure_port('[::]:50051')
    print("Service is running... ")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    iniciar_servidor()