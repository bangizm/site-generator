import unittest
from textnode import TextNode, TextType, split_nodes_delimiter

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node, node2)

        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(node, node2)

        node = TextNode("This is a text node", TextType.CODE)
        node2 = TextNode("This is a text node", TextType.CODE)
        self.assertEqual(node, node2)
        
        node = TextNode("This is a text node", TextType.LINK)
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertEqual(node, node2)

        node = TextNode("This is a text node", TextType.IMAGE)
        node2 = TextNode("This is a text node", TextType.IMAGE)
        self.assertEqual(node, node2)

    def test_noteq(self):
        #TextType", ["TEXT", "BOLD", "ITALIC", "CODE", "LINK", "IMAGE"]
        node = TextNode("This is a text node", TextType.LINK)
        node2 = TextNode("This is a text node", TextType.LINK, "localhost:8080")
        self.assertNotEqual(node, node2)
    
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a different text node", TextType.TEXT)
        self.assertNotEqual(node, node2)
    
        node = TextNode("This is a text node", TextType.LINK)
        node2 = TextNode("This is a text node", TextType.IMAGE)
        self.assertNotEqual(node, node2)
    
class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter_basic(self):
        nodes = [TextNode("This is **bold** text", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_no_split(self):
        nodes = [TextNode("This is normal text", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [TextNode("This is normal text", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_invalid_syntax(self):
        nodes = [TextNode("This is **bold text", TextType.TEXT)]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(nodes, "**", TextType.BOLD)

class TextExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images_basic(self):
        from textnode import extract_markdown_images
        text = "Here is an image: ![alt text](http://example.com/image.png)"
        result = extract_markdown_images(text)
        expected = [("alt text", "http://example.com/image.png")]
        self.assertEqual(result, expected)

    def test_extract_markdown_images_multiple(self):
        from textnode import extract_markdown_images
        text = "Image one: ![img1](http://example.com/img1.png) and Image two: ![img2](http://example.com/img2.png)"
        result = extract_markdown_images(text)
        expected = [("img1", "http://example.com/img1.png"), ("img2", "http://example.com/img2.png")]
        self.assertEqual(result, expected)

    def test_extract_markdown_images_none(self):
        from textnode import extract_markdown_images
        text = "This text has no images."
        result = extract_markdown_images(text)
        expected = []
        self.assertEqual(result, expected)

class TextExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links_basic(self):
        from textnode import extract_markdown_links
        text = "Here is a link: [Google](http://google.com)"
        result = extract_markdown_links(text)
        expected = [("Google", "http://google.com")]
        self.assertEqual(result, expected)

    def test_extract_markdown_links_multiple(self):
        from textnode import extract_markdown_links
        text = "Link one: [Example1](http://example1.com) and Link two: [Example2](http://example2.com)"
        result = extract_markdown_links(text)
        expected = [("Example1", "http://example1.com"), ("Example2", "http://example2.com")]
        self.assertEqual(result, expected)

    def test_extract_markdown_links_none(self):
        from textnode import extract_markdown_links
        text = "This text has no links."
        result = extract_markdown_links(text)
        expected = []
        self.assertEqual(result, expected)


    
if __name__ == "__main__":
    unittest.main()

