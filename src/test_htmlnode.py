import unittest
from htmlnode import *
class TestTextNode(unittest.TestCase):
    def testProps(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(),"")
        node1 = HTMLNode(props={
            "href": "https://www.google.com",
            "target": "_blank",
            }
        )
        self.assertEqual(node1.props_to_html(), ' href="https://www.google.com" target="_blank"')

if __name__ == "__main__":
    unittest.main()