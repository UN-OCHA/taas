# vim: set fileencoding=utf-8

import os
import sys
import taas
import unittest


class TestCmdline(unittest.TestCase):
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
