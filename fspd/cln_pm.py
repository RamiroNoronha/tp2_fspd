from __future__ import print_function
import sys
import grpc
import pm_pb2, pm_pb2_grpc

def run():
    if len(sys.argv) < 1:
        sys.exit(1)
    
    channel = grpc.insecure_channel(sys.argv[1])
    portmapper_stub = pm_pb2_grpc.PortMapperStub(channel)
    while 1:
        try:
            input_ = input()
        except EOFError:
            break
        command = input_.split()
        
        if command[0] == 'R':
            response = portmapper_stub.register_service(
                pm_pb2.RegisterServiceRequest(service_name=command[1], value=float(command[2]))
            )
            print(response.port)
        elif command[0] == 'U':
            response = portmapper_stub.unregister_service(
                pm_pb2.UnregisterServiceRequest(port=int(command[1]))
            )
            print(response.success)
        elif command[0] == 'G':
            response = portmapper_stub.get_service_info(
                pm_pb2.GetServiceInfoRequest(service_name=command[1])
            )
            if response.port != -1:
                print(f"{response.port} {response.value:.6f}")
        elif command[0] == 'T':
            response = portmapper_stub.terminate(
                pm_pb2.TerminateRequest()
            )
            print(f"{response.num_services} ")
            break

        else:
            break

if __name__ == '__main__':
    run()
