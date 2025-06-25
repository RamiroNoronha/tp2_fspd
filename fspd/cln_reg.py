import sys
from __future__ import print_function
import grpc
import reg_pb2, reg_pb2_grpc, pm_pb2, pm_pb2_grpc 

def run():
    if len(sys.argv) < 1:
        sys.exit(1)
    
    channel = grpc.insecure_channel(sys.argv[1])
    registry_stub = reg_pb2_grpc.RegistryStub(channel)
    while 1:
        try:
            input_ = input()
        except EOFError:
            break
        
        if command[0] == 'Q':
            response = registry_stub.query(
                reg_pb2.QueryRequest(service_name=command[1])
            )
            address = response.pm_address
            if address:
                portmapper_channel = grpc.insecure_channel(address)
                portmapper_stub = pm_pb2_grpc.PortMapperStub(portmapper_channel)
                response = portmapper_stub.get_service_info(
                    pm_pb2.GetServiceInfoRequest(service_name=command[1])
                )
                print(f"{response.port} {response.value:.6f}")
        elif command[0] == 'F':
            response = registry_stub.finalize(
                reg_pb2.FinalizeRequest()
            )
            print(response.num_services)
            break

        else:
            continue

if __name__ == '__main__':
    run()
