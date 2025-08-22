import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a text node", TextType.BOLD, "test")
        node4 = TextNode("This is a text node", TextType.LINK)
        node5 = TextNode("This is a text nod5", TextType.BOLD)
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node, node4)
        self.assertNotEqual(node, node5)
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_type_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")

    def test_text_type_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")

    def test_text_type_code(self):
        node = TextNode("print('hi')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hi')")

    def test_text_type_link(self):
        node = TextNode("Click here", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_text_type_image(self):
        node = TextNode("Alt text", TextType.IMAGE, url="https://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {
            "src": "https://example.com/image.png",
            "alt": "Alt text"
        })
    def test_single_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_code_blocks(self):
        node = TextNode("Here is `one` and here is `two`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Here is ", TextType.TEXT),
            TextNode("one", TextType.CODE),
            TextNode(" and here is ", TextType.TEXT),
            TextNode("two", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)

    def test_no_delimiters_returns_same_text(self):
        node = TextNode("Plain text only", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("Plain text only", TextType.TEXT)])

    def test_non_text_nodes_pass_through(self):
        node1 = TextNode("Already bold", TextType.BOLD)
        node2 = TextNode("This is `code` here", TextType.TEXT)
        result = split_nodes_delimiter([node1, node2], "`", TextType.CODE)
        self.assertEqual(result[0], node1)
        self.assertEqual(result[1].text, "This is ")
        self.assertEqual(result[2].text, "code")
        self.assertEqual(result[3].text, " here")

    def test_unclosed_delimiter_raises(self):
        node = TextNode("This is `unfinished code block", TextType.TEXT)
        with self.assertRaises(Exception) as cm:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(str(cm.exception), "No closing delimiter found")
    def test_text_starts_with_delimiter(self):
        node = TextNode("`code at start` then text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("code at start", TextType.CODE),
            TextNode(" then text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)
    def test_split_links_basic(self):
        node = TextNode(
            "This is text with a [link](https://example.com) and another [second link](https://second.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second link", TextType.LINK, "https://second.com"),
        ]
        self.assertListEqual(expected, new_nodes)
    def test_link_at_start(self):
        node = TextNode("[start link](https://start.com) and some text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("start link", TextType.LINK, "https://start.com"),
            TextNode(" and some text", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_link_at_end(self):
        node = TextNode("Some text and an [end link](https://end.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Some text and an ", TextType.TEXT),
            TextNode("end link", TextType.LINK, "https://end.com"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_multiple_adjacent_links(self):
        node = TextNode(
            "Links: [one](https://one.com)[two](https://two.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Links: ", TextType.TEXT),
            TextNode("one", TextType.LINK, "https://one.com"),
            TextNode("two", TextType.LINK, "https://two.com"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_text_to_textnodes_full_case(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` "
            "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
            "and a [link](https://boot.dev)"
        )
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(expected, nodes)
