PACKAGE=LB-CHORE
PROCESS_NAME=LB_CHORE

check:
	/opt/venv/bin/flake8

clean:
	@echo clean...
	@rm -rf log/*
	@rm -rf **/*.swp
	@rm -rf dist
	@rm -rf **/*.pyc
	@rm -rf **/__pycache__

run:
	/opt/venv/bin/uwsgi --ini etc/uwsgi.ini

reload:
	echo 'c' > master-fifo

stop:
	echo q > master-fifo

fstop:
	echo Q > master-fifo

kill:
	@echo "Stopping process: $(PROCESS_NAME)"
	@pgrep -f $(PROCESS_NAME) || echo "No process found with name: $(PROCESS_NAME)"
	@pkill -9 -f $(PROCESS_NAME)

install:
	python -m venv /opt/venv
	/opt/venv/bin/pip3 install --upgrade pip
	/opt/venv/bin/pip3 install -r requirements.txt