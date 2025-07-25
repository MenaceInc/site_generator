import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode()
        node2 = HTMLNode()
        
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = HTMLNode(tag="a")
        node2 = HTMLNode()
        
        self.assertNotEqual(node, node2)

    def test_props_to_html(self):
        node = HTMLNode(tag="a", props={"href": "https://menaceinc.com", "target": "_blank"})
        expected = ' href="https://menaceinc.com" target="_blank"'
        self.assertNotEqual(node.props_to_html(), expected)


class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("p", "Lorem ipsum")
        node2 = LeafNode("p", "Lorem ipsum")
        
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = LeafNode("b", "Bold sample text")
        node2 = LeafNode("p", "Lorem ipsum")
        
        self.assertNotEqual(node, node2)

    def test_to_html(self):
        node = LeafNode("p", "This is a paragraph of text.")
        expected = "<p>This is a paragraph of text.</p>"
        
        self.assertEqual(node.to_html(), expected)


class TestParentNode(unittest.TestCase):
    def test_eq(self):
        node = ParentNode("p", "Lorem ipsum")
        node2 = ParentNode("p", "Lorem ipsum")
        
        self.assertEqual(node, node2)

    def test_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"

        self.assertEqual(node.to_html(), expected)
        
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    

if __name__ == "__main__":
    unittest.main()
    