import shutil
import os
import sys
from blocknode import markdown_to_html_node
from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode
from gensite import generate_page, generate_pages_recursive, copy_static_to_public, extract_title


def main():
    copy_static_to_public()

    #TODO: FIX basepath..... FINISH This...
    #basepath = sys.argv[0] if len(sys.argv) > 0 else "/"
    basepath = "/"

    print(f" ... Generating sites using {basepath=}...")
    #generate_page('./content/index.md', './template.html', './public/index.html')
    generate_pages_recursive('./content', './template.html', './public', basepath=basepath)


if __name__ == "__main__":
    main()
