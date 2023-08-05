import unittest
from exonote import parse
from exonote.element import Element
from tests import util


EXAMPLE_1 = """\
## Heading 1
"""

EXAMPLE_2 = """\
## Heading 2 {}
"""

EXAMPLE_3 = """\
    ## Heading 3
"""

EXAMPLE_4 = """\
#### Heading 4 {#my-sid}
"""

EXAMPLE_5 = """\
##### Heading 5 {#my sid}
"""

EXAMPLE_6 = """\
####### Heading 5 {my sid}
"""


class TestHeadingElement(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_example_1(self):
        structure = parse(EXAMPLE_1)
        data = util.get_data(structure, Element.HEADING)
        self.assertIsNotNone(data)

    def test_example_2(self):
        structure = parse(EXAMPLE_2)
        data = util.get_data(structure, Element.HEADING)
        self.assertIsNotNone(data)
        self.assertEqual("Heading 2 {}", data["text"])

    def test_example_3(self):
        structure = parse(EXAMPLE_3)
        data = util.get_data(structure, Element.HEADING)
        self.assertIsNone(data)

    def test_example_4(self):
        structure = parse(EXAMPLE_4)
        data = util.get_data(structure, Element.HEADING)
        self.assertIsNotNone(data)
        self.assertEqual(4, data["level"])
        self.assertEqual("Heading 4", data["text"])
        self.assertEqual("#my-sid", data["id"])

    def test_example_5(self):
        structure = parse(EXAMPLE_5)
        data = util.get_data(structure, Element.HEADING)
        self.assertIsNotNone(data)
        self.assertEqual(5, data["level"])
        self.assertEqual("Heading 5 {#my sid}", data["text"])
        self.assertEqual("#heading_5_{#my_sid}", data["id"])

    def test_example_6(self):
        structure = parse(EXAMPLE_6)
        data = util.get_data(structure, Element.HEADING)
        self.assertIsNone(data)


if __name__ == '__main__':
    unittest.main()
