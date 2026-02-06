from enum import Enum
import re

from textnode import text_node_to_html_node, text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "PARAGRAPH"
    HEADING = "HEADING"       # 1-6 '#' characters
    CODE = "CODE"       # ``` \n ```
    QUOTE = "QUOTE"      # > blockquote [>]
    UNORDERED_LIST = "UNORDERED_LIST"  # - item or * item
    ORDERED_LIST = "ORDERED_LIST"   # 1. item
    

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    # Remove empty blocks
    blocks = [block.strip() for block in blocks if block.strip()]
    return blocks

def block_to_block_type(markdown):
    #stripped = markdown.lstrip()
    if re.match(r'^#{1,6}\s', markdown): 
        return BlockType.HEADING
    elif re.match(r'^```\s*\n', markdown) and markdown.endswith("```"):
        print(f'__DEBUG__ Detected CODE block: {markdown[:30]=}...')
        return BlockType.CODE
    elif markdown.startswith(">"):  # check each line? ####
        return BlockType.QUOTE
    elif markdown.startswith("- ") or markdown.startswith("* "):
        return BlockType.UNORDERED_LIST
    elif re.match(r'^\d+\.\s', markdown): # check each line? ####
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
    
def markdown_to_html_node(markdown):
    from htmlnode import LeafNode, ParentNode
    blocks = markdown_to_blocks(markdown)
    children = []
    
    for block in blocks:
        block_type = block_to_block_type(block)
        
        if block_type == BlockType.PARAGRAPH:
            # Replace newlines with spaces in paragraphs
            paragraph_text = block.replace('\n', ' ')
            text_nodes = text_to_textnodes(paragraph_text)
            html_nodes = [text_node_to_html_node(node) for node in text_nodes]
            children.append(ParentNode("p", html_nodes))
            
        elif block_type == BlockType.HEADING:
            level = len(re.match(r'^(#{1,6})\s', block).group(1))
            heading_text = re.sub(r'^(#{1,6})\s', '', block)
            text_nodes = text_to_textnodes(heading_text)
            html_nodes = [text_node_to_html_node(node) for node in text_nodes]
            children.append(ParentNode(f'h{level}', html_nodes))
            
        elif block_type == BlockType.CODE:
            code_content = re.sub(r'^```', '', block)
            code_content = re.sub(r'```$', '', code_content)
            children.append(ParentNode("pre", [LeafNode("code", code_content)]))
            
        elif block_type == BlockType.QUOTE:
            quote_lines = [line.lstrip('>').strip() for line in block.split('\n') if line.strip()]
            quote_content = '\n'.join(quote_lines)
            text_nodes = text_to_textnodes(quote_content)
            html_nodes = [text_node_to_html_node(node) for node in text_nodes]
            children.append(ParentNode("blockquote", html_nodes))
            
        elif block_type == BlockType.UNORDERED_LIST:
            print(f'__DEBUG__ Detected UNORDERED_LIST block: {block[:80]=}...')
            items = [line.lstrip('- ').strip() for line in block.split('\n') if line.strip()]
            print(f'__DEBUG__ STRIPPED Unordered list items: {items=}')
            list_items = []
            for item in items:
                print(f'__DEBUG__ Unordered list item: {block_type=} <> {item=}')
                text_nodes = text_to_textnodes(item)
                html_nodes = [text_node_to_html_node(node) for node in text_nodes]
                list_items.append(ParentNode("li", html_nodes))
            children.append(ParentNode("ul", list_items))
            
        elif block_type == BlockType.ORDERED_LIST:
            items = [re.sub(r'^\d+\.\s', '', line).strip() for line in block.split('\n') if line.strip()]
            list_items = []
            for item in items:
                text_nodes = text_to_textnodes(item)
                html_nodes = [text_node_to_html_node(node) for node in text_nodes]
                list_items.append(ParentNode("li", html_nodes))
            children.append(ParentNode("ol", list_items))
            
        else:
            raise ValueError("Unsupported BlockType:", block_type)
    
    return ParentNode("div", children)