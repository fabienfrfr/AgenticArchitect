#!/usr/bin/env python3
"""
Code Mapper: A bidirectional synchronization tool between code and JSON.

Usage:
    python code_mapper.py --to-json <code_directory> <output_json_file>
    python code_mapper.py --from-json <input_json_file>
"""

import os
import json
import argparse
from typing import List


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


# --- JSON → Code ---
def generate_code_from_json(json_path: str) -> None:
    """Generates files from a JSON structure."""
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
    Generates a JSON describing the structure of a code directory.

    Args:
        root_dir: Root directory to scan.
        output_json_path: Path to the output JSON file.
        extensions: List of file extensions to include (e.g., [".py", ".md"]). If None, all files are included.
    """
    files = []
    if extensions is None:
        extensions = [".py", ".md", ".json", ".yml", ".sh", ".txt"]

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if not any(file_path.endswith(ext) for ext in extensions):
                continue
            relative_path = os.path.relpath(file_path, root_dir)
            content = read_file_content(file_path)
            files.append({"path": relative_path, "content": content})

    project_data = {"files": files}
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(project_data, f, indent=2, ensure_ascii=False)

    print(f"✅ JSON generated: {output_json_path}")


# --- Command Line Interface ---
def main():
    parser = argparse.ArgumentParser(
        description="Code Mapper: Synchronize code and JSON."
    )
    parser.add_argument(
        "--from-json", metavar="JSON_PATH", help="Generate code from a JSON file."
    )
    parser.add_argument(
        "--to-json",
        nargs=2,
        metavar=("ROOT_DIR", "OUTPUT_JSON"),
        help="Generate JSON from a code directory.",
    )
    args = parser.parse_args()

    if args.from_json:
        generate_code_from_json(args.from_json)
    elif args.to_json:
        generate_json_from_code(args.to_json[0], args.to_json[1])
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
