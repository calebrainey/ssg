import os
import shutil
from textnode import TextType, TextNode
from htmlnode import HTMLNode
from generate_page import generate_page, generate_pages_recursive

def main():
    text_node = TextNode('This is a text node', TextType.BOLD, 'https://boot.dev')
    print(text_node)
    html_node = HTMLNode('div', 'Click Me', ['span'], {'id': 'btn', 'class': 'primary'})
    print(html_node)
    
    build_public_files()
    
def build_public_files():
    public_dir_path = "public"
    # If the directory exists
    if os.path.exists(public_dir_path):
        # Remove the directory
        shutil.rmtree(public_dir_path)
    # Recreate/create the public directory
    os.mkdir(public_dir_path)
    
    # Start copying static files
    copy_static_files(public_dir_path, static_dir="static")
    # Generate index.html using `generate_page`
    # generate_page('content/index.md', 'template.html', os.path.join(public_dir_path, 'index.html'))
    generate_pages_recursive('content', 'template.html', 'public')

def copy_static_files(public_dir_path, static_dir):
    # If static directory exists
    if os.path.exists(static_dir):
        # Make a list of directories and files
        dir_list = os.listdir(static_dir)
        
        for item in dir_list:
            src_path = os.path.join(static_dir, item)
            public_path = os.path.join(public_dir_path, item)
            
            # If a file
            if os.path.isfile(src_path):
                shutil.copy(src_path, public_path)
            # If a directory
            else:
                # Make the new directory
                os.mkdir(public_path)
                # Recursively call the function on the new directory
                copy_static_files(public_path, src_path)
                

if __name__ == "__main__":
    main()
