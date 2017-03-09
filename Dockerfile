FROM unocha/alpine-base-s6-python2:latest

MAINTAINER Paul Fenwick "paul@humanitarianresponse.info"

# Git is everyone's favourite source control manager
# Hub actually lets us make PRs to github
# openssh is the transport needed to make PRs to github
RUN apk add --update --no-cache git hub openssh

# What we expect now:
# - Jenkins checks out taas and taas-data and mounts them
# - Jenkins passes us env variables with the mountpoints
# - Jenkins passes us an env variable with an API key (for hub)
# - Jenkins mounts a .ssh directory (so we can push)
# - We run `make update` to run the update
