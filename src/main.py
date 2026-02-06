import shutil
import os
from blocknode import markdown_to_html_node
from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode

def generate_page(from_path, template_path, dest_path):

    print(f'Generating page from {from_path} to {dest_path} using template {template_path}')

    with open(from_path, 'r') as f:    # read markdown file from from_path
        markdown_text = f.read()   
    content_html = markdown_to_html_node(markdown_text).to_html()

    title_text = extract_title(markdown_text)
    # Do I need to remove the title from html_text?
    #content_html = content_html.replace(f'<h1>{title_text}</h1>', '', 1)
    
    with open(template_path, 'r') as f:    # read template file from template_path
        template_text = f.read()
    
    site_html = template_text.replace('{{ Title }}', title_text).replace('{{ Content }}', content_html)

    # write the resulting HTML to dest_path
    print(f'Writing generated HTML to {dest_path}...{site_html=}')
    with open(dest_path, 'w') as f:
        f.write(site_html)

def extract_title(markdown):
    lines = markdown.strip().split('\n')
    for line in lines:
        if line.startswith('# '):
            return line[2:].strip()
    raise Exception("No h1 header found")

def recursive_dircopy(src, dest):
    try:
        if os.path.isdir(src):
            if not os.path.exists(dest):
                os.makedirs(dest)
            items = os.listdir(src)   
            for item in items:
                s = os.path.join(src, item)
                d = os.path.join(dest, item)
                recursive_dircopy(s, d)   # shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(src, dest)
    except Exception as e:
        print(f'Error copying static files: {e}')


def copy_static_to_public():
    try:
        shutil.rmtree('./public')
        print('Removed existing ./public directory...')
    except Exception as e:
        print(f'No existing ./public directory to remove: {e}. No problme. Continuing...')

    try: 
        if not os.path.exists('./static'):
            print('Creating ./static directory...')
            os.mkdir('./static')    
        if not os.path.exists('./public'):
            print('Creating ./public directory...')
            os.mkdir('./public')
    except Exception as e:
        print(f'Error creating directories: {e}')
        return
       
    # Copy all files from ./static to ./public
    print('Copying contents of./static to ./public...')
    recursive_dircopy('./static', './public')
    print('Done!')


def main():
    copy_static_to_public()
    print(" ... Generating index.html ...")
    generate_page('./content/index.md', './template.html', './public/index.html')

if __name__ == "__main__":
    main()
