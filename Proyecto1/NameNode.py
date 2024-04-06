import grpc
import Service_pb2
import Service_pb2_grpc
from concurrent import futures

class ClientCallService(Service_pb2_grpc.ClientCallServiceServicer):
    def __init__(self):
        self.chunks = {}

    def sendPartitionFile(self, request, context):
        file_name = request.fileName
        part_number = request.partNumber
        chunk_key = f"{file_name}/part-{part_number:04d}"
        
        self.chunks[chunk_key] = request.content
        return Service_pb2.Request(requestFile=chunk_key)
    
    def ListStoredChunks(self, request, context):
        return Service_pb2.ChunkList(chunks=list(self.chunks.keys()))
    
#    def GetChunkDetails(self, request, context):
#        chunk_info = {key: len(value) for key, value in self.chunks.items()}
#        return Service_pb2.ChunkDetails(chunkInfo=chunk_info)

def iniciar_servidor():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), options=[
        ('grpc.max_send_message_length', 100 * 1024 * 1024),
        ('grpc.max_receive_message_length', 100 * 1024 * 1024)
    ])

    Service_pb2_grpc.add_ClientCallServiceServicer_to_server(ClientCallService(), server)
    server.add_insecure_port('[::]:50051')
    print("Service is running... ")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    iniciar_servidor()