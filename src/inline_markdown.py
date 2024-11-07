import re
from textnode import TextType, TextNode

def text_to_textnodes(text):
  BOLD_DELIMITER = "**"
  ITALIC_DELIMITER = "*"
  CODE_DELIMITER = "`"
  
  node = [TextNode(text, TextType.TEXT)]
  
  node = split_nodes_delimiter(node, BOLD_DELIMITER, TextType.BOLD)
  node = split_nodes_delimiter(node, ITALIC_DELIMITER, TextType.ITALIC)
  node = split_nodes_delimiter(node, CODE_DELIMITER, TextType.CODE)
  node = split_nodes_image(node)
  node = split_nodes_link(node)
    
  return node

def split_nodes_delimiter(old_nodes, delimiter, text_type):
  text_node_list = []
  
  for old_node in old_nodes:
    if old_node.text_type != TextType.TEXT.value:
      text_node_list.append(old_node)
      continue
      
    split_nodes = []  
    use_delimiter = old_node.text.split(delimiter)
    if len(use_delimiter) % 2 == 0:
      raise Exception('Could not find closing delimiter')
    
    for i in range(len(use_delimiter)):
      if use_delimiter[i] == "":
        continue
      if i % 2 != 0:
        split_nodes.append(TextNode(use_delimiter[i], text_type))
      else:
        split_nodes.append(TextNode(use_delimiter[i], TextType.TEXT))
    text_node_list.extend(split_nodes)
  return text_node_list

def split_nodes_image(old_nodes):
  new_nodes = []
  
  for old_node in old_nodes:
    remaining_text = old_node.text
    image_info = extract_markdown_images(old_node.text)
    if not image_info: 
      new_nodes.append(old_node)
      continue
      
    for text, url in image_info:
      sections = remaining_text.split(f"![{text}]({url})", 1)
      
      if sections[0]:
        new_nodes.append(TextNode(sections[0], TextType.TEXT))
        
      new_nodes.append(TextNode(text, TextType.IMAGE, url))
      
      remaining_text = sections[1]
      
    if remaining_text:
      new_nodes.append(TextNode(remaining_text, TextType.TEXT))
  
  return new_nodes

def split_nodes_link(old_nodes):
  new_nodes = []
  
  for old_node in old_nodes:
    remaining_text = old_node.text
    link_info = extract_markdown_links(old_node.text)
    
    if not link_info:
      new_nodes.append(old_node)
      continue
    
    for text, url in link_info:
      sections = remaining_text.split(f"[{text}]({url})", 1)
      
      if sections[0]:
        new_nodes.append(TextNode(sections[0], TextType.TEXT))
      
      new_nodes.append(TextNode(text, TextType.LINK, url))
      
      remaining_text = sections[1]
    
    if remaining_text:
      new_nodes.append(TextNode(remaining_text, TextType.TEXT))
      
  return new_nodes

def extract_markdown_images(text):
  return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
  return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)