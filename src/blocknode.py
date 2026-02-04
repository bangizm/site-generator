from enum import Enum

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    # Remove empty blocks
    blocks = [block.strip() for block in blocks if block.strip()]
    return blocks