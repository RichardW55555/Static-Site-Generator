from enum import Enum

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        lst = ""
        for prop in self.props:
            lst += f' {prop}="{self.props[prop]}"'
        return lst
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value != None:
            if self.tag != None:
                return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
            return self.value
        raise ValueError("invalid HTML: no value")
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag != None:
            if self.children != None:
                string = ""
                for child in self.children:
                    string += child.to_html()
                return f"<{self.tag}{self.props_to_html()}>{string}</{self.tag}>"
            raise ValueError("invalid HTML: no children")
        raise ValueError("invalid HTML: no tag")
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"