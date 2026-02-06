import unittest
from main import *

class TestMainFunctions(unittest.TestCase):

    def test_extract_title_with_h1(self):
        markdown1 = "# My Title\nSome other content."
        title = extract_title(markdown1)
        self.assertEqual(title, "My Title")

        markdown2 = " #  My Title  \nWith extra whitespace. "
        title = extract_title(markdown2)
        self.assertEqual(title, "My Title")

    def test_extract_title_without_h1(self):
        markdown1 = "## Subtitle\nSome other content."
        with self.assertRaises(Exception) as context1:
            extract_title(markdown1)
        self.assertTrue("No h1 header found" in str(context1.exception))

        markdown2 = " Some # of text not a title.\nAnd other text."
        with self.assertRaises(Exception) as context2:
            extract_title(markdown2)
        self.assertTrue("No h1 header found" in str(context2.exception))

    def test_generate_page(self):
        from tempfile import NamedTemporaryFile
        import os

        markdown_content = "# Test Title\n\nThis is a test paragraph."
        template_content = "<html><head><title>{{title}}</title></head><body>{{content}}</body></html>"

        with NamedTemporaryFile('w+', delete=False) as md_file, \
             NamedTemporaryFile('w+', delete=False) as template_file, \
             NamedTemporaryFile('r+', delete=False) as output_file:
            pass