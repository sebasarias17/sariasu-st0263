import grpc
import Service_pb2
import Service_pb2_grpc
from concurrent import futures
import os

class DataNodeService(Service_pb2_grpc.DataNodeServiceServicer):
    def __init__(self):
        self.stored_chunks = {}
    
    def StoreChunk(self, request, context):
        chunk_key = f"{request.fileName}_part_{request.partNumber}"
        self.stored_chunks[chunk_key] = request.content
        return Service_pb2.StoreChunkResponse(success=True, message="Chunk almacenado en memoria.") 
    
    def ListStoredChunks(self, request, context):
        return Service_pb2.ChunkList(chunkNames=list(self.stored_chunks.keys()))
    
    def GetChunk(self, request, context):
        chunk_key = f"{request.fileName}_part_{request.partNumber}"
        if chunk_key in self.stored_chunks:
            return Service_pb2.ChunkResponse(content=self.stored_chunks[chunk_key])
        else:
            # Manejo de errores, por ejemplo, si el chunk no existe
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Chunk no encontrado')
            return Service_pb2.ChunkResponse()

def iniciar_servidor_datanode():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), options=[
        ('grpc.max_send_message_length', 100 * 1024 * 1024),
        ('grpc.max_receive_message_length', 100 * 1024 * 1024)
    ])
    Service_pb2_grpc.add_DataNodeServiceServicer_to_server(DataNodeService(), server)
    server.add_insecure_port('[::]:50052')  # El puerto puede variar para cada DataNode
    print("DataNode ejecutándose en el puerto 50052...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    iniciar_servidor_datanode()
