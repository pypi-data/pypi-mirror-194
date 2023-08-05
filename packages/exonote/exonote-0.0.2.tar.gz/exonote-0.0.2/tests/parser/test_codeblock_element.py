import unittest
from exonote import parse
from exonote.element import Element
from tests import util


EXAMPLE_1 = """\
```
this is a code
block
```
"""

EXAMPLE_2 = """\
```title
this is a code
block with a
title
```
"""

EXAMPLE_3 = """\
```my title
this is a code
block with an
invalid
title
```
"""


class TestCodeblockElement(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_example_1(self):
        structure = parse(EXAMPLE_1)
        data = util.get_data(structure, Element.CODEBLOCK)
        self.assertIsNotNone(data)
        self.assertEqual("", data["title"])

    def test_example_2(self):
        structure = parse(EXAMPLE_2)
        data = util.get_data(structure, Element.CODEBLOCK)
        self.assertIsNotNone(data)
        self.assertEqual("title", data["title"])

    def test_example_3(self):
        structure = parse(EXAMPLE_3)
        data = util.get_data(structure, Element.CODEBLOCK)
        self.assertIsNone(data)


if __name__ == '__main__':
    unittest.main()
