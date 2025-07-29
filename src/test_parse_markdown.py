import unittest
from parse_markdown import (
    BlockType,
    block_to_blocktype,
    extract_markdown_images,
    extract_markdown_links,
    markdown_to_blocks,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes
)
from textnode import TextNode, TextType


class TestParseMarkdown(unittest.TestCase):
    def test_block_to_blocktype(self):
        markdown = """
This is a regular paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
"""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(blocks[0]))

        markdown = """
# This is a h1 heading
"""

        blocks = markdown_to_blocks(markdown)
        self.assertEqual(BlockType.HEADING, block_to_blocktype(blocks[0]))

        markdown = """
## This is a h2 heading
"""

        blocks = markdown_to_blocks(markdown)
        self.assertEqual(BlockType.HEADING, block_to_blocktype(blocks[0]))

        markdown = """
### This is a h3 heading
"""

        blocks = markdown_to_blocks(markdown)
        self.assertEqual(BlockType.HEADING, block_to_blocktype(blocks[0]))

        markdown = """
#### This is a h4 heading
"""

        blocks = markdown_to_blocks(markdown)
        self.assertEqual(BlockType.HEADING, block_to_blocktype(blocks[0]))

        markdown = """
##### This is a h5 heading
"""

        blocks = markdown_to_blocks(markdown)
        self.assertEqual(BlockType.HEADING, block_to_blocktype(blocks[0]))

        markdown = """
###### This is a h6 heading
"""

        blocks = markdown_to_blocks(markdown)
        self.assertEqual(BlockType.HEADING, block_to_blocktype(blocks[0]))

        markdown = """
####### This is a malformed heading with 7 hashes and should be considered a paragraph
"""

        blocks = markdown_to_blocks(markdown)
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(blocks[0]))

        markdown = """
# This is a malformed heading with multiple lines
# and should be considered a paragraph
"""

        blocks = markdown_to_blocks(markdown)
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(blocks[0]))

        markdown = """
```
#include <print>
int main(int argc, char* argv[]) {
    std::print("Hello, World!");
    return 0;
}
```
"""

        blocks = markdown_to_blocks(markdown)
        self.assertEqual(BlockType.CODE, block_to_blocktype(blocks[0]))

        markdown = """
``
#include <print>
int main(int argc, char* argv[]) {
    std::print("Malformed code block, missing a backtick at the start");
    std::print("Should be considered a paragraph");
    return 0;
}
```
"""

        blocks = markdown_to_blocks(markdown)
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(blocks[0]))

        markdown = """
> This is a quote block
> Every line must start with a > character and a space
"""

        blocks = markdown_to_blocks(markdown)
        self.assertEqual(BlockType.QUOTE, block_to_blocktype(blocks[0]))

        markdown = """
> This is a malformed quote block
Every line must start with a > character and a space
This should be considered a paragraph
"""

        blocks = markdown_to_blocks(markdown)
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(blocks[0]))

        markdown = """
- This is an unordered list
- with items
- Each item must start with a hyphen and a space
"""

        blocks = markdown_to_blocks(markdown)
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_blocktype(blocks[0]))

        markdown = """
- This is a malformed unordered list
- with items
Each item must start with a hyphen and a space
This should be considered a paragraph
"""

        blocks = markdown_to_blocks(markdown)
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(blocks[0]))

        markdown = """
1. This is an ordered list
2. with items
3. Each item must start with an ascending number, full stop and space
"""

        blocks = markdown_to_blocks(markdown)
        self.assertEqual(BlockType.ORDERED_LIST, block_to_blocktype(blocks[0]))

        markdown = """
1. This is a malformed ordered list
2. with items
Each item must start with an ascending number, full stop and space
This should be considered a paragraph
"""

        blocks = markdown_to_blocks(markdown)
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(blocks[0]))

    def test_extract_markdown_images(self):
        input = ""
        matches = extract_markdown_images(input)
        
        self.assertListEqual(
            matches,
            []
        )
        
        input = "This is text with an ![image](https://menaceinc.com/surprise.png)"
        matches = extract_markdown_images(input)
        
        self.assertListEqual(
            matches,
            [
                ("image", "https://menaceinc.com/surprise.png")
            ]
        )
        
        input = "This is text with ![multiple](https://menaceinc.com/surprise.png) ![images](https://menaceinc.com/wonder.png)"
        matches = extract_markdown_images(input)
        
        self.assertListEqual(
            matches,
            [
                ("multiple", "https://menaceinc.com/surprise.png"),
                ("images", "https://menaceinc.com/wonder.png")
            ]
        )
        
        input = "This is text with a [link](https://menaceinc.com/) and an ![image](https://menaceinc.com/wonder.png)"
        matches = extract_markdown_images(input)
        
        self.assertListEqual(
            matches,
            [
                ("image", "https://menaceinc.com/wonder.png")
            ]
        )
        
        input = "This is text with ![malformed syntax](https://menaceinc.com/surprise.png"
        matches = extract_markdown_images(input)
        
        self.assertListEqual(
            matches,
            []
        )

    def test_extract_markdown_links(self):
        input = ""
        matches = extract_markdown_links(input)

        self.assertListEqual(
            matches,
            []
        )

        input = "This is text with a [super interesting link](https://menaceinc.com/blog)"
        matches = extract_markdown_links(input)

        self.assertListEqual(
            matches,
            [
                ("super interesting link", "https://menaceinc.com/blog")
            ]
        )

        input = "This is text with [multiple](https://menaceinc.com/blog) [links](https://menaceinc.com/cv)"
        matches = extract_markdown_links(input)

        self.assertListEqual(
            matches,
            [
                ("multiple", "https://menaceinc.com/blog"),
                ("links", "https://menaceinc.com/cv")
            ]
        )
        
        input = "This is text with a [link](https://menaceinc.com/) and an ![image](https://menaceinc.com/wonder.png)"
        matches = extract_markdown_links(input)
        
        self.assertListEqual(
            matches,
            [
                ("link", "https://menaceinc.com/")
            ]
        )
        
        input = "This is text with [malformed syntax](https://menaceinc.com"
        matches = extract_markdown_links(input)
        
        self.assertListEqual(
            matches,
            []
        )

    def test_markdown_to_blocks(self):
        md = ""
        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [],
        )

        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

        md = """
             This is **bolded** paragraph            

        This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line       

- This is a list
- with items          
"""
        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

        md = """
This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_split_nodes_delimiter(self):
        node = TextNode("", TextType.TEXT)

        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "", TextType.TEXT)

        node = TextNode("This is text with malformed `code block", TextType.TEXT)
        
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT)
            ]
        )

        node = TextNode("This is text with two `code` `block` sections", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with two ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" ", TextType.TEXT),
                TextNode("block", TextType.CODE),
                TextNode(" sections", TextType.TEXT)
            ]
        )

    def test_split_images(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            new_nodes,
            [
                TextNode("", TextType.TEXT)
            ]
        )

        node = TextNode(
            "This is text with an ![image](https://menaceinc.com/surprise.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://menaceinc.com/surprise.png"),
            ]
        )

        node = TextNode(
            "This is text with ![multiple](https://menaceinc.com/surprise.png) ![images](https://menaceinc.com/wonder.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with ", TextType.TEXT),
                TextNode("multiple", TextType.IMAGE, "https://menaceinc.com/surprise.png"),
                TextNode(" ", TextType.TEXT),
                TextNode("images", TextType.IMAGE, "https://menaceinc.com/wonder.png"),
            ]
        )

    def test_split_linkss(self):
        node = TextNode(
            "This is text with a [link](https://menaceinc.com) and another [cool link](https://duckduckgo.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://menaceinc.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("cool link", TextType.LINK, "https://duckduckgo.com"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        input = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        textnodes = text_to_textnodes(input)

        self.assertListEqual(
            textnodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        )


if __name__ == "__main__":
    unittest.main()
