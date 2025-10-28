from htmlnode import LeafNode
from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold" #**str**
    ITALIC = "italic" #_str_
    CODE = "code" #`str`
    LINK = "link" #[str](url)
    IMAGE = "image" #![str](url)

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
    typ = text_node.text_type
    tex = text_node.text
    if typ == TextType.TEXT:
        return LeafNode(None, tex)
    elif typ == TextType.BOLD:
        return LeafNode("b", tex)
    elif typ == TextType.ITALIC:
        return LeafNode("i", tex)
    elif typ == TextType.CODE:
        return LeafNode("code", tex)
    elif typ == TextType.LINK:
        return LeafNode("a", tex, {"href": text_node.url})
    elif typ == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": tex})
    else:
        raise Exception("Not valid type")