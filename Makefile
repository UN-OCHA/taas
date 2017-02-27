all:
	virtualenv venv
	venv/bin/pip install --upgrade .
	venv/bin/pip install -r requirements.txt

test:
	venv/bin/pytest tests

clean:
	rm -rf venv *.pyc .cache tests/__pycache__
