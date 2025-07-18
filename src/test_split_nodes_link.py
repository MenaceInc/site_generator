import unittest
from textnode import TextNode, TextType
from split_nodes_link import split_nodes_link

class TestSplitNodesImages(unittest.TestCase):
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