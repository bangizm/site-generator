import shutil
from blocknode import markdown_to_html_node
import os

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    print(f'Generating pages recursively from {dir_path_content} to {dest_dir_path} using template {template_path}')
    # Crawl through dir_path_content recursively to find all .md files
    # For each .md file, generate a new .html using template_path
    # and save it to dest_dir_path, preserving directory structure.

    # ./content/../index.md  --> ./public/../index.html

    for subdirpath, dirnames, filenames in os.walk(dir_path_content):
        for file in filenames:
            if file.endswith(".md"):
                from_path = os.path.join(subdirpath, file)
                dest_path = subdirpath.replace(dir_path_content, dest_dir_path)
                dest_path = os.path.join(dest_path, os.path.splitext(file)[0] + ".html")
                if not os.path.exists(os.path.dirname(dest_path)):
                    os.makedirs(os.path.dirname(dest_path))
                generate_page(from_path, template_path, dest_path, basepath=basepath)

    # os.path.walk() generates the file names in a directory tree by walking the tree either top-down or bottom-up. 
    # For each directory in the tree rooted at directory top (including top itself), it yields a 3-tuple (dirpath, dirnames, filenames).
    ##################################################
    #for root, dirs, files in os.walk(dir_path_content):
    #    for file in files:
    #        if file.endswith('.md'):
    #            from_path = os.path.join(root, file)
    #            relative_path = os.path.relpath(from_path, dir_path_content)
    #            dest_path = os.path.join(dest_dir_path, relative_path)
    #            dest_path = os.path.splitext(dest_path)[0] + '.html'  # change extension to .html
    #            
    #            dest_dir = os.path.dirname(dest_path)
    #            if not os.path.exists(dest_dir):
    #                os.makedirs(dest_dir)
    #            generate_page(from_path, template_path, dest_path, basepath=basepath)

def generate_page(from_path, template_path, dest_path, basepath="/"):

    print(f'...Generating page from {from_path} to {dest_path} using template {template_path}')

    with open(from_path, 'r') as f:    # read markdown file from from_path
        markdown_text = f.read()   
    content_html = markdown_to_html_node(markdown_text).to_html()

    title_text = extract_title(markdown_text)
    # Do I need to remove the title from html_text?
    #content_html = content_html.replace(f'<h1>{title_text}</h1>', '', 1)
    
    with open(template_path, 'r') as f:    # read template file from template_path
        template_text = f.read()
    
    site_html = template_text.replace('{{ Title }}', title_text).replace('{{ Content }}', content_html)
    site_html = site_html.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    site_html = site_html.replace("href='/", f"href='{basepath}").replace("src='/", f"src='{basepath}")


    # write the resulting HTML to dest_path
    #----- print(f'Writing generated HTML to {dest_path}...{site_html=}')
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
                recursive_dircopy(s, d)   # 
                #shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(src, dest)
    except Exception as e:
        print(f'Error copying static files: {e}')


def copy_static_to_dest(dest_dir):
    try:
        shutil.rmtree(dest_dir)
        print(f'Removed existing {dest_dir} directory...')
    except Exception as e:
        print(f'No existing {dest_dir} directory to remove: {e}. No problme. Continuing...')

    try: 
        if not os.path.exists('./static'):
            print('Creating ./static directory...')
            os.mkdir('./static')    
        if not os.path.exists(dest_dir):
            print(f'Creating {dest_dir} directory...')
            os.mkdir(dest_dir)
    except Exception as e:
        print(f'Error creating directories: {e}')
        return
       
    # Copy all files from ./static to ./public
    print('Copying contents of./static to ./public...')
    recursive_dircopy('./static', dest_dir)
    print('Done!')
