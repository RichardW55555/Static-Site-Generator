from textnode import TextType, TextNode
from extract_markdown import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    parts = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        if delimiter not in node.text:
            new_nodes.append(node)
            continue
        
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise Exception("Invalid markdown, unmatched delimiter")
        
        for i, part in enumerate(parts):
            if i % 2 == 0:
                if part != "":
                    new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
    return new_nodes

def split_nodes_image(old_nodes):
    lst_of_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            lst_of_nodes.append(node)
            continue
        
        text = node.text
        images = extract_markdown_images(text)
        if not images:
            lst_of_nodes.append(node)
            continue
        
        for alt, url in images:
            needle = f"![{alt}]({url})"
            parts = text.split(needle, 1)
            if len(parts) != 2:
                break
            before, after = parts[0], parts[1]
            if before:
                lst_of_nodes.append(TextNode(before, TextType.TEXT))
            lst_of_nodes.append(TextNode(alt, TextType.IMAGE, url))
            text = after
        
        if text:
            lst_of_nodes.append(TextNode(text, TextType.TEXT))
    return lst_of_nodes

def split_nodes_link(old_nodes):
    lst_of_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            lst_of_nodes.append(node)
            continue
        
        text = node.text
        links = extract_markdown_links(text)
        if not links:
            lst_of_nodes.append(node)
            continue
        
        for alt, url in links:
            needle = f"[{alt}]({url})"
            parts = text.split(needle, 1)
            if len(parts) != 2:
                break
            before, after = parts[0], parts[1]
            if before:
                lst_of_nodes.append(TextNode(before, TextType.TEXT))
            lst_of_nodes.append(TextNode(alt, TextType.LINK, url))
            text = after
        
        if text:
            lst_of_nodes.append(TextNode(text, TextType.TEXT))
    return lst_of_nodes

def text_to_textnodes(text):
    return split_nodes_link(split_nodes_image(split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter([TextNode(text, TextType.TEXT)], "`", TextType.CODE), "_", TextType.ITALIC), "**", TextType.BOLD)))