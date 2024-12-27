all: databese_up creat_paste_bibs build_bib_funcao_postgree build_bib_sincronizacao_servidor_cliente
server: all install_requeriments_server run_server
cliente: all install_requeriments_cliente run_cliente

install_depedencia:
	@sudo apt-get update
	@sudo apt-get install python3-venv python3-pip docker.io docker-compose python3-poetry -y
	@sudo apt install libxcb-xinerama0 libxcb-xinerama0-dev libxcb1 libxcb1-dev libxkbcommon-x11-0 -y

venv:
	@test -d .venv || python3 -m venv .venv
	@chmod -R u+x .venv
	# @source .venv/bin/activate

clear:
	@rm -rf server/bibs
	@rm -rf cliente/bibs
	@rm -rf bib_funcao_postgree/dist
	@rm -rf bib_sincronizacao_servidor_cliente/dist


databese_up:
	@sudo docker-compose up -d --build

creat_paste_bibs:
	@mkdir server/bibs -p
	@mkdir cliente/bibs -p

build_bib_funcao_postgree:
	@cd bib_funcao_postgree && make
	@cp ./bib_funcao_postgree/dist/funcao_postgree-0.1.0-py3-none-any.whl ./cliente/bibs/
	@cp ./bib_funcao_postgree/dist/funcao_postgree-0.1.0-py3-none-any.whl ./server/bibs/

build_bib_sincronizacao_servidor_cliente:
	@cd bib_sincronizacao_servidor_cliente && make
	@cp ./bib_sincronizacao_servidor_cliente/dist/sincronizacao_servidor_cliente-0.1.0-py3-none-any.whl ./cliente/bibs/
	@cp ./bib_sincronizacao_servidor_cliente/dist/sincronizacao_servidor_cliente-0.1.0-py3-none-any.whl ./server/bibs/

install_requeriments_server:
	@cd server && pip install bibs/funcao_postgree-0.1.0-py3-none-any.whl --force-reinstall
	@cd server && pip install bibs/sincronizacao_servidor_cliente-0.1.0-py3-none-any.whl --force-reinstall
	@cd server && pip install -r requirements.txt

install_requeriments_cliente:
	@cd cliente && pip install bibs/funcao_postgree-0.1.0-py3-none-any.whl --force-reinstall
	@cd cliente && pip install bibs/sincronizacao_servidor_cliente-0.1.0-py3-none-any.whl --force-reinstall
	@cd cliente && pip install -r requirements.txt

run_server:
	@clear
	@cd server && python3 main.py

run_cliente:
	@clear
	@cd cliente && python3 main.py