FROM unocha/alpine-base-s6-python2:latest

MAINTAINER Paul Fenwick "paul@humanitarianresponse.info"

# Git is everyone's favourite source control manager
# Hub actually lets us make PRs to github
# openssh is the transport needed to make PRs to github
RUN apk add --update --no-cache git hub openssh
RUN apk add --update --no-cache make
RUN apk add --update --no-cache py-virtualenv

# These are needed so python can build its things
RUN apk add --update --no-cache gcc
RUN apk add --update --no-cache python-dev
RUN apk add --update --no-cache musl-dev
RUN apk add --update --no-cache linux-headers
RUN apk add --update --no-cache libffi-dev
RUN apk add --update --no-cache openssl-dev

# What we expect now:
# - Jenkins checks out taas and taas-data and mounts them
# - Jenkins passes us env variables with the mountpoints
# - [Maybe] Jenkins passes us an env variable with an API key (for hub)
# - Jenkins mounts a .ssh directory (so we can push)
# - We run `make update` to run the update

# Here's a docker command that *ALMOST* works, but fails when it tries to push.
# sudo docker run --rm --name tmp-taas -v ~/.ssh:/.ssh -v ~/cvs/UN/taas:/tmp/taas -v ~/cvs/UN/taas-data:/tmp/taas-data -w /tmp/taas -e 'TAAS_PR_LABEL=dockertest' -e GIT_COMMITTER_NAME=BeepBoop -e 'GIT_COMMITTER_EMAIL=paul@humanitarianresponse.info' -e 'GIT_AUTHOR_NAME=BeepBoop' -e 'GIT_AUTHOR_EMAIL=paul@humanitarianresponse.info' f0c803fd0001 make update
