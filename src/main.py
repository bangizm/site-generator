import shutil
import os
import sys
from blocknode import markdown_to_html_node
from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode
from gensite import generate_page, generate_pages_recursive, copy_static_to_public, extract_title


def main():
    copy_static_to_public()

    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    print(f" ... Generating sites using {basepath=}...")
    generate_pages_recursive('./content', './template.html', './docs', basepath=basepath)
    #generate_page('./content/index.md', './template.html', './public/index.html')


if __name__ == "__main__":
    main()
