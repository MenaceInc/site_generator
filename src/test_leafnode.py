import unittest

from leafnode import LeafNode


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

    

if __name__ == "__main__":
    unittest.main()
    