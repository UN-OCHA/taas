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

The harder way:

    $ virtualenv venv
    $ . venv/bin/activate
    $ pip install --upgrade .
    $ pip install -r requirements.txt

# Running the code:

Activate the virtual environment:

    $ . env/bin/activate

Then run scripts from the `bin` directory:

    $ bin/fetch.py

## Contributing

Please run `pip freeze > requirements.txt` when making code changes, so we get any updated
library requirements along with your code.
