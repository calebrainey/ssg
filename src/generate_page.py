import os
import shutil
from blocks import markdown_to_html_node, extract_title

def generate_page(from_path, template_path, dest_path):  
  # Read the markdown file
  with open(from_path, "r", encoding="utf-8") as f:
    md_content = f.read()
  
  # Read the template file
  with open(template_path, "r", encoding="utf-8") as template_file:
    template_content = template_file.read()
  
  # Get the content for the template page
  html_string = markdown_to_html_node(md_content)
  html = html_string.to_html()
  # Get the title for the template page
  title = extract_title(md_content)  
  
  updated_template = template_content.replace("{{ Title }}", title)
  updated_template = updated_template.replace("{{ Content }}", html)
  
  write_to_html_file(updated_template, dest_path)
  
def write_to_html_file(html_content, destination):
  # Make sure the directory exists
  os.makedirs(os.path.dirname(destination), exist_ok=True)
  
  with open(destination, "w", encoding="utf-8") as file:
    file.write(html_content)
    
""" 
# dir_path_content is the source dir of the md files
# template_path is the template to use
# dest_dir_path is the destination of the new html files/directories
"""
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
  if os.path.exists(dir_path_content):
    dir_list = os.listdir(dir_path_content)
    
    for item in dir_list:
      print(f"PRINT: {item}")
      
      from_path = os.path.join(dir_path_content, item)
      dest_path = os.path.join(dest_dir_path, item)
      
      if os.path.isfile(from_path):
        print("file")
        dest_file_name = f"{item.rstrip(".md")}.html"
        generate_page(from_path, template_path, os.path.join(dest_dir_path, dest_file_name))
      else:
        print("directory")
        generate_pages_recursive(from_path, template_path, dest_path)