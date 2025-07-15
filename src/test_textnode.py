import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    
    def test_text_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    
    def test_text_type_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)


    def test_url_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://menaceinc.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://menaceinc.com")
        self.assertEqual(node, node2)


    def test_url_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://menaceink.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://menaceinc.com")
        self.assertNotEqual(node, node2)


    def test_url_none_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "https://menaceinc.com")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
    