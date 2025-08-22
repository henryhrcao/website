from htmlnode import HTMLNode
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    def to_html(self):
        if self.tag == "img":
            return f'<{self.tag}{self.props_to_html()}>'
        if self.value:
            if self.tag:
                return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
            else: 
                return self.value
        else: raise ValueError(f"No value {self}")