from textnode import TextNode, TextType

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