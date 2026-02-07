import shutil
import os
import sys
from blocknode import markdown_to_html_node
from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode
from gensite import copy_static_to_dest, generate_page, generate_pages_recursive, extract_title


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    dest_dir = './docs'
    copy_static_to_dest(dest_dir)
    print(f" ... Generating sites using {basepath=}...")
    generate_pages_recursive('./content', './template.html', dest_dir, basepath=basepath)
    #generate_page('./content/index.md', './template.html', './public/index.html')


if __name__ == "__main__":
    main()
