all:
	virtualenv venv
	venv/bin/pip install -q --upgrade .
	venv/bin/pip install -q -r requirements.txt

test:	all
	venv/bin/pytest tests

cover:	all
	venv/bin/pytest --cov=. tests

fetch:	all
	venv/bin/python bin/fetch.py

update:	all
	venv/bin/python bin/update.py

clean:
	rm -rf venv *.pyc .cache tests/__pycache__
