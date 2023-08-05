import unittest
from exonote import parse
from exonote.element import Element
from tests import util


EXAMPLE_1 = """\
hello __world__
"""

EXAMPLE_2 = """\
hello __world__!
"""

EXAMPLE_3 = """\
hello ?__world__
"""

EXAMPLE_4 = """\
hello ?__world__?
"""

EXAMPLE_5 = """\
hello __the
world__
"""

EXAMPLE_6 = """\
hello world
"""

EXAMPLE_7 = """\
hello __world __
"""

EXAMPLE_8 = """\
hello __ world__
"""

EXAMPLE_9 = """\
hello __ world __
"""

EXAMPLE_10 = """\
hello __the \\__ world__
"""

EXAMPLE_11 = """\
hello __the\\__ world__
"""

EXAMPLE_12 = """\
hello __the \\__world__
"""

EXAMPLE_13 = """\
hello __the\\__world__
"""

EXAMPLE_14 = """\
hello __the world\\__
"""

EXAMPLE_15 = """\
hello ___the world___
"""

EXAMPLE_16 = """\
hello __\\__the world\\____
"""


class TestUnderlineElement(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_example_1(self):
        structure = parse(EXAMPLE_1)
        data = util.get_data(structure, Element.UNDERLINE)
        self.assertIsNotNone(data)

    def test_example_2(self):
        structure = parse(EXAMPLE_2)
        data = util.get_data(structure, Element.UNDERLINE)
        self.assertIsNotNone(data)

    def test_example_3(self):
        structure = parse(EXAMPLE_3)
        data = util.get_data(structure, Element.UNDERLINE)
        self.assertIsNotNone(data)

    def test_example_4(self):
        structure = parse(EXAMPLE_4)
        data = util.get_data(structure, Element.UNDERLINE)
        self.assertIsNotNone(data)

    def test_example_5(self):
        structure = parse(EXAMPLE_5)
        data = util.get_data(structure, Element.UNDERLINE)
        self.assertIsNotNone(data)

    def test_example_6(self):
        structure = parse(EXAMPLE_6)
        data = util.get_data(structure, Element.UNDERLINE)
        self.assertIsNone(data)

    def test_example_7(self):
        structure = parse(EXAMPLE_7)
        data = util.get_data(structure, Element.UNDERLINE)
        self.assertIsNone(data)

    def test_example_8(self):
        structure = parse(EXAMPLE_8)
        data = util.get_data(structure, Element.UNDERLINE)
        self.assertIsNone(data)

    def test_example_9(self):
        structure = parse(EXAMPLE_9)
        data = util.get_data(structure, Element.UNDERLINE)
        self.assertIsNone(data)
        
    def test_example_10(self):
        structure = parse(EXAMPLE_10)
        data = util.get_data(structure, Element.UNDERLINE)
        self.assertIsNotNone(data)
        self.assertEqual("the __ world", data["text"])

    def test_example_11(self):
        structure = parse(EXAMPLE_11)
        data = util.get_data(structure, Element.UNDERLINE)
        self.assertIsNotNone(data)
        self.assertEqual("the__ world", data["text"])

    def test_example_12(self):
        structure = parse(EXAMPLE_12)
        data = util.get_data(structure, Element.UNDERLINE)
        self.assertIsNotNone(data)
        self.assertEqual("the __world", data["text"])

    def test_example_13(self):
        structure = parse(EXAMPLE_13)
        data = util.get_data(structure, Element.UNDERLINE)
        self.assertIsNotNone(data)
        self.assertEqual("the__world", data["text"])

    def test_example_14(self):
        structure = parse(EXAMPLE_14)
        data = util.get_data(structure, Element.UNDERLINE)
        self.assertIsNone(data)

    def test_example_15(self):
        structure = parse(EXAMPLE_15)
        data = util.get_data(structure, Element.UNDERLINE)
        self.assertIsNotNone(data)
        self.assertEqual("the world", data["text"])

    def test_example_16(self):
        structure = parse(EXAMPLE_16)
        data = util.get_data(structure, Element.UNDERLINE)
        self.assertIsNotNone(data)
        self.assertEqual("__the world_", data["text"])


if __name__ == '__main__':
    unittest.main()
