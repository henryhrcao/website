from enum import Enum
from htmlnode import *
from textnode import *
from parentnode import *
import re
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED = "unordered_list"
    ORDERED = "ordered_list"
def markdown_to_blocks(markdown):
    lines = markdown.split("\n\n")
    formattedLines = []
    for line in lines:
        line = line.strip()
        if line != "":
            formattedLines.append(line)
    return formattedLines
def extract_title(markdown):
    lines = markdown.split("\n\n")
    for line in lines:
        line = line.strip()
        if line.startswith("# "):
            line = line.lstrip("# ")
            return line
def block_to_block_type(blocks):
    if blocks.startswith("#"):
        hashes = len(blocks) - len(blocks.lstrip("#"))
        if hashes > 0 and hashes < 7:
            blocks = blocks.lstrip("#")
            if blocks.startswith(" "):
                return BlockType.HEADING
    if blocks.startswith("```") and blocks.endswith("```"):
        return BlockType.CODE
    if blocks.startswith(">"):
        lines = blocks.splitlines()
        correct = True
        for line in lines:
            if not line.startswith(">"):
                correct = False
        if correct: return BlockType.QUOTE
    if blocks.startswith("- "):
        lines = blocks.splitlines()
        correct = True
        for line in lines:
            if not line.startswith("- "):
                correct = False
        if correct: return BlockType.UNORDERED
    
    if blocks.startswith("1. "):
        lines = blocks.splitlines()
        correct = True
        counter = 0
        for line in lines:
            counter +=1
            if not line.startswith(f"{counter}. "):
                correct = False
        if correct: return BlockType.ORDERED
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        BType = block_to_block_type(block)
        #print(f"{block}\n" + "test")
        match BType:
            case BlockType.PARAGRAPH:
                textChildren = text_to_textnodes(block)
                htmlChildren = []
                for text in textChildren:
                    if text.text != "":
                        htmlChildren.append(text_node_to_html_node(text))
                children.append(ParentNode("p", htmlChildren))
            case BlockType.HEADING:
                hSize = len(block) - len(block.lstrip("#"))
                heading = block.lstrip("#")
                heading = heading[1:len(heading)]
                textChildren = text_to_textnodes(heading)
                htmlChildren = []
                for text in textChildren:
                    if text.text != "":
                        htmlChildren.append(text_node_to_html_node(text))
                children.append(ParentNode(f"h{hSize}", htmlChildren))
            case BlockType.QUOTE:
                lines = block.splitlines()
                htmlChildren = []
                counter = 0
                for line in lines:
                    counter += 1
                    textChildren = text_to_textnodes(line)
                    for text in textChildren:
                        text.text = text.text.lstrip("> ")
                        if counter != len(lines):
                            text.text += "\n"
                        if text.text != "":
                            htmlChildren.append(text_node_to_html_node(text))
                children.append(ParentNode("blockquote", htmlChildren))
            case BlockType.CODE:
                text = TextNode(block.strip("```"),TextType.CODE)
                text.text = text.text.lstrip()
                htmlChildren = []
                htmlChildren.append(text_node_to_html_node(text))
                children.append(ParentNode("pre", htmlChildren))
            case BlockType.UNORDERED:
                lines = block.splitlines()
                listChildren = []
                counter = 0
                for line in lines:
                    counter += 1
                    htmlChildren = []
                    textChildren = text_to_textnodes(line)
                    for text in textChildren:
                        text.text = text.text.lstrip("- ")
                        if counter != len(lines):
                            text.text += "\n"
                        html = text_node_to_html_node(text)
                        html.value = html.value.rstrip()
                        if html.value != "":
                            htmlChildren.append(html)
                    listChildren.append(ParentNode("li",htmlChildren))
                children.append(ParentNode("ul", listChildren))
            case BlockType.ORDERED:
                lines = block.splitlines()
                listChildren = []
                counter = 0
                for line in lines:
                    counter += 1
                    htmlChildren = []
                    textChildren = text_to_textnodes(line)
                    for text in textChildren:
                        text.text = text.text.lstrip(f"{counter}. ")
                        if counter != len(lines):
                            text.text += "\n"
                        html = text_node_to_html_node(text)
                        html.value = html.value.rstrip()
                        if html.value != "":
                            htmlChildren.append(html)
                    listChildren.append(ParentNode("li",htmlChildren))
                children.append(ParentNode("ol", listChildren))
    return ParentNode("div", children)