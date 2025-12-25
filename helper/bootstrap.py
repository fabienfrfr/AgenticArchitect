import os
import json

def create_file(file_path: str, content: str):
    """Create a file with the given content, including parent directories."""
    # Gérer le cas des fichiers à la racine (sans dossier parent)
    if os.path.dirname(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        f.write(content)
    print(f"📄 Created: {file_path}")

def main():
    # 1. Load the project structure from JSON
    with open("project_structure.json", "r") as f:
        project_data = json.load(f)

    # 2. Create all files
    for file_info in project_data["files"]:
        create_file(file_info["path"], file_info["content"])

    # 3. Make shell scripts executable
    for script_path in ["apps/deploy.sh", "apps/init_db.sh"]:
        if os.path.exists(script_path):
            os.chmod(script_path, 0o755)
            print(f"🔧 Made executable: {script_path}")

    print("\n✅ Project structure generated successfully!")
    print("📄 See INSTALL.txt for setup instructions.")

if __name__ == "__main__":
    main()

