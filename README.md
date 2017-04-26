# UN-OCHA Taxonomy As A Service

[![Build Status](https://travis-ci.org/UN-OCHA/taas.svg?branch=master)](https://travis-ci.org/UN-OCHA/taas)
[![Coverage Status](https://coveralls.io/repos/github/UN-OCHA/taas/badge.svg?branch=master)](https://coveralls.io/github/UN-OCHA/taas)
[![Code Climate](https://lima.codeclimate.com/github/UN-OCHA/taas/badges/gpa.svg)](https://lima.codeclimate.com/github/UN-OCHA/taas)
[![Issue Count](https://lima.codeclimate.com/github/UN-OCHA/taas/badges/issue_count.svg)](https://lima.codeclimate.com/github/UN-OCHA/taas)
[![Image Version](https://images.microbadger.com/badges/version/unocha/taas.svg)](https://microbadger.com/images/unocha/taas)
[![Image Layers](https://images.microbadger.com/badges/image/unocha/taas.svg)](https://microbadger.com/images/unocha/taas)

This code that powers the UN Office for the Coordination of Humanitarian Affairs (UN-OCHA)
Taxnonomy as a Service APIs.

## Requirements

* pip: `sudo easy_install pip`

* virtualenv: `pip install virtualenv`

## Building the code

The easy way:

    $ make

# Running the code:

Activate the virtual environment:

    $ . venv/bin/activate

Fetch updates with `gss2json`. Make sure you have the `UN-OCHA/taas-data` directory checked
out the same level as `taas`, or set your `TAAS_DATA` environment variable first.

    $ gss2json

Create a pull-request by adding the `--pull` switch:

    $ gss2json --pull

Call with `--help` for more details:

    $ gss2json --help

## Contributing

Please run `make freeze` when making code changes with new libraries, so we get any updated
library requirements along with your code.

## Running from Docker

If you really want to...

```
$ git checkout UN-OCHA/taas
$ git checkout UN-OCHA/taas-data
$ cd taas
$ make docker tag VERSION=1
$ docker run                                                \
    --rm --name tmp-taas                                    \
    -v ~/.config/hub:/root/.config/hub                      \
    -v ~/.ssh:/root/.ssh                                    \
    -v ~/taas:/tmp/taas                                     \
    -v ~/taas-data:/tmp/taas-data                           \
    -w /tmp/taas                                            \
    -e 'TAAS_PR_LABEL=dockertest'                           \
    -e 'GIT_COMMITTER_NAME=BeepBoop'                        \
    -e 'GIT_COMMITTER_EMAIL=paul@humanitarianresponse.info' \
    -e 'GIT_AUTHOR_NAME=BeepBoop'                           \
    -e 'GIT_AUTHOR_EMAIL=paul@humanitarianresponse.info'    \
    unocha/taas:1 make update
```

Things to note:

- You must have run [hub](https://github.com/github/hub) at least once to generate your `~/.config/hub` token.
- I'm a docker n00b, so there's almost certainly a better way to do all of the above. Patches welcome!
