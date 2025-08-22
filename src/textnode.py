from enum import Enum
import re
from leafnode import *
class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self,text,text_type,url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
        pass
    def __eq__(self, value):
        if isinstance(value, TextNode):
            return (self.text == value.text and self.text_type == value.text_type and self.url == value.url)
        else: return False
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
        pass
def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            text_node.text = re.sub(r"\s+", " ", text_node.text)
            return LeafNode(None,value=text_node.text)
        case TextType.BOLD:
            text_node.text = re.sub(r"\s+", " ", text_node.text)
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            text_node.text = re.sub(r"\s+", " ", text_node.text)
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            text_node.text = re.sub(r"\n[ \t]+", "\n", text_node.text)
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            text_node.text = re.sub(r"\s+", " ", text_node.text)
            return LeafNode("a", text_node.text,{"href": text_node.url})
        case TextType.IMAGE:
            text_node.text = re.sub(r"\s+", " ", text_node.text)
            return LeafNode("img", "", {
                "src": text_node.url,
                "alt": text_node.text,
                })
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        while True:
            index1 = text.find(delimiter)
            if index1 == -1:
                if text != "":
                    new_nodes.append(TextNode(text, TextType.TEXT))
                break
            index2 = text.find(delimiter, index1 + len(delimiter))
            if index2 == -1:
                raise Exception("No closing delimiter found")
            if index1 >= 0:
                if text[:index1] != "":
                    new_nodes.append(TextNode(text[:index1], TextType.TEXT))
                new_nodes.append(TextNode(text[index1 + len(delimiter):index2], text_type))
                text = text[index2 + len(delimiter):]
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        text = node.text
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        matches = extract_markdown_links(text)
        if not matches:
            new_nodes.append(node)
        counter = 0
        for match in matches:
            counter+=1
            sections = text.split(f"[{match[0]}]({match[1]})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(match[0], TextType.LINK, match[1]))
            if counter == len(matches) and sections[1] != "":
                new_nodes.append(TextNode(sections[1], TextType.TEXT))
            text = sections[1]
    return new_nodes

def split_nodes_images(old_nodes):
    new_nodes = []
    for node in old_nodes:
        text = node.text
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        matches = extract_markdown_images(text)
        if not matches:
            new_nodes.append(node)
        counter = 0
        for match in matches:
            counter+=1
            sections = text.split(f"![{match[0]}]({match[1]})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(match[0], TextType.IMAGE, match[1]))
            if counter == len(matches) and sections[1] != "":
                new_nodes.append(TextNode(sections[1], TextType.TEXT))
            text = sections[1]
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes,"**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes,"_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes,"`", TextType.CODE)
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches
def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


