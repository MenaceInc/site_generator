import re
from textnode import TextNode, TextType


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        
        split_strings = node.text.split(delimiter)
        if len(split_strings) != 3:
            raise Exception("invalid Markdown")
        
        result.append(TextNode(split_strings[0], TextType.TEXT))
        result.append(TextNode(split_strings[1], text_type))
        result.append(TextNode(split_strings[2], TextType.TEXT))
    
    return result


def split_nodes_image(old_nodes):
    result = []
    
    for node in old_nodes:
        split_strings = re.split(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", node.text)
        step = 3
        
        for index in range(0, len(split_strings), step):     
            if index > (len(split_strings) - 2):
                break  
            result.append(TextNode(split_strings[index], TextType.TEXT))
            result.append(TextNode(split_strings[index + 1], TextType.IMAGE, split_strings[index + 2]))
    
    return result


def split_nodes_link(old_nodes):
    result = []
    
    for node in old_nodes:
        split_strings = re.split(r"\[([^\[\]]*)\]\(([^\(\)]*)\)", node.text)
        step = 3
        
        for index in range(0, len(split_strings), step):     
            if index > (len(split_strings) - 2):
                break  
            result.append(TextNode(split_strings[index], TextType.TEXT))
            result.append(TextNode(split_strings[index + 1], TextType.LINK, split_strings[index + 2]))
    
    return result
