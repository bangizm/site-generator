import unittest
from textnode import (
    TextNode,
    TextType,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    extract_markdown_images,
    extract_markdown_links,
)

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
        text = "Here is an image: ![alt text](http://example.com/image.png)"
        result = extract_markdown_images(text)
        expected = [("alt text", "http://example.com/image.png")]
        self.assertEqual(result, expected)

    def test_extract_markdown_images_multiple(self):
        text = "Image one: ![img1](http://example.com/img1.png) and Image two: ![img2](http://example.com/img2.png)"
        result = extract_markdown_images(text)
        expected = [("img1", "http://example.com/img1.png"), ("img2", "http://example.com/img2.png")]
        self.assertEqual(result, expected)

    def test_extract_markdown_images_none(self):
        text = "This text has no images."
        result = extract_markdown_images(text)
        expected = []
        self.assertEqual(result, expected)

class TextExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links_basic(self):
        text = "Here is a link: [Google](http://google.com)"
        result = extract_markdown_links(text)
        expected = [("Google", "http://google.com")]
        self.assertEqual(result, expected)

    def test_extract_markdown_links_multiple(self):
        text = "Link one: [Example1](http://example1.com) and Link two: [Example2](http://example2.com)"
        result = extract_markdown_links(text)
        expected = [("Example1", "http://example1.com"), ("Example2", "http://example2.com")]
        self.assertEqual(result, expected)

    def test_extract_markdown_links_none(self):
        text = "This text has no links."
        result = extract_markdown_links(text)
        expected = []
        self.assertEqual(result, expected)

class TestSplitNodesImage(unittest.TestCase):
    def test_split_nodes_image_basic(self):
        nodes = [TextNode("Here is an image: ![alt text](http://example.com/image.png)", TextType.TEXT)]
        result = split_nodes_image(nodes)
        expected = [
            TextNode("Here is an image: ", TextType.TEXT),
            TextNode("alt text", TextType.IMAGE, "http://example.com/image.png")
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_image_multiple(self):
        nodes = [TextNode("Image one: ![img1](http://example.com/img1.png) and Image two: ![img2](http://example.com/img2.png)", TextType.TEXT)]
        result = split_nodes_image(nodes)
        expected = [
            TextNode("Image one: ", TextType.TEXT),
            TextNode("img1", TextType.IMAGE, "http://example.com/img1.png"),
            TextNode(" and Image two: ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "http://example.com/img2.png")
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_image_none(self):
        nodes = [TextNode("This text has no images.", TextType.TEXT)]
        result = split_nodes_image(nodes)
        expected = [TextNode("This text has no images.", TextType.TEXT)]
        self.assertEqual(result, expected)

class TestSplitNodesLink(unittest.TestCase):
    def test_split_nodes_link_basic(self):
        nodes = [TextNode("Here is a link: [Google](http://google.com)", TextType.TEXT)]
        result = split_nodes_link(nodes)
        expected = [
            TextNode("Here is a link: ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "http://google.com")
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_link_multiple(self):
        nodes = [TextNode("Link one: [Example1](http://example1.com) and Link two: [Example2](http://example2.com)", TextType.TEXT)]
        result = split_nodes_link(nodes)
        expected = [
            TextNode("Link one: ", TextType.TEXT),
            TextNode("Example1", TextType.LINK, "http://example1.com"),
            TextNode(" and Link two: ", TextType.TEXT),
            TextNode("Example2", TextType.LINK, "http://example2.com")
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_link_none(self):
        nodes = [TextNode("This text has no links.", TextType.TEXT)]
        result = split_nodes_link(nodes)
        expected = [TextNode("This text has no links.", TextType.TEXT)]
        self.assertEqual(result, expected)

class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_text_nodes_dynamic(self):
        text = "This is **bold** text and this is _italic_ text. Here is a [link](http://example.com) and an image ![alt](http://example.com/img.png)."
        nodes = [TextNode(text, TextType.TEXT)]
        
        # First split by images
        nodes = split_nodes_image(nodes)
        # Then split by links
        nodes = split_nodes_link(nodes)
        # Then split by bold
        nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        # Then split by italic
        nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text and this is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text. Here is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "http://example.com"),
            TextNode(" and an image ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "http://example.com/img.png"),
            TextNode(".", TextType.TEXT)
        ]
        self.assertEqual(nodes, expected)

        text2 = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected2 = [
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
        nodes2 = [TextNode(text2, TextType.TEXT)]
        nodes2 = split_nodes_image(nodes2)
        nodes2 = split_nodes_link(nodes2)
        nodes2 = split_nodes_delimiter(nodes2, "**", TextType.BOLD)
        nodes2 = split_nodes_delimiter(nodes2, "_", TextType.ITALIC)
        nodes2 = split_nodes_delimiter(nodes2, "`", TextType.CODE)
        self.assertEqual(nodes2, expected2)
        
    
    
if __name__ == "__main__":
    unittest.main()

