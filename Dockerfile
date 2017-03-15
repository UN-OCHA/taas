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
