FROM unocha/alpine-base-s6-python2:latest

MAINTAINER Paul Fenwick "paul@humanitarianresponse.info"

# Git is everyone's favourite source control manager
# Hub actually lets us make PRs to github
# openssh is the transport needed to make PRs to github
RUN apk add --update --no-cache git hub openssh

# Copy over our app
COPY . /app
WORKDIR /app

# Make sure we're up to date
RUN git pull

# Build everything ready to go
RUN make

