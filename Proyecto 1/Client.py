import grpc
import Service_pb2
import Service_pb2_grpc

def read_file(file_path):
    with open(file_path, 'rb') as file:
        return file.read()

file_path = './Archivo1.docx'
file_content = read_file(file_path)

with grpc.insecure_channel('localhost:50051') as channel:
    stub = Service_pb2_grpc.ClientCallServiceStub(channel)
    response = stub.sendFile(Service_pb2.File(content = file_content))
    print(response.requestFile)