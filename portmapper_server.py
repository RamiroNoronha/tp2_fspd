from concurrent import futures
import sys
import threading
import time
import grpc
import portmapper_pb2
import portmapper_pb2_grpc
import registry_pb2
import registry_pb2_grpc

class PortMapperService(portmapper_pb2_grpc.PortMapperServicer):
    def __init__(self, server_instance, own_port, registry_locator=None):
        self._server = server_instance
        self._own_locator = f"localhost:{own_port}"
        self._registry_locator = registry_locator

        self._services = {}
        self._next_port = 1025
        self._lock = threading.Lock()

    def _contact_registry(self, operation, name):
        if not self._registry_locator:
            return
        
        try:
            with grpc.insecure_channel(self._registry_locator) as channel:
                stub = registry_pb2_grpc.RegistryStub(channel)

                if operation == 'map':
                    stub.MapService(registry_pb2.MapRequest(name=name, portmapper_location=self._own_locator))
                elif operation == 'unmap':
                    stub.UnmapService(registry_pb2.UnmapRequest(name=name))

        except grpc.RpcError as error:
            print(f"ERRO: It wasn't possible to connect to the registry in {self._registry_locator}. Erro: {error.details()}", file=sys.stderr)    

    def RegisterService(self, request, context):
        with self._lock:
            if request.name in self._services:
                self._services[request.name]['value'] = request.value
                return portmapper_pb2.RegisterReply(port=self._services[request.name]['port'])
            port = self._next_port
            self._next_port +=1

            self._services[request.name] = {'port': port, 'value': request.value}

            self._contact_registry('map', request.name)
            return portmapper_pb2.RegisterReply(port=port)
        
    def UnregisterService(self, request, context):
        with self._lock:
            for name, service in list(self._services.items()):
                if service['port'] == request.port:
                    del self._services[name]
                    self._contact_registry('unmap', name)
                    return portmapper_pb2.UnregisterReply(status=0)
         
            return portmapper_pb2.UnregisterReply(status=-1)

    def GetServiceInfo(self, request, context):
        with self._lock:
            if request.name in self._services:
                return portmapper_pb2.GetInfoReply(port=self._services[request.name]['port'], value=self._services[request.name]['value'])
            
            return portmapper_pb2.GetInfoReply(port=-1, value=0.0)

    def Terminate(self, request, context):
        with self._lock:
            count = len(self._services)
        
        def shutdown():
            time.sleep(1) 
            self._server.stop(0)

        threading.Thread(target=shutdown).start()
        return portmapper_pb2.TerminateReply(registered_services_count=count)


def serve():
    if len(sys.argv) < 2:
        print("Args error")
        sys.exit(1)

    port = sys.argv[1]

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    registry_port = sys.argv[2] if len(sys.argv) == 3 else None
    portmapper_pb2_grpc.add_PortMapperServicer_to_server(PortMapperService(server, port, registry_port ), server)

    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"Server stated on port {port}")
    server.wait_for_termination()
    print("Server terminated")

if __name__ == '__main__':
    serve()
