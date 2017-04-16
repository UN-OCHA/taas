from taas.mapping import Literal, Map, Concat, Link, make_map
import unittest


class TestMapping(unittest.TestCase):

    row = {
        "id": "3",
        "foo": "bar",
        "baz": "bazza",
        "link": "42 - Some other endpoint"
    }

    def test_literal(self):

        mystr = "foo"

        lit = Literal({"value": mystr})

        value = lit.emit(self.row)

        self.assertEqual(value, mystr)

    def test_map(self):
        mymap = Map({"field": "foo"})

        self.assertEqual(
            mymap.emit(self.row),
            "bar"
        )

        self.assertEqual(
            mymap.emit({"foo": "baz"}),
            "baz"
        )

    def test_map_strip(self):
        mymap = Map({"field": "foo"})

        # Fields should trim spaces by default
        self.assertEqual(
            mymap.emit({"foo": " data "}),
            "data"
        )

        # If we set trim to false, we should get back unchanged data
        notrim_map = Map({"field": "foo", "trim": False})

        self.assertEqual(
            notrim_map.emit({"foo": " data "}),
            " data "
        )

    def test_map_optional(self):
        mymap = Map({"field": "foo", "optional": True})

        self.assertEqual(mymap.emit({"foo": ""}), None)
        self.assertEqual(mymap.emit({"foo": "bar"}), "bar")

        strictmap = Map({"field": "foo"})

        # Make sure we get a ValueError if we're missing data
        # on a required field.
        with self.assertRaises(ValueError):
            strictmap.emit({"foo": ""})

        # Make sure we get a KeyError if we're missing the column
        # entirely.
        with self.assertRaises(KeyError):
            strictmap.emit({"oof": "Not the field you're looking for."})

    def test_map_extended(self):
        """Tests the extended map sequence, which takes multiple fields"""
        mymap = Map({"field": ["foo", "bar"]})

        self.assertEqual(mymap.emit({"foo": "Foo", "bar": "Bar"}), "Foo")
        self.assertEqual(mymap.emit({"foo": "", "bar": "Bar"}), "Bar")

        with self.assertRaises(ValueError):
            mymap.emit({"foo": "", "bar": ""})

    def test_concat(self):
        concat = Concat({
            "field": "id",
            "prefix": "https://example.com/",
            "postfix": "/self"
        })

        self.assertEqual(
            concat.emit(self.row),
            "https://example.com/3/self"
        )

    def test_concat_optional(self):
        concat = Concat({
            "field": "id",
            "prefix": "https://example.com/",
            "optional": True
        })

        self.assertEqual(
            concat.emit({"id": ""}),
            None
        )

    def test_link(self):
        link = Link({
            "field": "link",
            "prefix": "https://example.com/"
        })

        self.assertEqual(
            link.emit(self.row),
            "https://example.com/42"
        )

    def test_make_map(self):
        """
        Tests that the `make_map` function is able to correctly return each of
        our mapping classes.
        """

        # TODO: This should be a reusable chunk of data we can put somewhere.
        mapping = {

            # Foo uses the default settings (map)
            "foo": "bar",

            # Baz is the same, but explicit
            "baz": {
                "type": "map",
                "field": "bar"
            },

            # Bazza is the same, type: map is assumed.
            "bazza": {
                "field": "bar"
            },

            "lit": {
                "type": "literal",
                "value": "MyLiteralString"
            },
            "con": {
                "type": "concat",
                "field": "somefield",
                "prefix": "lol"
            }
        }

        made_map = make_map(mapping)

        assert(isinstance(made_map["foo"], Map))
        assert(isinstance(made_map["baz"], Map))
        assert(isinstance(made_map["bazza"], Map))
        assert(isinstance(made_map["lit"], Literal))
        assert(isinstance(made_map["con"], Concat))
