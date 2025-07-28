from enum import Enum
from htmlnode import HTMLNode, LeafNode


class TextType(Enum):
    TEXT    = "text"
    BOLD    = "bold"
    ITALIC  = "italic"
    CODE    = "code"
    LINK    = "link"
    IMAGE   = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, rhs_node):
        return self.text == rhs_node.text and self.text_type == rhs_node.text_type and self.url == rhs_node.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node):
    new_node = HTMLNode()
    
    match (text_node.text_type):
        case TextType.TEXT:
            new_node = LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            new_node = LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            new_node = LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            new_node = LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            new_node = LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            new_node = LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Unknown text_type when converting TextNode to HTMLNode")
    
    return new_node
