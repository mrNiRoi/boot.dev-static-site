import re
from htmlnode import LeafNode, ParentNode
from textnode import TextNode, TextType, BlockType


def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"invalid text type: {text_node.text_type}")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise Exception(f"Invalid Markdown syntax: unmatched '{delimiter}'")

        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes

def extract_markdown_images(text):
    maches = re.findall(r"\!\[(.*?)\]\((.*?)\)", text)
    # (r"!\[([^\[\]]*)\]\(([^\(\)]*)\)")
    return maches

def extract_markdown_links(text):
    maches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    # r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return maches


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        images = extract_markdown_images(text)
        if not images:
            new_nodes.append(node)
            continue

        for alt, url in images:
            split_text = text.split(f"![{alt}]({url})", 1)
            if split_text[0]:
                new_nodes.append(TextNode(split_text[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            text = split_text[1]
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes



def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        text = node.text
        links = extract_markdown_links(text)

        if not links:
            new_nodes.append(node)
            continue
        
        for alt, url in links:
            split_text = text.split(f"[{alt}]({url})", 1)
            if split_text[0]:
                new_nodes.append(TextNode(split_text[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.LINK, url))
            text = split_text[1]
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes


def markdown_to_blocks(markdown):
    raw_blocks = re.split(r"\n\s*\n", markdown.strip())
    blocks = []
    for block in raw_blocks:
        lines = [line.strip() for line in block.split("\n") if line.strip() != ""]
        cleaned_block = "\n".join(lines)
        if cleaned_block:
            blocks.append(cleaned_block)
    return blocks


def block_to_block_type(block):

    stripped = block.strip()

    if stripped.startswith("```") and stripped.endswith("```"):
        return BlockType.CODE

    if re.match(r"^#{1,6} ", stripped):
        return BlockType.HEADING
    
    lines = stripped.split("\n")
    if all(line.strip().startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.strip().startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    
    ordered_list = True
    for i, line in enumerate(lines, start=1):
        if not re.match(rf"^{i}\. ", line.strip()):
            ordered_list = False
            break
    if ordered_list and len(lines) > 1:
        return BlockType.ORDERED_LIST
    
    # defult 
    return BlockType.PARAGRAPH


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(tn) for tn in text_nodes]

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            node = ParentNode("p", text_to_children(block.replace("\n", " ")))

        elif block_type == BlockType.HEADING:
            match = re.match(r"^(#{1,6}) (.*)", block)
            level = len(match.group(1))
            content = match.group(2).replace("\n", " ")
            node = ParentNode(f"h{level}", text_to_children(content))

        elif block_type == BlockType.CODE:
            inner_text = block
            if inner_text.startswith("```") and inner_text.endswith("```"):
                inner_text = inner_text[3:-3]
            node = ParentNode("pre", [LeafNode("code", inner_text)])

        elif block_type == BlockType.QUOTE:
            cleaned = "\n".join(line.lstrip("> ").strip() for line in block.split("\n"))
            node = ParentNode("blockquote", text_to_children(cleaned))

        elif block_type == BlockType.UNORDERED_LIST:
            list_items = []
            for line in block.split("\n"):
                text = line.lstrip("- ").strip()
                list_items.append(ParentNode("li", text_to_children(text)))
            node = ParentNode("ul", list_items)

        elif block_type == BlockType.ORDERED_LIST:
            list_items = []
            for line in block.split("\n"):
                text = re.sub(r"^\d+\.\s+", "", line)
                list_items.append(ParentNode("li", text_to_children(text)))
            node = ParentNode("ol", list_items)

        else:
            raise ValueError(f"Unknown block type: {block_type}")

        children.append(node)

    return ParentNode("div", children)
