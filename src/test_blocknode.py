import unittest
from blocknode import markdown_to_blocks

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