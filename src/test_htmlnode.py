import unittest

from htmlnode import HTMLNode


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

    

if __name__ == "__main__":
    unittest.main()
    