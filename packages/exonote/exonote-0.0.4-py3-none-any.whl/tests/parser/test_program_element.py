import unittest
from exonote import parse
from exonote.element import Element
from tests import util


EXAMPLE_1 = """\
this is a $[title](location)
"""

EXAMPLE_2 = """\
this is a $[](location)
"""

EXAMPLE_3 = """\
this is a $[title]()
"""

EXAMPLE_4 = """\
this is a $[]()
"""

EXAMPLE_5 = """\
this is a "$[title](location)"
"""

EXAMPLE_6 = """\
this is a $[title][location]
"""

EXAMPLE_7 = """\
this is a $[][location]
"""

EXAMPLE_8 = """\
this is a $[title][]
"""

EXAMPLE_9 = """\
this is a $[][]
"""

EXAMPLE_10 = """\
this is a "$[title][location]"
"""


class TestProgramElement(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_example_1(self):
        structure = parse(EXAMPLE_1)
        data = util.get_data(structure, Element.PROGRAM)
        self.assertIsNotNone(data)

    def test_example_2(self):
        structure = parse(EXAMPLE_2)
        data = util.get_data(structure, Element.PROGRAM)
        self.assertIsNotNone(data)

    def test_example_3(self):
        structure = parse(EXAMPLE_3)
        data = util.get_data(structure, Element.PROGRAM)
        self.assertIsNone(data)

    def test_example_4(self):
        structure = parse(EXAMPLE_4)
        data = util.get_data(structure, Element.PROGRAM)
        self.assertIsNone(data)

    def test_example_5(self):
        structure = parse(EXAMPLE_5)
        data = util.get_data(structure, Element.PROGRAM)
        self.assertIsNotNone(data)

    def test_example_6(self):
        structure = parse(EXAMPLE_6)
        data = util.get_data(structure, Element.PROGRAM)
        self.assertIsNotNone(data)

    def test_example_7(self):
        structure = parse(EXAMPLE_7)
        data = util.get_data(structure, Element.PROGRAM)
        self.assertIsNotNone(data)

    def test_example_8(self):
        structure = parse(EXAMPLE_8)
        data = util.get_data(structure, Element.PROGRAM)
        self.assertIsNone(data)

    def test_example_9(self):
        structure = parse(EXAMPLE_9)
        data = util.get_data(structure, Element.PROGRAM)
        self.assertIsNone(data)

    def test_example_10(self):
        structure = parse(EXAMPLE_10)
        data = util.get_data(structure, Element.PROGRAM)
        self.assertIsNotNone(data)


if __name__ == '__main__':
    unittest.main()
