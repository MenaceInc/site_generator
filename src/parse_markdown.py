import re
from enum import Enum
from textnode import TextNode, TextType


class BlockType(Enum):
    PARAGRAPH       = "paragraph"
    HEADING         = "heading"
    CODE            = "code"
    QUOTE           = "quote"
    UNORDERED_LIST  = "unordered_list"
    ORDERED_LIST    = "ordered_list"


markdown_image_regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
markdown_link_regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"


def block_to_blocktype(block):
    lines = block.split("\n")

    match(block[0]):
        case "#":
            if len(lines) == 1 and \
                lines[0].startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
                return BlockType.HEADING
            
        case "`":
            if lines[0].startswith("```") and lines[-1].endswith("```"):
                return BlockType.CODE
            
        case ">":
            for line in lines:
                if not line.startswith("> "):
                    return BlockType.PARAGRAPH
            return BlockType.QUOTE
        
        case "-":
            for line in lines:
                if not line.startswith("- "):
                    return BlockType.PARAGRAPH
            return BlockType.UNORDERED_LIST
        
        case "1":
            current_index = 1
            for line in lines:
                if not line.startswith(f"{current_index}. "):
                    return BlockType.PARAGRAPH
                current_index += 1
            return BlockType.ORDERED_LIST
        
        case _:
            return BlockType.PARAGRAPH

    return BlockType.PARAGRAPH


def extract_markdown_images(text):
    return re.findall(markdown_image_regex, text)


def extract_markdown_links(text):
    return re.findall(markdown_link_regex, text)


def markdown_to_blocks(markdown):
    if markdown == "":
        return []

    blocks = markdown.split("\n\n")

    for index in range(len(blocks)):
        blocks[index] = blocks[index].lstrip().rstrip()

    result = []

    for block in blocks:
        
        if block != '':
            result.append(block)

    return result


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if delimiter == "":
        raise ValueError("delimiter is empty")
    
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        
        split_strings = node.text.split(delimiter)
        if len(split_strings) % 2 == 0:
            raise Exception("invalid Markdown")
        
        for index in range(len(split_strings)):
            if split_strings[index] == "":
                continue

            if index % 2 == 0:
                result.append(TextNode(split_strings[index], TextType.TEXT))
            else:
                result.append(TextNode(split_strings[index], text_type))
    
    return result


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes