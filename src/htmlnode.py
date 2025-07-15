
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __eq__(self, rhs):
        return self.tag == rhs.tag and self.value == rhs.value and self.children == rhs.children and self.props == rhs.props
    
    def __repr__(self):
        return f"HTMLNode(tag:{self.tag}, value:{self.value}, children:{self.children}, props:{self.props})"
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        result = ""
        for key in self.props:
            result += f" {key}={self.props[key]}"
        return result