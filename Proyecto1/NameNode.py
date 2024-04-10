import grpc
import Service_pb2
import Service_pb2_grpc
from concurrent import futures

class NameNodeService(Service_pb2_grpc.NameNodeServiceServicer):
    def ListAllStoredChunks(self, request, context):
        data_nodes = ["54.87.188.179:50052", "44.211.137.11:50053", "34.204.7.252:50054"]
        all_chunks = {}

        for datanode in data_nodes:
            chunks = obtener_chunks_de_datanode(datanode)
            chunk_names = Service_pb2.ChunkNames(chunkName=chunks)
            all_chunks[datanode] = chunk_names

        return Service_pb2.AllChunksResponse(chunks=all_chunks)

def obtener_chunks_de_datanode(datanode_address):
    with grpc.insecure_channel(datanode_address) as channel:
        stub = Service_pb2_grpc.DataNodeServiceStub(channel)
        response = stub.ListStoredChunks(Service_pb2.Empty())
        return response.chunkNames    

def main():
    data_nodes = ["54.87.188.179:50052", "44.211.137.11:50053", "34.204.7.252:50054"]
    todos_los_chunks = {}

    for datanode in data_nodes:
        chunks = obtener_chunks_de_datanode(datanode)
        todos_los_chunks[datanode] = chunks

    # Imprimir la información recopilada
    for datanode, chunks in todos_los_chunks.items():
        print(f"DataNode {datanode} tiene los siguientes chunks:")
        for chunk in chunks:
            print(f" - {chunk}")

def iniciar_servidor_namenode():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Service_pb2_grpc.add_NameNodeServiceServicer_to_server(NameNodeService(), server)
    server.add_insecure_port('0.0.0.0:50055')  # Elige un puerto adecuado para el NameNode
    print("NameNode ejecutándose en el puerto 50055...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    iniciar_servidor_namenode()