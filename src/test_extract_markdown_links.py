import unittest

from extract_markdown_links import extract_markdown_links

class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_links(
            "This is text with a [super interesting link](https://menaceinc.com/blog)"
        )
        self.assertListEqual([("super interesting link", "https://menaceinc.com/blog")], matches)
