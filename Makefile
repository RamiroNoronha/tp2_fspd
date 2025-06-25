# Makefile para o exercício de gRPC em Python
# Este arquivo gerencia a geração de código e a execução dos servidores e clientes.

# --- Variáveis de Configuração ---

# Define o interpretador Python a ser usado. 'python3' é mais explícito.
PYTHON = python3

# Comando para invocar o compilador de Protocol Buffers do gRPC para Python.
PROTOC = $(PYTHON) -m grpc_tools.protoc

# Lista de todos os arquivos .proto que definem os serviços.
PROTO_FILES = portmapper.proto registry.proto

# Lista de todos os arquivos Python que serão gerados pelos .proto.
# O Makefile usará esta lista para saber o que construir e o que limpar.
PY_GENERATED_FILES = portmapper_pb2.py portmapper_pb2_grpc.py registry_pb2.py registry_pb2_grpc.py


# --- Regras Principais ---

# A regra 'all' é uma regra "falsa" (.PHONY) que serve como dependência principal.
# Ela garante que todo o código necessário (os stubs do gRPC) seja gerado.
.PHONY: all
all: $(PY_GENERATED_FILES)

# Regra para gerar os arquivos Python do gRPC (_pb2.py e _pb2_grpc.py).
# Ela só será executada se algum dos arquivos .proto for mais recente que os arquivos gerados,
# ou se os arquivos gerados não existirem.
$(PY_GENERATED_FILES): $(PROTO_FILES)
	@echo "==> Generating pythom files from .proto..."
	$(PROTOC) -I. --python_out=. --grpc_python_out=. $(PROTO_FILES)
	@echo "==> Stubs successfull generated."


# --- Regras de Execução ---
# Todas as regras de execução dependem de 'all' para garantir que os stubs
# do gRPC existam antes de tentar rodar os programas.

# Executa o servidor portmapper (comportamento da Etapa 1)
# Exemplo de uso: make run_portmapper_1 arg=50051
.PHONY: run_portmapper_1
run_portmapper_1: all
	$(PYTHON) portmapper_server.py $(arg)

# Executa o servidor portmapper (comportamento da Etapa 2)
# Exemplo de uso: make run_portmapper_2 arg1=50051 arg2=localhost:50052
.PHONY: run_portmapper_2
run_portmapper_2: all
	$(PYTHON) portmapper_server.py $(arg1) $(arg2)

# Executa o cliente do portmapper
# Exemplo de uso: make run_cli_portmapper arg=localhost:50051
.PHONY: run_cli_portmapper
run_cli_portmapper: all
	$(PYTHON) portmapper_client.py $(arg)

# Executa o servidor registry
# Exemplo de uso: make run_registry arg=50052
.PHONY: run_registry
run_registry: all
	$(PYTHON) registry_server.py $(arg)

# Executa o cliente do registry
# Exemplo de uso: make run_cli_registry arg=localhost:50052
.PHONY: run_cli_registry
run_cli_registry: all
	$(PYTHON) registry_client.py $(arg)


# --- Regra de Limpeza ---

# Remove todos os arquivos gerados e o diretório de cache do Python.
# .PHONY garante que a regra seja executada mesmo que exista um arquivo chamado 'clean'.
.PHONY: clean
clean:
	@echo "==> Cleaning generated files and python cache..."
	rm -f $(PY_GENERATED_FILES)
	rm -rf __pycache__
	@echo "==> All clean"
