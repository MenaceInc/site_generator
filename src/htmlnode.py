
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
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value == None:
            raise ValueError()
        
        if self.tag == None:
            return self.value
        
        return f"<{self.tag}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Missing tag in ParentNode")

        if self.children == None:
            raise ValueError("Missing children in ParentNode")
        
        result = f"<{self.tag}>"
        for child in self.children:
            result += child.to_html()
        result += f"</{self.tag}>"

        return result