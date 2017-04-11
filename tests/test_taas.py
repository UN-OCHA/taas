# vim: set fileencoding=utf-8

import os
import sys
import taas
import unittest


class TestTaas(unittest.TestCase):
    test_root = os.path.dirname(__file__)
    test_config = os.path.join(test_root, "config.yml")

    def test_process_csv(self):
        config = taas.read_config(self.test_config)

        result = taas.process_csv(
            'pokedex',
            config['sources']['pokedex']['v1']['mapping'],
            self.test_root
        )

        bulbasaur = result['data'][0]

        # Test all our fields exist, sub-maps are in place, and
        # we can handle unicode okay.
        self.assertEqual(bulbasaur['id'], '1')
        self.assertEqual(bulbasaur['name']['en'], 'Bulbasaur')
        self.assertEqual(bulbasaur['name']['jp'], 'フシギソウ')
        self.assertEqual(bulbasaur['type'], 'grass')

    def clear_env(self):
        # Clean our environment of variables that may screw our tests

        try:
            del os.environ["TAAS_DATA"]
        except KeyError:
            pass

    def test_read_config(self):
        config = taas.read_config(self.test_config)

        assert config['sources'] is not None
        assert config['sources']['pokedex'] is not None

    def test_taas_data_env(self):
        """
            Tests that we handle the TAAS_DATA environment correctly.
        """

        # Clear env first, just in case
        self.clear_env()

        fake_env = "/tmp/somefakedir"

        data = taas.data_root()
        assert data is not None

        os.environ["TAAS_DATA"] = fake_env
        data_env = taas.data_root()

        assert data_env != data
        assert data_env == fake_env

    def test_data_roots(self):
        """
            Tests our data roots in various ways.
        """

        data_root = taas.data_root()

        assert taas.data_root() is not None

        assert taas.sheets_root() == os.path.join(data_root, "sheets")
        assert taas.json_root() == os.path.join(data_root, "json")
