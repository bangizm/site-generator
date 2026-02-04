from enum import Enum
#TextType = Enum("TextType", ["TEXT", "BOLD", "ITALIC", "CODE", "LINK", "IMAGE"])
class TextType(Enum):
    TEXT = "TEXT"
    BOLD = "BOLD"
    ITALIC = "ITALIC"
    CODE = "CODE"
    LINK = "LINK"
    IMAGE = "IMAGE"

class TextNode:
    def __init__(self, text, texttype, url=None):
        self.text = text
        self.text_type = texttype
        self.url = url

    def __eq__(self, other):
        return(
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
            )
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
    if text_node.text_type not in TextType:
        raise ValueError("Invalid TextType:", text_node.text_type)
    
    from htmlnode import LeafNode
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", None, {"src": text_node.url, "alt": text_node.text})
