# UN-OCHA Taxonomy As A Service

[![Build Status](https://travis-ci.org/UN-OCHA/taas.svg?branch=master)](https://travis-ci.org/UN-OCHA/taas)
[![Coverage Status](https://coveralls.io/repos/github/UN-OCHA/taas/badge.svg?branch=master)](https://coveralls.io/github/UN-OCHA/taas)
[![Code Climate](https://lima.codeclimate.com/github/UN-OCHA/taas/badges/gpa.svg)](https://lima.codeclimate.com/github/UN-OCHA/taas)
[![Issue Count](https://lima.codeclimate.com/github/UN-OCHA/taas/badges/issue_count.svg)](https://lima.codeclimate.com/github/UN-OCHA/taas)

This code that powers the UN Office for the Coordination of Humanitarian Affairs (UN-OCHA)
Taxnonomy as a Service APIs.

## Building the code

The easy way:

    $ make

# Running the code:

Activate the virtual environment:

    $ . env/bin/activate

Fetch updates with `fetch`. Make sure you have the `UN-OCHA/taas-data` directory checked
out the same level as `taas`, or set your `TAAS_DATA` environment variable first.

    $ fetch

Create a pull-request using `update.py`:

    $ bin/update.py

## Contributing

Please run `make freeze` when making code changes with new libraries, so we get any updated
library requirements along with your code.
