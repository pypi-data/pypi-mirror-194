import unittest
from exonote import parse
from exonote.element import Element
from tests import util


EXAMPLE_1 = """\
hello !world!
"""

EXAMPLE_2 = """\
hello !world!!
"""

EXAMPLE_3 = """\
hello ?!world!
"""

EXAMPLE_4 = """\
hello ?!world!?
"""

EXAMPLE_5 = """\
hello !the
world!
"""

EXAMPLE_6 = """\
hello world
"""

EXAMPLE_7 = """\
hello !world !
"""

EXAMPLE_8 = """\
hello ! world!
"""

EXAMPLE_9 = """\
hello ! world !
"""

EXAMPLE_10 = """\
hello !the \\! world!
"""

EXAMPLE_11 = """\
hello !the\\! world!
"""

EXAMPLE_12 = """\
hello !the \\!world!
"""

EXAMPLE_13 = """\
hello !the\\!world!
"""

EXAMPLE_14 = """\
hello !the world\\!
"""

EXAMPLE_15 = """\
hello !!the world!!
"""

EXAMPLE_16 = """\
hello !\\!the world\\!!
"""


class TestNoticeElement(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_example_1(self):
        structure = parse(EXAMPLE_1)
        data = util.get_data(structure, Element.NOTICE)
        self.assertIsNotNone(data)

    def test_example_2(self):
        structure = parse(EXAMPLE_2)
        data = util.get_data(structure, Element.NOTICE)
        self.assertIsNotNone(data)

    def test_example_3(self):
        structure = parse(EXAMPLE_3)
        data = util.get_data(structure, Element.NOTICE)
        self.assertIsNotNone(data)

    def test_example_4(self):
        structure = parse(EXAMPLE_4)
        data = util.get_data(structure, Element.NOTICE)
        self.assertIsNotNone(data)

    def test_example_5(self):
        structure = parse(EXAMPLE_5)
        data = util.get_data(structure, Element.NOTICE)
        self.assertIsNotNone(data)

    def test_example_6(self):
        structure = parse(EXAMPLE_6)
        data = util.get_data(structure, Element.NOTICE)
        self.assertIsNone(data)

    def test_example_7(self):
        structure = parse(EXAMPLE_7)
        data = util.get_data(structure, Element.NOTICE)
        self.assertIsNone(data)

    def test_example_8(self):
        structure = parse(EXAMPLE_8)
        data = util.get_data(structure, Element.NOTICE)
        self.assertIsNone(data)

    def test_example_9(self):
        structure = parse(EXAMPLE_9)
        data = util.get_data(structure, Element.NOTICE)
        self.assertIsNone(data)
        
    def test_example_10(self):
        structure = parse(EXAMPLE_10)
        data = util.get_data(structure, Element.NOTICE)
        self.assertIsNotNone(data)
        self.assertEqual("the ! world", data["text"])

    def test_example_11(self):
        structure = parse(EXAMPLE_11)
        data = util.get_data(structure, Element.NOTICE)
        self.assertIsNotNone(data)
        self.assertEqual("the! world", data["text"])

    def test_example_12(self):
        structure = parse(EXAMPLE_12)
        data = util.get_data(structure, Element.NOTICE)
        self.assertIsNotNone(data)
        self.assertEqual("the !world", data["text"])

    def test_example_13(self):
        structure = parse(EXAMPLE_13)
        data = util.get_data(structure, Element.NOTICE)
        self.assertIsNotNone(data)
        self.assertEqual("the!world", data["text"])

    def test_example_14(self):
        structure = parse(EXAMPLE_14)
        data = util.get_data(structure, Element.NOTICE)
        self.assertIsNone(data)

    def test_example_15(self):
        structure = parse(EXAMPLE_15)
        data = util.get_data(structure, Element.NOTICE)
        self.assertIsNone(data)
        # The Warning element eats the double "!!"
        # that's why the next two lines are commented out.
        # self.assertIsNotNone(data)
        # self.assertEqual("the world", data["text"])

    def test_example_16(self):
        structure = parse(EXAMPLE_16)
        data = util.get_data(structure, Element.NOTICE)
        self.assertIsNotNone(data)
        self.assertEqual("!the world!", data["text"])


if __name__ == '__main__':
    unittest.main()
