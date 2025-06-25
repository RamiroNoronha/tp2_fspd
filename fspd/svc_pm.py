import sys
import grpc
import threading
from concurrent import futures
import socket

import pm_pb2, pm_pb2_grpc, reg_pb2, reg_pb2_grpc 

class PortMapper(pm_pb2_grpc.PortMapperServicer):
   def __init__(self, stop_event, registry_address=None, portmapper_port_=5555):
      self.services = {}
      self.next_port = 1025
      self._stop_event = stop_event
      self.registry_address = registry_address
      self.portmapper_port = portmapper_port_
      if registry_address:
         self.registry_channel = grpc.insecure_channel(registry_address)
      else:
         self.registry_channel = None

   def register_service(self, request, context):
      name = request.service_name
      value = request.value
      if name in self.services:
         self.services[name]['value'] = value
         port = self.services[name]['port']
      else:
         port = self.next_port
         self.services[name] = {'value': value, 'port': port}
         self.next_port += 1
      if self.registry_channel:
         fqdn = socket.getfqdn()
         registry_stub = reg_pb2_grpc.RegistryStub(self.registry_channel)
         registry_stub.map(reg_pb2.MapRequest(service_name=name, pm_address=f'{fqdn}:{self.portmapper_port}'))
      return pm_pb2.RegisterServiceReply(port=port)
   
   def unregister_service(self, request, context):
      port = request.port
      for name, service in list(self.services.items()):
         if service['port'] == port:
            del self.services[name]
            if self.registry_channel:
               registry_stub = reg_pb2_grpc.RegistryStub(self.registry_channel)
               registry_stub.unmap(reg_pb2.UnMapRequest(service_name=name))
            return pm_pb2.UnregisterServiceReply(success=0)
      return pm_pb2.UnregisterServiceReply(success=-1)
   
   def get_service_info(self, request, context):
      name = request.service_name
      if name in self.services:
         port = self.services[name]['port']
         value = self.services[name]['value']
         return pm_pb2.GetServiceInfoReply(port=port, value=value)
      else:
         return pm_pb2.GetServiceInfoReply(port=-1, value=0.0)
      
   def terminate(self, request, context):
      self._stop_event.set()
      return pm_pb2.TerminateReply(num_services=len(self.services))
   

def serve():
   stop_event = threading.Event()
   server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
   if len(sys.argv) > 2:
      port = sys.argv[1]
      registry_address = sys.argv[2]
      portmapper = PortMapper(stop_event, registry_address, portmapper_port_=int(port))
      server.add_insecure_port(f'localhost:{port}')
   elif len(sys.argv) > 1:
      port = sys.argv[1]
      portmapper = PortMapper(stop_event)
      server.add_insecure_port(f'localhost:{port}')
   else:
      sys.exit(1)
   pm_pb2_grpc.add_PortMapperServicer_to_server(portmapper, server)
   server.start()
   stop_event.wait()
   server.stop(1)
   

if __name__ == '__main__':
    serve()
