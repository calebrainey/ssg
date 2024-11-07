import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_second_text_eq(self):
        my_node = TextNode("This is my node", TextType.ITALIC)
        my_second_node = TextNode("This is my node", TextType.ITALIC)
        self.assertEqual(my_node, my_second_node)

    def test_not_eq(self):
        good_node = TextNode("This is a good node", TextType.BOLD)
        bad_node = TextNode("This is a good node", TextType.BOLD)
        self.assertEqual(good_node, bad_node)
        
    def test_text_type_node(self):
        node = TextNode("TEST", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "TEST")
        
    def test_bold_type_node(self):
        node = TextNode("bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "bold")
        
    def test_image_type_node(self):
        node = TextNode("alt text", TextType.IMAGE, 'haulershq.com')
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {'src': 'haulershq.com', 'alt': 'alt text'})
        
class TestDelimiter(unittest.TestCase):
    def test_italic_delimeter(self):
        node = TextNode('*This* is a text node.', TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], '*', TextType.ITALIC)
        
        expected_nodes = [
            TextNode('This', TextType.ITALIC),
            TextNode(' is a text node.', TextType.TEXT)
        ]
        self.assertEqual(len(new_nodes), len(expected_nodes))
        for i in range(len(expected_nodes)):
            self.assertEqual(new_nodes[i].text, expected_nodes[i].text)
            self.assertEqual(new_nodes[i].text_type, expected_nodes[i].text_type)
            
    def test_bold_delimeter(self):
        node = TextNode('**This** is a text node.', TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
        
        expected_nodes = [
            TextNode('This', TextType.BOLD),
            TextNode(' is a text node.', TextType.TEXT)
        ]
        self.assertEqual(len(new_nodes), len(expected_nodes))
        for i in range(len(expected_nodes)):
            self.assertEqual(new_nodes[i].text, expected_nodes[i].text)
            self.assertEqual(new_nodes[i].text_type, expected_nodes[i].text_type)
            
    def test_code_delimeter(self):
        node = TextNode('`This` is a text node.', TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], '`', TextType.CODE)
        
        expected_nodes = [
            TextNode('This', TextType.CODE),
            TextNode(' is a text node.', TextType.TEXT)
        ]
        self.assertEqual(len(new_nodes), len(expected_nodes))
        for i in range(len(expected_nodes)):
            self.assertEqual(new_nodes[i].text, expected_nodes[i].text)
            self.assertEqual(new_nodes[i].text_type, expected_nodes[i].text_type)
            
    def test_code_delimeter(self):
        node = TextNode('`This` is a text node.', TextType.TEXT)
        second_node = TextNode('A second `node`!', TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, second_node], '`', TextType.CODE)
        
        expected_nodes = [
            TextNode('This', TextType.CODE),
            TextNode(' is a text node.', TextType.TEXT),
            TextNode('A second ', TextType.TEXT),
            TextNode('node', TextType.CODE),
            TextNode('!', TextType.TEXT)
        ]
        self.assertEqual(len(new_nodes), len(expected_nodes))
        for i in range(len(expected_nodes)):
            self.assertEqual(new_nodes[i].text, expected_nodes[i].text)
            self.assertEqual(new_nodes[i].text_type, expected_nodes[i].text_type)
        
    def test_missing_delimeter(self):
        node = TextNode('This is a **text node.', TextType.TEXT)
        with self.assertRaises(Exception):
            new_nodes = split_nodes_delimiter([node], '**', TextType.ITALIC)
    
    def test_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(text)
        expected = [
            ('rick roll', 'https://i.imgur.com/aKaOqIh.gif'),
            ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')
        ]
        self.assertEqual(result, expected)
        
    def test_links(self):
        text = "This is text with a link **[to boot dev](https://www.boot.dev)** and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = extract_markdown_links(text)
        expected = [
            ('to boot dev', 'https://www.boot.dev'),
            ('to youtube', 'https://www.youtube.com/@bootdotdev')
        ]
        self.assertEqual(result, expected)
        
    def test_split_image_node(self):
        text = TextNode("This is text with an ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) and ![to youtube](https://www.youtube.com/@bootdotdev) images", TextType.TEXT)
        result = split_nodes_image([text])
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev"),
            TextNode(" images", TextType.TEXT)
        ]
        self.assertEqual(result, expected)
        
    def test_split_link_node(self):
        text = TextNode("This is text with an [obi wan](https://i.imgur.com/fJRm4Vk.jpeg) and [to youtube](https://www.youtube.com/@bootdotdev) images", TextType.TEXT)
        result = split_nodes_link([text])
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("obi wan", TextType.LINK, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            TextNode(" images", TextType.TEXT)
        ]
        self.assertEqual(result, expected)
        
    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT), 
            TextNode("text", TextType.BOLD), 
            TextNode(" with an ", TextType.TEXT), 
            TextNode("italic", TextType.ITALIC), 
            TextNode(" word and a ", TextType.TEXT), 
            TextNode("code block", TextType.CODE), 
            TextNode(" and an ", TextType.TEXT), 
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"), 
            TextNode(" and a ", TextType.TEXT), 
            TextNode("link", TextType.LINK, "https://boot.dev")
        ]
        self.assertEqual(result, expected)
        
    def test_text_to_textnodes_double_bold(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) **and** a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT), 
            TextNode("text", TextType.BOLD), 
            TextNode(" with an ", TextType.TEXT), 
            TextNode("italic", TextType.ITALIC), 
            TextNode(" word and a ", TextType.TEXT), 
            TextNode("code block", TextType.CODE), 
            TextNode(" and an ", TextType.TEXT), 
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"), 
            TextNode(" ", TextType.TEXT), 
            TextNode("and", TextType.BOLD), 
            TextNode(" a ", TextType.TEXT), 
            TextNode("link", TextType.LINK, "https://boot.dev")
        ]
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
