from taas.mapping import Literal, Map, Concat
import unittest


class TestMapping(unittest.TestCase):

    row = {
        "id": "3",
        "foo": "bar",
        "baz": "bazza"
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

    # TODO: Test *optional* maps.

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
