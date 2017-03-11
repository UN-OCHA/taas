import os
import sys
import taas

test_root   = os.path.dirname(__file__)
test_config = os.path.join( test_root, "config.yml" )

def clear_env():
    # Clean our environment of variables that may screw our tests

    try:
        del os.environ["TAAS_DATA"]
    except KeyError: pass

def test_read_config():
    config = taas.read_config(test_config)

    assert config['sources'] is not None
    assert config['sources']['bad_key'] is not None

def test_taas_data_env():
    """
        Tests that we handle the TAAS_DATA environment correctly.
    """

    # Clear env first, just in case
    clear_env()

    fake_env = "/tmp/somefakedir"

    data = taas.data_root()
    assert data is not None

    os.environ["TAAS_DATA"] = fake_env
    data_env = taas.data_root()

    assert data_env != data
    assert data_env == fake_env

def test_data_roots():
    """
        Tests our data roots in various ways.
    """

    data_root = taas.data_root()

    assert taas.data_root() is not None

    assert taas.sheets_root() == os.path.join(data_root,"sheets")
    assert taas.json_root()   == os.path.join(data_root,"json")
