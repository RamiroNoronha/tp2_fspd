from concurrent import futures
import sys
import threading
import time
import grpc
import registry_pb2
import registry_pb2_grpc

class RegistryService(registry_pb2_grpc.RegistryServicer):
    def __init__(self, server_instance):
        self._server = server_instance
        self._registry_data = {}
        self._lock = threading.Lock()

    def MapService(self, request, context):
        with self._lock:
            self._registry_data[request.name] = request.portmapper_location
            return registry_pb2.MapReply(number_of_services=len(self._registry_data))
    
    def UnmapService(self, request, context):
        with self._lock:
            if request.name in self._registry_data:
                del self._registry_data[request.name]
                return registry_pb2.UnmapReply(status=0)
            return registry_pb2.UnmapReply(status=-1)
    
    def QueryService(self, request, context):
        with self._lock:
            service_location = self._registry_data.get(request.name)
            if service_location:
                return registry_pb2.QueryReply(portmapper_location=service_location)
            return registry_pb2.QueryReply(portmapper_location='')
    
    def Finalize(self, request, context):
        with self._lock:
            count = len(self._registry_data)

        def shutdown():
            time.sleep(0.5)
            self._server.stop(0)
        
        threading.Thread(target=shutdown).start()

        return registry_pb2.FinalizeReply(registered_services_count=count)

def serve():
    if len(sys.argv) != 2:
        print('Args error')
        sys.exit(1)

    port = sys.argv[1]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    registry_pb2_grpc.add_RegistryServicer_to_server(RegistryService(server), server)

    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f'Server Registry started on port {port}')
    server.wait_for_termination()
    print("Server Registry finished")

if __name__ == '__main__':
    serve()