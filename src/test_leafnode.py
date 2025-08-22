import unittest
from leafnode import *
class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        node1 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node1.to_html(), '<a href="https://www.google.com">Click me!</a>')
        node2 = LeafNode(None,None)
        with self.assertRaises(ValueError):
            node2.to_html()
        node3 = LeafNode(None,"test")
        self.assertEqual(node3.to_html(), "test")
if __name__ == "__main__":
    unittest.main()