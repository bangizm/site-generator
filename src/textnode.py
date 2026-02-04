from enum import Enum
import re

#TextType = Enum("TextType", ["TEXT", "BOLD", "ITALIC", "CODE", "LINK", "IMAGE"])
class TextType(Enum):
    TEXT = "TEXT"
    BOLD = "BOLD"       # **bold**
    ITALIC = "ITALIC"   # _italic_
    CODE = "CODE"       # `code`
    LINK = "LINK"       # [text](url)
    IMAGE = "IMAGE"     # ![alt text](url)

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

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    split = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split = node.text.split(delimiter)
        if len(split) <= 1:
            new_nodes.append(node)
            continue
        if len(split) % 2 == 0:
            # Even number of parts means odd number of delimiters
            # e.g., "This is **bold** text" -> ["This is ", "bold", " text"] (3 parts, 2 delimiters)
            raise ValueError("Invalid Markdown Syntax: Uneven number of delimiters in text:", node.text)
        for i, part in enumerate(split):
            if i % 2 == 0:
                # Even index: normal text
                if part:
                    new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                # Odd index: delimited text
                new_nodes.append(TextNode(part, text_type))
    # ToDo: Handle nested delimiters
    return new_nodes

def extract_markdown_images(text):
    # Extract markdown image text and returns a list of tuples (alt_text, url)
    pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    matches = re.findall(pattern, text)
    image_texts = []
    for alt_text, url in matches:
        image_texts.append((alt_text, url))

    return image_texts

def extract_markdown_links(text):
    # Extract markdown link text and returns a list of tuples (link_text, url)
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    matches = re.findall(pattern, text)
    link_texts = []
    for link_text, url in matches:
        link_texts.append((link_text, url))

    return link_texts