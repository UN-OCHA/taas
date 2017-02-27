# UN-OCHA Taxonomy As A Service

This code that powers the UN Office for the Coordination of Humanitarian Affairs (UN-OCHA)
Taxnonomy as a Service APIs.

## Running this code

First, set up your virtual environment and install the requirements:

    $ virtualenv venv
    $ . venv/bin/activate
    $ pip install --upgrade .
    $ pip install -r requirements.txt

To run, simply:

    $ . env/bin/activate
    $ python bin/somescript.py

## Contributing

Please run `pip freeze > requirements.txt` when making code changes, so we get any updated
library requirements along with your code.
