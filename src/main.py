import shutil
import sys
import os
from markdown_blocks import generate_pages_recursive

def copy_dir(src, dst):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for name in os.listdir(src):
        if name.startswith(".") or "Zone.Identifier" in name:
            continue
        src_path = os.path.join(src, name)
        dst_path = os.path.join(dst, name)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
            print(f"Copied file: {src_path} -> {dst_path}")
        else:
            copy_dir(src_path, dst_path)

def main():
    basepath = "/"
    if len(sys.argv) >=2:
        basepath = sys.argv[1]
    src_dir = "static"
    dst_dir = "docs"
    if os.path.exists(dst_dir):
        shutil.rmtree(dst_dir)
    os.mkdir(dst_dir)
    
    copy_dir(src_dir, dst_dir)
    
    generate_pages_recursive(basepath, "content", "template.html", dst_dir)

if __name__ == "__main__":
    main()