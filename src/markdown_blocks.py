from enum import Enum
import os
from textnode import text_node_to_html_node
from htmlnode import LeafNode, ParentNode
from split_nodes_delimiter import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    lines = block.splitlines()
    num = 0
    start = 0
    end = len(lines)
    
    while start < end and lines[start] == "":
        start += 1
    while end > start and lines[end-1].strip() == "":
        end -= 1
    trimmed = lines[start:end]
    
    while num < len(block) and block[num] == "#":
        num += 1
    if 1 <= num <= 6 and num < len(block) and block[num] == " ":
        return BlockType.HEADING
    
    if len(trimmed) >= 2 and trimmed[0].strip() == "```" and trimmed[-1].strip() == "```":
        return BlockType.CODE
    
    if all(line.strip().startswith(">") for line in lines if line.strip() != ""):
        return BlockType.QUOTE
    
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    
    if all(line.startswith(f"{idx}. ") for idx, line in enumerate(lines, start=1)):
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def markdown_to_html_node(markdown):
    markdown = markdown_to_blocks(markdown)
    container = ParentNode("div", [])
    for block in markdown:
        block_type = block_to_block_type(block)
        
        if block_type == BlockType.PARAGRAPH:
            lines = [line.strip() for line in block.splitlines() if line.strip() != ""]
            text = " ".join(lines)
            nodes = text_to_textnodes(text)
            html_children = [text_node_to_html_node(n) for n in nodes]
            container.children.append(ParentNode("p", html_children))
        
        elif block_type == BlockType.HEADING:
            num = 0
            while num < len(block) and block[num] == "#":
                num += 1
            text = block[num:].lstrip()
            nodes = text_to_textnodes(text)
            html_children = [text_node_to_html_node(n) for n in nodes]
            container.children.append(ParentNode(f"h{num}", html_children))
        
        elif block_type == BlockType.CODE:
            lines = block.splitlines()
            text = "\n".join(lines[1:-1]) + "\n"
            children = LeafNode(None, text)
            node = ParentNode("code", [children])
            container.children.append(ParentNode("pre", [node]))
        
        elif block_type == BlockType.QUOTE:
            parts = []
            for l in block.splitlines():
                s = l.strip()
                if not s:
                    continue
                if s.startswith(">"):
                    s = s[1:]
                    if s.startswith(" "):
                        s = s[1:]
                    if s == "":
                        continue
                    parts.append(s)
                else:
                    parts.append(l.strip())
            text = " ".join(parts)
            nodes = text_to_textnodes(text)
            html_children = [text_node_to_html_node(n) for n in nodes]
            container.children.append(ParentNode("blockquote", html_children))
        
        elif block_type == BlockType.UNORDERED_LIST:
            lines = [line for line in block.splitlines() if line.strip()]
            list_nodes = []
            for line in lines:
                if line.startswith("- "):
                    item_text = line[2:]
                else:
                    continue
                nodes = text_to_textnodes(item_text)
                children = [text_node_to_html_node(n) for n in nodes]
                list_nodes.append(ParentNode("li", children))
            container.children.append(ParentNode("ul", list_nodes))
        
        elif block_type == BlockType.ORDERED_LIST:
            lines = [line for line in block.splitlines() if line.strip()]
            list_nodes = []
            for idx, line in enumerate(lines, start=1):
                prefix = f"{idx}. "
                if line.startswith(prefix):
                    item_text = line[len(prefix):]
                else:
                    continue
                nodes = text_to_textnodes(item_text)
                children = [text_node_to_html_node(n) for n in nodes]
                list_nodes.append(ParentNode("li", children))
            container.children.append(ParentNode("ol", list_nodes))
    return container

def extract_title(markdown):
    for line in markdown.splitlines():
        s = line.strip()
        if s.startswith("#"):
            hashes = 0
            while hashes < len(s) and s[hashes] == "#":
                hashes += 1
            if hashes == 1 and (len(s) == 1 or s[1].isspace()):
                return s[hashes:].strip()
    raise Exception("No h1 header")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, "r", encoding="utf-8") as f:
        md = f.read()
    
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()
    
    html = markdown_to_html_node(md).to_html()
    title = extract_title(md)
    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(page)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for dir_path in os.listdir(dir_path_content):
        full_src = os.path.join(dir_path_content, dir_path)
        if os.path.isfile(full_src):
            if dir_path.endswith(".md"):
                out_name = dir_path.rsplit(".md", 1)[0] + ".html"
                dst_html = os.path.join(dest_dir_path, out_name)
                generate_page(full_src, template_path, dst_html)
        elif os.path.isdir(full_src):
            dest_path = os.path.join(dest_dir_path, dir_path)
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)
            generate_pages_recursive(full_src, template_path, dest_path)