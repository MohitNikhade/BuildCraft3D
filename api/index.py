import os
from fastapi import FastAPI

app = FastAPI()

# On Vercel, the root directory during execution houses the public folder
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODELS_DIR = os.path.join(BASE_DIR, "public", "models")

def get_clean_directory_tree(path):
    tree = {"name": os.path.basename(path), "type": "folder", "children": [], "files": []}
    try:
        if not os.path.exists(path):
            return tree
        for entry in os.scandir(path):
            if entry.is_dir():
                sub_tree = get_clean_directory_tree(entry.path)
                if sub_tree["children"] or sub_tree["files"]:
                    tree["children"].append(sub_tree)
            elif entry.is_file() and entry.name.lower().endswith('.glb'):
                clean_name = os.path.splitext(entry.name)[0]
                # Vercel handles serving files inside 'public/' under the root domain automatically
                relative_url = os.path.relpath(entry.path, os.path.join(BASE_DIR, "public")).replace("\\", "/")
                tree["files"].append({"name": clean_name, "url": f"/{relative_url}"})
    except Exception as e:
        print(f"Error scanning {path}: {e}")
    return tree

@app.get("/api/furniture-tree")
def get_furniture():
    furniture_path = os.path.join(MODELS_DIR, "Furniture")
    return get_clean_directory_tree(furniture_path)
