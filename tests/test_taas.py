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
