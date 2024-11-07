import unittest
from blocks import markdown_to_blocks, block_to_block_type, markdown_to_html_node, extract_title
from textnode import TextType, TextNode
from htmlnode import ParentNode, LeafNode

class TestBlocks(unittest.TestCase):
  def test_markdown_to_blocks(self):
    doc = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"
    result = markdown_to_blocks(doc)
    expected = [
      '# This is a heading', 
      'This is a paragraph of text. It has some **bold** and *italic* words inside of it.', 
      '* This is the first list item in a list block\n* This is a list item\n* This is another list item'
      ]
    self.assertEqual(result, expected)
  
  def test_block_to_block_heading(self):
    block = "### This is a heading"
    result = block_to_block_type(block)
    expected = "heading"
    self.assertEqual(result, expected)
  
  def test_quote_block(self):
    block = "> Quote 1\n> Quote 2"
    result = block_to_block_type(block)
    expected = "quote"
    self.assertEqual(result, expected)

  def test_not_quote_block(self):
    block = "> Quote 1\n Quote 2"
    result = block_to_block_type(block)
    expected = "paragraph"
    self.assertEqual(result, expected)
    
  def test_code_block(self):
    block = "```\nhello world\n```"
    result = block_to_block_type(block)
    expected = "code"
    self.assertEqual(result, expected)
  
  def test_ul_block(self):
    block = "* Item 1\n* Item 2"
    result = block_to_block_type(block)
    expected = "unordered_list"
    self.assertEqual(result, expected)
    
  def test_not_ul_block(self):
    block = "* Item 1\n- Item 2"
    result = block_to_block_type(block)
    expected = "paragraph"
    self.assertEqual(result, expected)
    
  def test_ol_block(self):
    block = "1. Item 1\n2. Item 2"
    result = block_to_block_type(block)
    expected = "ordered_list"
    self.assertEqual(result, expected)
    
  def test_h1_extract(self):
    h1 = "# Hello world"
    result = extract_title(h1)
    expected = "Hello world"
    self.assertEqual(result, expected)
  
  def test_h1_extract_two(self):
    h1 = "# Hello world  "
    result = extract_title(h1)
    expected = "Hello world"
    self.assertEqual(result, expected)

  # def test_paragraph_block(self):
  #   block = "This is a paragraph."
  #   result = markdown_to_html_node(block)
  #   expected = ParentNode("div", [
  #     ParentNode("p", [LeafNode(None, "This is a paragraph.", None)])
  #   ])
  #   print(f"RESULT: {result}")
  #   print(f"EXPECTED: {expected}")
  #   self.assertEqual(result, expected)

  # def test_heading_block(self):
  #   block = "### This is a heading"
  #   result = markdown_to_html_node(block)
  #   expected = ParentNode("div", [
  #       ParentNode("h3", [LeafNode(None, "This is a heading", None)])
  #   ])
    
  #   self.assertEqual(result, expected)

  # def test_quote_block(self):
  #   block = "> This is a quote\n> with multiple lines."
  #   result = markdown_to_html_node(block)
  #   expected = ParentNode("blockquote", [
  #       ParentNode("p", [LeafNode(None, "This is a quote", None)]),
  #       ParentNode("p", [LeafNode(None, "with multiple lines.", None)])
  #   ])
  #   self.assertEqual(result, expected)
    
    
if __name__ == "__main__":
  unittest.main()