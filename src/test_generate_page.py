import os
import unittest
from generate_page import generate_page, generate_pages_recursive

class TestGeneratePage(unittest.TestCase):
  def test_generate_page(self):
    from_path = "content/index.md"
    template_path = "template.html"
    destination_path = "public/index.html"
    result = generate_page(from_path, template_path, destination_path)
    # print(result)
    
  def test_generate_page_recursive(self):
    dir_path_content = "content"
    template_path = "template.html"
    dest_dir_path = "public"
    result = generate_pages_recursive(dir_path_content, template_path, dest_dir_path)
    print(result)

if __name__ == "__main__":
  unittest.main()