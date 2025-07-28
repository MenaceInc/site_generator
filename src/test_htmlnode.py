import unittest
from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode()
        node2 = HTMLNode()
        
        self.assertEqual(node, node2)
        
        node = HTMLNode(tag="p")
        node2 = HTMLNode()
        
        self.assertNotEqual(node, node2)
        
        node = HTMLNode(tag="p")
        node2 = HTMLNode(tag="p")
        
        self.assertEqual(node, node2)
    
    def test_repr(self):
        node = HTMLNode()
        expected = "HTMLNode(tag:None, value:None, children:None, props:None)"
        
        self.assertEqual(repr(node), expected)
        
        node = HTMLNode(tag="p", value="Lorem ipsum")
        expected = "HTMLNode(tag:p, value:Lorem ipsum, children:None, props:None)"
        
        self.assertEqual(repr(node), expected)
        
        node = HTMLNode(tag="a", value="my website", props={"href": "https://menaceinc.com"})
        expected = "HTMLNode(tag:a, value:my website, children:None, props:{'href': 'https://menaceinc.com'})"
        
        self.assertEqual(repr(node), expected)
    
    def test_to_html(self):
        node = HTMLNode()
        
        with self.assertRaises(NotImplementedError):
            node.to_html()
    
    def test_props_to_html(self):
        node = HTMLNode()
        expected = ""
        
        self.assertEqual(node.props_to_html(), expected)
        
        node = HTMLNode(props={})
        expected = ""
        
        self.assertEqual(node.props_to_html(), expected)
        
        node = HTMLNode(tag="a", props={"href": "https://menaceinc.com", "target": "_blank"})
        expected = ' href="https://menaceinc.com" target="_blank"'
        
        self.assertEqual(node.props_to_html(), expected)


class TestLeafNode(unittest.TestCase):
    def test_init(self):
        with self.assertRaises(TypeError):
            node = LeafNode()
    
    def test_to_html(self):
        node = LeafNode(tag=None, value=None)
        with self.assertRaises(ValueError):
            node.to_html()
        
        node = LeafNode(tag=None, value="This is an untagged piece of text")
        expected = "This is an untagged piece of text"
        
        self.assertEqual(node.to_html(), expected)
        
        node = LeafNode(tag="p", value="This is a paragraph of text.")
        expected = "<p>This is a paragraph of text.</p>"
        
        self.assertEqual(node.to_html(), expected)


class TestParentNode(unittest.TestCase):
    def test_init(self):
        with self.assertRaises(TypeError):
            node = ParentNode()
    
    def test_to_html(self):
        node = ParentNode(None, None)
        
        with self.assertRaises(ValueError):
            node.to_html()
        
        node = ParentNode("p", None)
        
        with self.assertRaises(ValueError):
            node.to_html()
        
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
        
        child_node = LeafNode("span", "child")
        node = ParentNode("div", [child_node])
        
        expected = "<div><span>child</span></div>"
        
        self.assertEqual(node.to_html(), expected)
        
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        node = ParentNode("div", [child_node])
        
        expected = "<div><span><b>grandchild</b></span></div>"
        
        self.assertEqual(node.to_html(), expected)


if __name__ == "__main__":
    unittest.main()
