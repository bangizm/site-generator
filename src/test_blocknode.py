import unittest
from blocknode import *

class TestBlockNode(unittest.TestCase):
    def test_markdown_to_blocks_basic(self):
        markdown = "This is the first block.\n\nThis is the second block."
        result = markdown_to_blocks(markdown)
        expected = [
            "This is the first block.",
            "This is the second block."
        ]
        self.assertEqual(result, expected)

    def test_markdown_to_blocks_with_empty_blocks(self):
        markdown = "This is the first block.\n\n\n\nThis is the second block.\n\n"
        result = markdown_to_blocks(markdown)
        expected = [
            "This is the first block.",
            "This is the second block."
        ]
        self.assertEqual(result, expected)

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

    def test_block_to_block_type(self):
        from blocknode import block_to_block_type, BlockType

        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("``` \ncode block\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("- List item"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("1. Ordered item"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("This is a normal paragraph."), BlockType.PARAGRAPH)

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