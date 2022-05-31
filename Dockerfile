FROM public.ecr.aws/unocha/python3-base-s6:3.9

MAINTAINER Paul Fenwick "paul@humanitarianresponse.info"

ARG VERSION
ARG VCS_URL
ARG VCS_REF
ARG BUILD_DATE

LABEL org.label-schema.schema-version="1.0" \
      org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.vendor="UN-OCHA" \
      org.label-schema.version=$VERSION \
      org.label-schema.name="taas" \
      org.label-schema.description="This container provides a python environment for Taxonomy as a Service." \
      org.label-schema.vcs-url=$VCS_URL \
      org.label-schema.vcs-ref=$VCS_REF

# openssh is the transport needed to make PRs to github
RUN apk add --update --no-cache \
      git openssh \
      make \
      py-virtualenv \
      # These are needed so python can build its things.
      gcc \
      python3-dev \
      musl-dev \
      linux-headers \
      libffi-dev \
      openssl-dev

WORKDIR /tmp/taas
CMD make update
