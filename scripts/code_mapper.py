#!/usr/bin/env python3
"""
Code Mapper: A bidirectional synchronization tool between code and JSON.
Optimized with .gitignore support and default pathing.

Usage:
    python scripts/code_mapper.py --to-json
    python scripts/code_mapper.py --from-json scripts/project_structure.json
"""

import os
import json
import argparse
import fnmatch
from typing import List

# --- Default Configurations ---
# Default output: scripts/project_structure.json
DEFAULT_OUTPUT = os.path.join("scripts", "project_structure.json")
# Default root: The parent directory of the 'scripts' folder
DEFAULT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# --- Utility Functions ---
def read_file_content(file_path: str) -> str:
    """Reads the content of a file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(file_path: str, content: str) -> None:
    """Writes a file, creating parent directories if necessary."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"📄 File created: {file_path}")


# --- Gitignore Logic ---
def get_ignored_patterns(root_dir: str) -> List[str]:
    """Reads the .gitignore file and returns a list of patterns to ignore."""
    patterns = [".git", "__pycache__", "*.pyc", ".venv", ".DS_Store", "node_modules"]
    gitignore_path = os.path.join(root_dir, ".gitignore")

    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    patterns.append(line)
    return patterns


def is_ignored(path: str, patterns: List[str]) -> bool:
    """Checks if a path matches any pattern in the ignore list."""
    base_name = os.path.basename(path)
    for pattern in patterns:
        if fnmatch.fnmatch(base_name, pattern) or fnmatch.fnmatch(path, pattern):
            return True
        # Handle directory-specific patterns (e.g., 'dir/')
        if pattern.endswith("/") and fnmatch.fnmatch(base_name, pattern[:-1]):
            return True
    return False


# --- JSON → Code ---
def generate_code_from_json(json_path: str) -> None:
    """Generates files from a JSON structure."""
    if not os.path.exists(json_path):
        print(f"❌ Error: {json_path} not found.")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        project_data = json.load(f)

    for file_info in project_data["files"]:
        write_file(file_info["path"], file_info["content"])

    print("✅ Code generated successfully!")


# --- Code → JSON ---
def generate_json_from_code(
    root_dir: str, output_json_path: str, extensions: List[str] = None
) -> None:
    """
    Generates a JSON describing the structure of a code directory, respecting .gitignore.
    """
    files = []
    if extensions is None:
        extensions = [".py", ".md", ".json", ".yml", ".sh", ".puml", ".txt", ".txt"]

    ignored_patterns = get_ignored_patterns(root_dir)
    print(f"🔍 Scanning: {root_dir}")
    print(f"📁 Output target: {output_json_path}")

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Prune ignored directories to speed up the walk
        dirnames[:] = [
            d
            for d in dirnames
            if not is_ignored(os.path.join(dirpath, d), ignored_patterns)
        ]

        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            relative_path = os.path.relpath(file_path, root_dir)

            if is_ignored(relative_path, ignored_patterns):
                continue

            if not any(file_path.endswith(ext) for ext in extensions):
                continue

            try:
                content = read_file_content(file_path)
                files.append({"path": relative_path, "content": content})
            except Exception as e:
                print(f"⚠️ Could not read {relative_path}: {e}")

    project_data = {"files": files}

    # Ensure the output directory exists (e.g., 'scripts/')
    os.makedirs(os.path.dirname(os.path.abspath(output_json_path)), exist_ok=True)

    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(project_data, f, indent=2, ensure_ascii=False)

    print(f"✅ JSON generated successfully with {len(files)} files.")


# --- Command Line Interface ---
def main():
    parser = argparse.ArgumentParser(
        description="Code Mapper: Synchronize project code and JSON structures."
    )
    parser.add_argument(
        "--from-json",
        nargs="?",
        const=DEFAULT_OUTPUT,
        metavar="JSON_PATH",
        help="Generate code from a JSON file (default: scripts/project_structure.json).",
    )
    parser.add_argument(
        "--to-json",
        nargs="*",
        help="Generate JSON from code. Can take [ROOT_DIR] [OUTPUT_JSON]. Defaults to project root and scripts/project_structure.json.",
    )

    args = parser.parse_args()

    if args.from_json:
        generate_code_from_json(args.from_json)
    elif args.to_json is not None:
        # Determine paths based on provided arguments or defaults
        root = args.to_json[0] if len(args.to_json) > 0 else DEFAULT_ROOT
        output = args.to_json[1] if len(args.to_json) > 1 else DEFAULT_OUTPUT
        generate_json_from_code(root, output)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
