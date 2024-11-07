import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
  def test_props_to_html(self):
    node = HTMLNode('a', '', '', {"href": "https://google.com", "target": "_blank"})
    expected = ' href="https://google.com" target="_blank"'
    self.assertEqual(node.props_to_html(), expected)
    
  def test_to_html_error(self):
    node = HTMLNode('div')
    with self.assertRaises(NotImplementedError):
      node.to_html()
      
  def test_default_of_html(self):
    node = HTMLNode()
    self.assertIsNone(node.tag)
    self.assertIsNone(node.value)
    self.assertIsNone(node.children)
    self.assertIsNone(node.props)
    
class TestLeafNode(unittest.TestCase):
  def test_render_p(self):
    leaf_node = LeafNode('p', 'This is a paragraph of text.')
    expected_text = '<p>This is a paragraph of text.</p>'
    self.assertEqual(leaf_node.to_html(), expected_text)
  
  def test_no_tag(self):
    leaf_node = LeafNode(None, 'This does not have a surrounding tag.')
    expected_text = 'This does not have a surrounding tag.'
    self.assertEqual(leaf_node.to_html(), expected_text)
    
class TestParentNode(unittest.TestCase):
  def test_child_node(self):
      child_node = LeafNode('p', 'This is a p child.')
      parent_node = ParentNode('div', [child_node])
      self.assertEqual(parent_node.to_html(), '<div><p>This is a p child.</p></div>')
      
  def test_parent_node_in_parent(self):
    child = LeafNode('p', 'test test test')
    first_parent = ParentNode('div', [child])
    second_parent = ParentNode('div', [first_parent])
    self.assertEqual(second_parent.to_html(), '<div><div><p>test test test</p></div></div>')
    
  def test_parent_no_tag(self):
    child = LeafNode('p', 'test test test')
    parent = ParentNode(None, [child])
    with self.assertRaises(ValueError):
      parent.to_html()
      
  def test_child_no_tag(self):
    child = LeafNode(None, 'test test test')
    parent = ParentNode('div', [child])
    self.assertEqual(parent.to_html(), '<div>test test test</div>')
    
if __name__ == "__main":
  unittest.main()