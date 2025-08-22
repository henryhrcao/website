import unittest

from blocks import *
class TestTextNode(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    def test_paragraph(self):
        block = "This is a simple paragraph of text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_levels(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
        # Not a heading if more than 6 hashes
        self.assertEqual(block_to_block_type("####### Not heading"), BlockType.PARAGRAPH)
        # Not a heading if no space after hash
        self.assertEqual(block_to_block_type("##Not heading"), BlockType.PARAGRAPH)

    def test_code_block(self):
        block = "```\nprint('Hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        # Missing closing backticks means paragraph
        block = "```\nprint('oops')"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_quote_block(self):
        block = "> This is a quote\n> still part of quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        # Mixed line without ">" breaks it into paragraph
        block = "> First line\nNot quoted"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_block(self):
        block = "- item one\n- item two\n- item three"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED)
        # Missing space after "-" is not valid list
        self.assertEqual(block_to_block_type("-item wrong"), BlockType.PARAGRAPH)

    def test_ordered_list_block(self):
        block = "1. first\n2. second\n3. third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED)
        # Wrong numbering breaks it
        block = "1. first\n3. second"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        # Missing space after number-dot
        block = "1.first"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    def test_paragraphs(self):
        md = """
            This is **bolded** paragraph
            text in a p
            tag here

            This is another paragraph with _italic_ text and `code` here

            """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
    def test_headings(self):
        md = """
        # Heading 1

        ## Heading 2

        ### Heading 3
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3></div>",
        )
    def test_codeblock(self):
        md = """
        ```
        This is text that _should_ remain
        the **same** even with inline stuff
        ```
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    def test_quote_block(self):
        md = """
> This is a quote
> spanning multiple lines
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote spanning multiple lines</blockquote></div>",
        )
    def test_unordered_list(self):
        md = """
- item one
- item two
- item three
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>item one</li><li>item two</li><li>item three</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. first item
2. second item
3. third item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>first item</li><li>second item</li><li>third item</li></ol></div>",
        )

    if __name__ == "__main__":
        unittest.main()

