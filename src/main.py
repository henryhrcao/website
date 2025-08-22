
from blocks import *
import os
import shutil
import sys
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

def generate_page(from_path, template_path, dest_path, base):
    markdownFile = open(from_path)
    markdown = markdownFile.read()
    markdownFile.close()

    templateFile = open(template_path)
    templateLines = templateFile.readlines()
    title = extract_title(markdown)
    html = markdown_to_html_node(markdown)
    html = html.to_html()
    title = title.replace('href="/', f'href="{base}')
    title = title.replace('src="/', f'src="{base}')
    html = html.replace('href="/', f'href="{base}')
    html = html.replace('src="/', f'src="{base}')
    destFile = open(dest_path, "w")
    for line in templateLines:
        formatted = line.strip()
        if formatted.startswith("<title>"):
            destFile.write(f"<title>{title}</title>")
        elif formatted.startswith("<article>"):
            destFile.write(f"<article>{html}</article>")
        else:
            line = line.replace('href="/', f'href="{base}docs/')
            line = line.replace('src="/', f'src="{base}docs/')
            destFile.write(line)
    templateFile.close()
    destFile.close()
    return

def generateWebsite(from_path, template_path, dest_path, base):
    if os.path.isdir(from_path):
        files = os.listdir(from_path)
        for file in files:
            filePath = os.path.join(from_path,file)
            destPath = os.path.join(dest_path,file)
            generateWebsite(filePath,template_path,destPath,base)
    else:
        dest_path = dest_path.replace(".md", ".html")
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        generate_page(from_path, template_path, dest_path,base)
        
def main():
    basePath = "/"
    if len(sys.argv) ==2:
        basePath = sys.argv[1]
    copy("static","docs")
    #generate_page("content/index.md", "template.html","public/index.html")
    generateWebsite("content", "template.html","docs", basePath)
main()