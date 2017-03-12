venv: requirements.txt
	virtualenv venv
	venv/bin/pip install -q --upgrade pip
	venv/bin/pip install -q --editable .
	venv/bin/pip install -q -r requirements.txt
	venv/bin/pip install -q yamllint pep8 nose

test: venv FORCE
	venv/bin/pep8 . --exclude venv --max-line-length 120
	venv/bin/yamllint .
	venv/bin/nosetests --with-coverage

coveralls: test FORCE
	venv/bin/coveralls

fetch:	venv FORCE
	venv/bin/python bin/fetch.py

update:	venv FORCE
	venv/bin/python bin/update.py

clean:
	rm -rf venv *.pyc .cache tests/__pycache__ .coverage taas.egg-info htmlcov

# Magical line that allows us to force execution of a target
FORCE:
