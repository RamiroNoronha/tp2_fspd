import sys
import grpc
import registry_pb2
import registry_pb2_grpc
import portmapper_pb2
import portmapper_pb2_grpc

def run():
    if len(sys.argv) != 2:
        print("Args error")
        return

    registry_address = sys.argv[1]

    try:
        with grpc.insecure_channel(registry_address) as registry_channel:
            registry_stub = registry_pb2_grpc.RegistryStub(registry_channel)

            for line in sys.stdin:
                parts = line.strip().split()
                if not parts:
                    continue
                
                command = parts[0]

                if command == 'Q' and len(parts) == 2:
                    name = parts[1]
                    query_response = registry_stub.QueryService(registry_pb2.QueryRequest(name=name))
                    
                    portmapper_locator = query_response.portmapper_location
                    if not portmapper_locator:
                        continue

                    try:
                        with grpc.insecure_channel(portmapper_locator) as pm_channel:
                            pm_stub = portmapper_pb2_grpc.PortMapperStub(pm_channel)
                            info_response = pm_stub.GetServiceInfo(portmapper_pb2.GetInfoRequest(name=name))
                            
                            if info_response.port != -1:
                                print(f"{info_response.port} {info_response.value:.6f}")
                    except grpc.RpcError as e:
                        print(f"ERRO: Falha ao contatar portmapper em {portmapper_locator}: {e.details()}", file=sys.stderr)
                    
                    continue
                if command == 'F' and len(parts) == 1:
                    finalize_response = registry_stub.Finalize(registry_pb2.FinalizeRequest())
                    print(finalize_response.registered_services_count)
                    break
                
    except grpc.RpcError as e:
        print(f"ERRO: Failt to connect to the registry service {registry_address}: {e.details()}", file=sys.stderr)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)

if __name__ == '__main__':
    run()