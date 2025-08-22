from htmlnode import HTMLNode
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    def to_html(self):
        if self.tag:
            if self.children:
                string = f'<{self.tag}{self.props_to_html()}>'
                for child in self.children:
                    string += child.to_html()
                string += f'</{self.tag}>'
                return string
            else: raise ValueError("No Children")
        else: raise ValueError("No value")