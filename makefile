.PHONY: server login

server:
	python scripts/set_up_server.py

login-manual:
	python -i scripts/login.py 

run:
	./run.sh