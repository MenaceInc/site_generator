import re
from textnode import TextNode, TextType

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