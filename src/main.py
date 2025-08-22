from textnode import *
from blocks import *
import os
import shutil
def copy(src,dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)
    files = os.listdir(src)
    for file in files:
        filePath = os.path.join(src,file)
        destPath = os.path.join(dest,file)
        if os.path.isfile(filePath):
            shutil.copy(filePath,destPath)
        else:
            copy(filePath,destPath)
    return

def generate_page(from_path, template_path, dest_path):
    markdownFile = open(from_path)
    markdown = markdownFile.read()
    markdownFile.close()

    templateFile = open(template_path)
    templateLines = templateFile.readlines()
    title = extract_title(markdown)
    html = markdown_to_html_node(markdown)
    html = html.to_html()

    destFile = open(dest_path, "w")
    for line in templateLines:
        formatted = line.strip()
        if formatted.startswith("<title>"):
            destFile.write(f"<title>{title}</title>")
        elif formatted.startswith("<article>"):
            destFile.write(f"<article>{html}</article>")
        else:
            destFile.write(line)
    templateFile.close()
    destFile.close()
    return

def generateWebsite(from_path, template_path, dest_path):
    if os.path.isdir(from_path):
        files = os.listdir(from_path)
        for file in files:
            filePath = os.path.join(from_path,file)
            destPath = os.path.join(dest_path,file)
            generateWebsite(filePath,template_path,destPath)
    else:
        dest_path = dest_path.replace(".md", ".html")
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        generate_page(from_path, template_path, dest_path)
        
def main():
    copy("static","public")
    #generate_page("content/index.md", "template.html","public/index.html")
    generateWebsite("content", "template.html","public")
main()