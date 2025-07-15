from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode

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