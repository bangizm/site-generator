import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        #node1 = HTMLNode("a", "This is an HTMLNode", [HTMLNode()], {"href": "localhost:8080", "target": "_blank"})
        #node2 = HTMLNode("a", "This is an HTMLNode", [HTMLNode()], {"href": "localhost:8080", "target": "_blank"})
        node1 = HTMLNode("a", "This is an HTMLNode", None, {"href": "localhost:8080", "target": "_blank"})
        node2 = HTMLNode("a", "This is an HTMLNode", None, {"href": "localhost:8080", "target": "_blank"})
        self.assertEqual(node1.tag, node2.tag)
        self.assertEqual(node1.value, node2.value)
        self.assertEqual(node1.children, node2.children)
        self.assertEqual(node1.props, node2.props)

    def test_props_to_html(self):
        node1 = HTMLNode("a", "This is an HTMLNode", [HTMLNode()], {"href": "localhost:8080", "target": "_blank"})
        self.assertEqual(node1.props_to_html(), " href='localhost:8080' target='_blank'")

    def test_repr(self):
        node1 = HTMLNode("a", "This is an HTMLNode", [HTMLNode()], {"href": "localhost:8080", "target": "_blank"})
        self.assertEqual(
            f'{node1!r}',
            "HTMLNode(tag=a, value=This is an HTMLNode, children=[HTMLNode(tag=None, value=None, children=None, props=None)], props={'href': 'localhost:8080', 'target': '_blank'})")

    def test_noteq(self):
        node1 = HTMLNode("a", "This is an HTMLNode", [HTMLNode()], {"href": "localhost:8080", "target": "_blank"})
        node2 = HTMLNode("a", "This is an HTMLNode", None, {"href": "localhost:8080", "target": "_blank"})
        self.assertNotEqual(node1, node2)

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

        node1 = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node1.to_html(), "<p>This is a paragraph of text.</p>")

    def test_leaf_repr(self):
        node1 = LeafNode("a", "This is a LeafNode", {"href": "localhost:8080", "target": "_blank"})
        self.assertEqual(
            f'{node1!r}',
            "HTMLNode(tag=a, value=This is a LeafNode, props={'href': 'localhost:8080', 'target': '_blank'})")

    def test_leaf_equal_a(self):
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node2.to_html(), "<a href='https://www.google.com'>Click me!</a>")

        node1 = LeafNode(None, "This is a LeafNode", {"href": "localhost:8080", "target": "_blank"})
        self.assertEqual(node1.to_html(), "This is a LeafNode")

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
        leaf_node = LeafNode("span", "I am a child LeafNode");
        leaf_node_with_props = LeafNode("a", "I am a child with props LeafNode", {"href": "http://example.com"});
        parent_node = ParentNode("div", [leaf_node, leaf_node_with_props]);
        self.assertEqual(
            parent_node.to_html(),
            '<div><span>I am a child LeafNode</span><a href=\'http://example.com\'>I am a child with props LeafNode</a></div>'
        )
        new_parent = ParentNode("", [parent_node])
        #self.assertRaises(ValueError("ParentNode.tag = None or '' UNEXPECTED"), new_parent.to_html)


        # test value==None and children is != None

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_node_to_html_node_plaintext(self):
        text_node = TextNode("Hello, world!", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        expected_node = LeafNode(None, "Hello, world!")
        self.assertEqual(html_node, expected_node)

    def test_text_node_to_html_node_bold(self):
        text_node = TextNode("Bold Text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        expected_node = LeafNode("b", "Bold Text")
        self.assertEqual(html_node, expected_node)

    def test_text_node_to_html_node_link(self):
        text_node = TextNode("Google", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(text_node)
        expected_node = LeafNode("a", "Google", {"href": "https://www.google.com"})
        self.assertEqual(html_node, expected_node)
        
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")