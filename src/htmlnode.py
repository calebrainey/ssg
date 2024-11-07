class HTMLNode:
  def __init__(self, tag=None, value=None, children=None, props=None):
    self.tag = tag
    self.value = value
    self.children = children
    self.props = props
    
  def __repr__(self):
    return f'HTMLNode("{self.tag}", "{self.value}", "{self.children}", "{self.props}")'
    
  def to_html(self):
    raise NotImplementedError('to_html method not implemented yet')
  
  def props_to_html(self):
    if self.props is None:
      return ""
    
    props_html = ""
    for key, value in self.props.items():
      props_html += f' {key}="{value}"'
      
    return props_html
  
class LeafNode(HTMLNode):
  def __init__(self, tag, value, props=None):
    super().__init__(tag, value, None, props)
    
  def to_html(self):
    if self.value is None:
      raise ValueError('All leaf nodes must have a value')
    
    if self.tag is None:
      return self.value
    
    return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
  
  def __repr__(self):
    return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
  def __init__(self, tag, children, props=None):
    super().__init__(tag=tag, value=None, children=children, props=props)
    
  def to_html(self):
    if self.tag is None:
      raise ValueError('Does not have a tag.')
    if self.children is None:
      raise ValueError('ParenNode must have children.')
    
    child_node_str = ""
    for child in self.children:
      child_node_str += child.to_html()
    return f"<{self.tag}{self.props_to_html()}>{child_node_str}</{self.tag}>"
  
  def __repr__(self):
    return f"ParentNode({self.tag}, {self.children}, {self.props})"