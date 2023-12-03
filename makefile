init:
	python -m venv .venv && \
	. .venv/bin/activate && \
	pip install -r requirements.txt 

init-db:
	mysql -u root -p < init.sql && \
	flask fill-db