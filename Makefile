all:
	virtualenv venv
	venv/bin/pip install --upgrade .
	venv/bin/pip install -r requirements.txt

clean:
	rm -rf venv *.pyc


