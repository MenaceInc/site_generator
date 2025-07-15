from textnode import TextNode, TextType

def main():
    node = TextNode()
    node.text = "This is some anchor text"
    node.text_type = TextType.LINK_TEXT
    node.url = "https://www.boot.dev"

    print(node)

main()