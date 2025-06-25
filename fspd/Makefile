.PHONY: all clean run_cli_portmapper run_portmapper_1 run_portmapper_2 run_registry run_cli_registry

PROTOC=python3 -m grpc_tools.protoc
PYTHON=python3

all: pm_pb2.py pm_pb2_grpc.py reg_pb2.py reg_pb2_grpc.py

pm_pb2.py pm_pb2_grpc.py: pm.proto
	$(PROTOC) -I. --python_out=. --grpc_python_out=. --proto_path=. pm.proto

reg_pb2.py reg_pb2_grpc.py: reg.proto
	$(PROTOC) -I. --python_out=. --grpc_python_out=. --proto_path=. reg.proto

clean: 
	rm -f pm_pb2.py pm_pb2_grpc.py reg_pb2.py reg_pb2_grpc.py __pycache__/*

run_cli_portmapper: all
	$(PYTHON) cln_pm.py $(arg)

run_portmapper_1: all
	$(PYTHON) svc_pm.py $(arg)

run_portmapper_2: all
	$(PYTHON) svc_pm.py $(arg1) $(arg2)

run_registry: all
	$(PYTHON) svc_reg.py $(arg)

run_cli_registry: all
	$(PYTHON) cln_reg.py $(arg)