from enum import Enum

class TextType(Enum):
    PLAIN_TEXT = ""
    BOLD_TEXT = "**"
    ITALIC_TEXT = "_"
    CODE_TEXT = "`"
    LINK_TEXT = "[]()"
    IMAGE_TEXT = "![]()"

class TextNode:
    def __init__(self):
        self.text = ""
        self.text_type = TextType.PLAIN_TEXT
        self.url = None

    def __eq__(self, rhs_node):
        return self.text == rhs_node.text and self.text_type == rhs_node.text_type and self.url == rhs_node.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    