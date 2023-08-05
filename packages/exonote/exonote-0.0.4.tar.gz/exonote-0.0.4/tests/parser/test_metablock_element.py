import unittest
from exonote import parse
from exonote.element import Element
from tests import util


EXAMPLE_1 = """\
%%%
this is a code
block
%%%
"""

EXAMPLE_2 = """\
%%%title
this is a code
block with a
title
%%%
"""

EXAMPLE_3 = """\
%%%my title
this is a code
block with an
invalid
title
%%%
"""

EXAMPLE_4 = """\


%%%title
this is a code
block with a
title
%%%


"""


class TestMetablockElement(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_example_1(self):
        structure = parse(EXAMPLE_1)
        data = util.get_data(structure, Element.METABLOCK)
        self.assertIsNotNone(data)
        self.assertEqual("", data["title"])

    def test_example_2(self):
        structure = parse(EXAMPLE_2)
        data = util.get_data(structure, Element.METABLOCK)
        self.assertIsNotNone(data)
        self.assertEqual("title", data["title"])

    def test_example_3(self):
        structure = parse(EXAMPLE_3)
        data = util.get_data(structure, Element.METABLOCK)
        self.assertIsNone(data)

    def test_example_4(self):
        structure = parse(EXAMPLE_4)
        data = util.get_data(structure, Element.METABLOCK)
        self.assertIsNotNone(data)
        data = util.get_data(structure, Element.STRING)
        self.assertIsNone(data)


if __name__ == '__main__':
    unittest.main()
