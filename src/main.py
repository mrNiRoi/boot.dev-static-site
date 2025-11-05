import os
import sys
import shutil
import functions
from textnode import TextNode, TextType


def main():

    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    copy_recursive("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown_file = f.read()
    
    with open(template_path, "r") as f:
        template_file = f.read()

    html_str = functions.markdown_to_html_node(markdown_file).to_html()
    title = functions.extract_title(markdown_file)
    
    template_file = template_file.replace("{{ Title }}", title)
    template_file = template_file.replace("{{ Content }}", html_str)

    template_file = template_file.replace('href="/', f'href="{basepath}')
    template_file = template_file.replace('src="/', f'src="{basepath}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(template_file)

def copy_recursive(fromdir, todir):

    if not os.path.exists(todir):
        os.makedirs(todir)
    else:
        for filename in os.listdir(todir):
            file_path = os.path.join(todir, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
    
    for item in os.listdir(fromdir):
        fromdir_path = os.path.join(fromdir, item)
        todir_path = os.path.join(todir, item)

        if os.path.isdir(fromdir_path):
            print(f"Copying directory: {fromdir_path} -> {todir_path}")
            os.makedirs(todir_path, exist_ok=True)
            copy_recursive(fromdir_path, todir_path)
        else:
            print(f"Copying file: {fromdir_path} -> {todir_path}")
            shutil.copy(fromdir_path, todir_path)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):

    for entry in os.listdir(dir_path_content):
        entry_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)

        if os.path.isdir(entry_path):
            generate_pages_recursive(entry_path, template_path, dest_path, basepath)
        elif entry_path.endswith(".md"):
            dest_file = os.path.splitext(dest_path)[0] + ".html"
            generate_page(entry_path, template_path, dest_file, basepath)



if __name__ == "__main__":
    main()