from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

def extract_title(markdown):
  block_list = markdown.split("\n\n")
  for block in block_list:
    if block.startswith("#") and block.count("#") == 1:
      clean_h1 = block.lstrip("#").strip()
      return clean_h1
    else: 
      raise Exception("No h1 heading found")

def markdown_to_blocks(markdown):
  block_list = markdown.split("\n\n")

  stripped_blocks = []
  for block in block_list:
    if block == "":
      continue
    block = block.strip()
    stripped_blocks.append(block)
  
  return stripped_blocks

def block_to_block_type(block):
  lines = block.split("\n")
  
  # check for headings
  if block.startswith('#'):
    heading_num = block.count("#")
    if heading_num and heading_num <= 6 and block[heading_num] == " ":
      return "heading"
  
  # check for code
  if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
    return "code"
  
  # check for quote
  if block.startswith(">"):
    for line in lines:
      if not line.startswith(">"):
        return "paragraph"
    return "quote"
  
  # check for unordered list
  if block.startswith("* "):
    for line in lines:
      if not line.startswith("* "):
        return "paragraph"
    return "unordered_list"
  
  if block.startswith("- "):
    for line in lines:
      if not line.startswith("- "):
        return "paragraph"
    return "unordered_list"
  
  # check for ordered list
  if block.startswith("1. "):
    i = 1
    for line in lines:
      if not line.startswith(f"{i}. "):
        return "paragraph"
      i += 1
    return "ordered_list"
      
  return "paragraph"

""" """ """ """ """ """ """ """
""" """ """ """ """ """ """ """
def markdown_to_html_node(markdown):
  blocks  = markdown_to_blocks(markdown)
  child_nodes = []
  
  for block in blocks:
    block_type = block_to_block_type(block)
    
    if block_type == "paragraph":
      # Block to list of text nodes
      text_child_nodes = text_to_textnodes(block)
      # Take the list of text nodes to html
      text_html = ParentNode('p', list(map(lambda node: text_node_to_html_node(node), text_child_nodes)))
      # Add html node to overall child nodes
      child_nodes.append(text_html)
    elif block_type == "quote":
      lines = block.split("\n")
      quote_paragraphs = []
      for line in lines:
        # If it's not a quote, raise an error
        if not line.startswith(">"):
          raise ValueError("Invalid quote block")
        
        quote_paragraphs.append(line.lstrip(">").strip())
      
      content = " ".join(quote_paragraphs)
      quote_text_node = text_to_textnodes(content)
      quote_parent = ParentNode('blockquote', list(map(lambda node: text_node_to_html_node(node), quote_text_node)))
      child_nodes.append(quote_parent)
    elif block_type == "heading":
      # Get heading number
      heading_num = block.count("#")
      # Get the heading text
      text = block[heading_num + 1:].strip()
      # Make the text a text node
      heading_child_nodes = text_to_textnodes(text)
      # Take the text to html
      heading = ParentNode(f"h{heading_num}", list(map(lambda node: text_node_to_html_node(node), heading_child_nodes)))
      # Add heading to overall child nodes
      child_nodes.append(heading)
    elif block_type == "unordered_list":
      lines = block.split("\n")
      ul_items = []
      for line in lines:
        if not (line.startswith("*") or line.startswith("-")):
          raise ValueError("Not a valid list item")
        
        # Clean the line
        clean_line = line.lstrip("*-").strip()
        # Make the text a list of text nodes
        line_child_nodes = text_to_textnodes(clean_line)
        # Make the line nodes a list item
        line_li = ParentNode('li', list(map(lambda node: text_node_to_html_node(node), line_child_nodes)))
        # Add to ul_items
        ul_items.append(line_li)
      # Put all ul items into the ul parent
      ul_parent = ParentNode('ul', ul_items)
      # Add to overall child nodes
      child_nodes.append(ul_parent)
    elif block_type == "ordered_list":
      lines = block.split("\n")
      ol_items = []
      for line in lines:
        # Get the text and clean it
        text = line[3:].strip()
        # Make the text a list of text nodes
        line_child_nodes = text_to_textnodes(text)
        # Make the line nodes a list item
        line_li = ParentNode('li', list(map(lambda node: text_node_to_html_node(node), line_child_nodes)))
        # Add to the ol items
        ol_items.append(line_li)
      # Put all the ol items in the ol parent
      ol_parent = ParentNode('ol', ol_items)
      # Add to overall child nodes
      child_nodes.append(ol_parent)
    elif block_type == "code":
      if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Not a valid code block")

      # Get the text
      text = block[4:-3]
      # Convert text to child nodes
      code_child_nodes = text_to_textnodes(text)
      # Create the code node
      code_node = ParentNode('code', list(map(lambda node: text_node_to_html_node(node), code_child_nodes)))
      # Create the pre node
      pre_node = ParentNode('pre', [code_node])
      # Add to overall child nodes
      child_nodes.append(pre_node)    

  html_node = ParentNode('div', child_nodes)
  return html_node