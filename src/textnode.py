from enum import Enum

class TextType(Enum):
    PLAIN = ""
    BOLD = "**"
    ITALIC = "_"
    CODE = "`"
    LINK = "[]()"
    IMAGE = "![]()"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, rhs_node):
        return self.text == rhs_node.text and self.text_type == rhs_node.text_type and self.url == rhs_node.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    