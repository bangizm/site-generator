import shutil
import os
from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode

def recursive_dircopy(src, dest):
    try:
        if os.path.isdir(src):
            if not os.path.exists(dest):
                os.makedirs(dest)
            items = os.listdir(src)   
            for item in items:
                s = os.path.join(src, item)
                d = os.path.join(dest, item)
                recursive_dircopy(s, d)           # shutil.copytree(s, d, dirs_exist_ok=True)
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

if __name__ == "__main__":
    main()
