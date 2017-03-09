import os
import sys
import taas

test_root   = os.path.dirname(__file__)
test_config = os.path.join( test_root, "config.yml" )

# TODO: Write a lot more tests!

def test_read_config():
    config = taas.read_config(test_config)

    assert config['sources'] is not None
    assert config['sources']['bad_key'] is not None

def test_taas_data_env():
    """
        Tests that we handle the TAAS_DATA environment correctly.
    """

    # Clear env first, just in case
    try:
        del os.environ["TAAS_DATA"]
    except KeyError: pass

    fake_env = "/tmp/somefakedir"

    sheets = taas.sheets_root()
    assert sheets is not None

    os.environ["TAAS_DATA"] = fake_env
    sheets_env = taas.sheets_root()

    assert sheets_env != sheets
    assert sheets_env == fake_env
