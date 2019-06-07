# We use --system-site-packages so we can potentially make Docker's life
# easier by installing deps from apk.

# We have some variables, used to tag the tag image. These can be overridden
# by passing different versions on the CLI.
ORGANISATION=unocha
IMAGE=taas
VERSION=1

# And some helper binaries.
AWK=awk
DATE=date
GIT=git
SED=sed

venv: requirements.txt
	virtualenv --system-site-packages venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install --upgrade appdirs
	venv/bin/pip install --upgrade --editable .
	venv/bin/pip install -r requirements.txt

test: venv FORCE
	venv/bin/nosetests --with-coverage --cover-package=.
	venv/bin/pep8 .
	venv/bin/yamllint -d relaxed .

# Reports tests to our CI providers and friends
test-report: test FORCE
	venv/bin/coveralls
	venv/bin/codeclimate-test-reporter

update:	venv FORCE
	venv/bin/gss2json --push

freeze:
	venv/bin/pip freeze | grep -v taas.git > requirements.txt

# Tee the output to file, so we can parse it for tagging.
docker:
	docker build \
		--build-arg VCS_REF=`$(GIT) rev-parse --short HEAD` \
		--build-arg VCS_URL=`$(GIT) config --get remote.origin.url | $(SED) 's#git@github.com:#https://github.com/#'` \
		--build-arg BUILD_DATE=`$(DATE) -u +"%Y-%m-%dT%H:%M:%SZ"` \
		--build-arg VERSION=$(VERSION) \
		-f Dockerfile . | tee buildlog.txt

tag:
	$(eval IMAGE_HASH=$(shell tail -n 1 buildlog.txt | $(AWK) '{print $$NF}'))
	docker tag $(IMAGE_HASH) $(ORGANISATION)/$(IMAGE):$(VERSION)

clean:
	rm -rf venv *.pyc taas/*.pyc .cache tests/__pycache__ .coverage taas.egg-info htmlcov buildlog.txt

# Magical line that allows us to force execution of a target
FORCE:
