from concurrent import futures
import sys
import threading
import time
import grpc
import portmapper_pb2
import portmapper_pb2_grpc

class PortMapperService(portmapper_pb2_grpc.PortMapperServicer):
    def __init__(self, server_intance):
        self._server = server_intance
        self._services = {}
        self._ports = {}
        self._next_port = 1025
        self._lock = threading.Lock()

    def RegisterService(self, request, context):
        with self._lock:
            if request.name in self._services:
                self._services[request.name]['value'] = request.value
                return portmapper_pb2.RegisterReply(port=self._services[request.name]['port'])
            port = self._next_port
            self._next_port +=1
            self._services[request.name] = {'port': port, 'value': request.value}
            self._ports[port] = request.name
            return portmapper_pb2.RegisterReply(port=port)
        
    def UnregisterService(self, request, context):
        with self._lock:
            for name, service in list(self._services.items()):
                if service['port'] == request.port:
                    del self._services[name]
                    del self._ports[request.port]
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
    if len(sys.argv) != 2:
        print("Args error")
        sys.exit(1)

    port = sys.argv[1]

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    portmapper_pb2_grpc.add_PortMapperServicer_to_server(PortMapperService(server), server)

    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"Server stated on port {port}")
    server.wait_for_termination()
    print("Server terminated")

if __name__ == '__main__':
    serve()
