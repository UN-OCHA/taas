venv: requirements.txt
	virtualenv venv
	venv/bin/pip install -q --upgrade pip
	venv/bin/pip install -q --upgrade --editable .
	venv/bin/pip install -q -r requirements.txt

test: venv FORCE
	venv/bin/pep8 . --exclude venv --max-line-length 120
	venv/bin/yamllint .
	venv/bin/nosetests --with-coverage --cover-package=.

# Reports tests to our CI providers and friends
test-report: test FORCE
	venv/bin/coveralls
	venv/bin/codeclimate-test-reporter

fetch:	venv FORCE
	venv/bin/python bin/fetch.py

update:	venv FORCE
	venv/bin/python bin/update.py

freeze:
	venv/bin/pip freeze | grep -v taas.git > requirements.txt

clean:
	rm -rf venv *.pyc .cache tests/__pycache__ .coverage taas.egg-info htmlcov

# Magical line that allows us to force execution of a target
FORCE:
