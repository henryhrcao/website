
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        pass
    def to_html(self):
        raise NotImplementedError
    def props_to_html(self):
        if(self.props):
            string = ""
            for prop in self.props:
                string += f' {prop}="{self.props[prop]}"'
            return string
        else: return ""
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
