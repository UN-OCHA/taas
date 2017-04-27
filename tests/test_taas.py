# vim: set fileencoding=utf-8

import json
import os
import sys
import taas
from backports import tempfile
import unittest


class TestTaas(unittest.TestCase):
    test_root = os.path.dirname(__file__)
    test_config = os.path.join(test_root, "config.yml")
    test_config_d = os.path.join(test_root, "config.d")

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
        self.assertEqual(bulbasaur['characteristic']['weight']['kg'], '6.9')
        self.assertEqual(bulbasaur['type'], 'grass')

    def clear_env(self):
        # Clean our environment of variables that may screw our tests

        try:
            del os.environ["TAAS_DATA"]
        except KeyError:
            pass

    def test_read_config(self):
        config = taas.read_config(self.test_config)

        self.assertNotEqual(config['sources'], None)
        self.assertNotEqual(config['sources']['pokedex'], None)

    def test_read_config_d(self):
        config = taas.read_config(self.test_config_d)

        print config

        self.assertEqual(config['food']['vegemite']['type'], 'breakfast spread')
        self.assertEqual(config['food']['durian']['type'], 'fruit')

    def test_taas_data_env(self):
        """
            Tests that we handle the TAAS_DATA environment correctly.
        """

        # Clear env first, just in case
        self.clear_env()

        fake_env = "/tmp/somefakedir"

        data = taas.data_root()
        self.assertNotEqual(data, None)

        os.environ["TAAS_DATA"] = fake_env
        data_env = taas.data_root()

        self.assertNotEqual(data_env, data)
        self.assertEqual(data_env, fake_env)

    def test_data_roots(self):
        """
            Tests our data roots in various ways.
        """

        data_root = taas.data_root()

        self.assertNotEqual(taas.data_root(), None)

        self.assertEqual(taas.sheets_root(), os.path.join(data_root, "sheets"))
        self.assertEqual(taas.json_root(), os.path.join(data_root, "json"))

    def test_split_url(self):

        # Our test data is our countries sheet.
        result = taas.split_url(
            "https://docs.google.com/spreadsheets/d/1NjSI2LaS3SqbgYc0HdD8oIb7lofGtiHgoKKATCpwVdY/edit#gid=1528390745"
        )

        self.assertEqual(result.key, "1NjSI2LaS3SqbgYc0HdD8oIb7lofGtiHgoKKATCpwVdY")
        self.assertEqual(result.gid, "1528390745")

    def test_key_gid_clash(self):

        # Supplying key/gid with URL should give us an error containing our sheet name.
        with self.assertRaises(KeyError) as ex:
            taas.compute_key_gid(
                "MySource", {"key": "foo", "gid": 0, "url": "http://example.com/"}
            )

        self.assertRegexpMatches(ex.exception.message, "MySource")

    def test_fragments(self):
        config = taas.read_config(self.test_config)

        source = 'pokedex'
        version = 'v1'
        version_config = config['sources'][source][version]

        data = taas.process_csv(
            source,
            version_config['mapping'],
            self.test_root
        )

        # TempDirs will clean themselves up after running. <3
        with tempfile.TemporaryDirectory() as tempdir:

            # 'tmpdir/v1'
            version_dir = os.path.join(tempdir, version)

            # 'tmpdir/v1/pokedex'
            fragment_dir = os.path.join(version_dir, source)

            # 'tmpdir/v1/pokedex.json'
            full_json = fragment_dir + ".json"

            # Sanity check: None of our paths exist already
            assert(not os.path.isdir(version_dir))

            # Now process our data
            taas.save_json(source, version, data, tempdir, version_config)

            # And let's read it back in!

            # Test the written data to see if it contains things we expect.
            with open(full_json, 'r') as json_in:
                read_data = json.load(json_in)

                # Bulbasar should be our zeroth record.
                bulbasaur = read_data['data'][0]

                self.assertEqual(bulbasaur['id'], '1')
                self.assertEqual(bulbasaur['name']['en'], 'Bulbasaur')
                self.assertEqual(bulbasaur['name']['jp'], u'フシギソウ')
                self.assertEqual(bulbasaur['characteristic']['weight']['kg'], '6.9')
                self.assertEqual(bulbasaur['type'], 'grass')

            # And let's test a fragment
            charmander_id = '4'

            with open(os.path.join(fragment_dir, charmander_id)) as json_in:
                read_data = json.load(json_in)

                # Our *only* record should now be Charmander

                charmander = read_data['data'][0]

                self.assertEqual(charmander['id'], charmander_id)
                self.assertEqual(charmander['name']['en'], "Charmander")
