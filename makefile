.PHONY: server login run clear

server:
	python scripts/set_up_server.py

login-manual:
	python -i scripts/login.py 

run: clear
	./scripts/run.sh

clear:
	./scripts/clear.sh