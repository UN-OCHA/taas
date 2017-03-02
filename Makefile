all:
	virtualenv venv
	venv/bin/pip install -q --upgrade .
	venv/bin/pip install -q -r requirements.txt

test:	all
	venv/bin/pytest tests

clean:
	rm -rf venv *.pyc .cache tests/__pycache__
