import unittest
from parentnode import *
from leafnode import *
class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_to_html_with_multiple_children(self):
        child1 = LeafNode("span", "first")
        child2 = LeafNode("b", "second")
        parent = ParentNode("div", [child1, child2])
        self.assertEqual(
            parent.to_html(),
            "<div><span>first</span><b>second</b></div>"
        )

    def test_to_html_with_props(self):
        child = LeafNode("span", "content")
        parent = ParentNode("div", [child], props={"class": "container", "id": "main"})
        # Order of props may vary; check using 'in' for each
        html = parent.to_html()
        self.assertTrue(html.startswith("<div"))
        self.assertIn('class="container"', html)
        self.assertIn('id="main"', html)
        self.assertTrue(html.endswith("</div>"))

    def test_to_html_no_children_raises(self):
        with self.assertRaises(ValueError) as cm:
            ParentNode("div", []).to_html()
        self.assertEqual(str(cm.exception), "No Children")

    def test_to_html_no_tag_raises(self):
        child = LeafNode("span", "content")
        with self.assertRaises(ValueError) as cm:
            ParentNode(None, [child]).to_html()
        self.assertEqual(str(cm.exception), "No value")

    def test_nested_parent_with_props(self):
        grandchild = LeafNode("em", "deep")
        child = ParentNode("span", [grandchild], props={"style": "color:red;"})
        parent = ParentNode("div", [child], props={"class": "outer"})
        html = parent.to_html()
        self.assertIn('<div class="outer">', html)
        self.assertIn('<span style="color:red;">', html)
        self.assertIn("<em>deep</em>", html)

if __name__ == "__main__":
    unittest.main()