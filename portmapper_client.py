import sys
import grpc
import portmapper_pb2
import portmapper_pb2_grpc

def run():
    if len(sys.argv) != 2:
        print("Error args")
        return

    server_address = sys.argv[1]

    try:
        with grpc.insecure_channel(server_address) as channel:
            stub = portmapper_pb2_grpc.PortMapperStub(channel)

            for line in sys.stdin:
                parts = line.strip().split()
                if not parts:
                    continue

                command = parts[0]

                if command not in ['R', 'U', 'G', 'T']:
                    continue

                try:
                    if command == 'R' and len(parts) == 3:
                        name = parts[1]
                        value = float(parts[2])
                        response = stub.RegisterService(portmapper_pb2.RegisterRequest(name=name, value=value))
                        print(response.port)
                        continue
                    
                    if command == 'U' and len(parts) == 2:
                        port = int(parts[1])
                        response = stub.UnregisterService(portmapper_pb2.UnregisterRequest(port=port))
                        print(response.status)
                        continue

                    if command == 'G' and len(parts) == 2:
                        name = parts[1]
                        response = stub.GetServiceInfo(portmapper_pb2.GetInfoRequest(name=name))
                        if response.port != -1:
                            print(f"{response.port} {response.value:.6f}")
                        continue

                    if command == 'T' and len(parts) == 1:
                        response = stub.Terminate(portmapper_pb2.TerminateRequest())
                        print(response.registered_services_count)
                        break 


                except ValueError:
                    continue

    except grpc.RpcError as e:
        print(f"Erro de RPC: {e.code()} - {e.details()}", file=sys.stderr)
    except Exception as e:
        print(f"Ocorreu um erro: {e}", file=sys.stderr)

if __name__ == '__main__':
    run()