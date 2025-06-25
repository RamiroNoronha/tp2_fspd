import grpc
import threading
from concurrent import futures
import sys
import reg_pb2, reg_pb2_grpc

class Registry(reg_pb2_grpc.RegistryServicer):
    def __init__(self, stop_event):
        self.service_map = {}
        self._stop_event = stop_event

    def map(self, request, context):
        name = request.service_name
        address = request.pm_address
        self.service_map[name] = address
        return reg_pb2.MapReply(num_services=len(self.service_map))
    
    def unmap(self, request, context):
        name = request.service_name
        if name in self.service_map:
            del self.service_map[name]
            return reg_pb2.UnMapReply(success=0)
        else:
            return reg_pb2.UnMapReply(success=-1)
    
    def query(self, request, context):
        name = request.service_name
        if name in self.service_map:
            address = self.service_map[name]
            return reg_pb2.QueryReply(pm_address=address) 
        else:
            return reg_pb2.QueryReply(pm_address="") 
        
    def finalize(self, request, context):
        self._stop_event.set()
        return reg_pb2.FinalizeReply(num_services=len(self.service_map))
   
   

def serve():
    stop_event = threading.Event()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    portmapper = Registry(stop_event)
    reg_pb2_grpc.add_RegistryServicer_to_server(portmapper, server)
    if len(sys.argv) > 1:
        address = sys.argv[1]
        server.add_insecure_port(f'localhost:{address}')
    else:
        sys.exit(1)
    server.start()
    stop_event.wait()
    server.stop(1)
   

if __name__ == '__main__':
    serve()
