import sys
import os
import re


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def parse_frontmatter(content):
    if not content.startswith("---"):
        return {}, content
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        return {}, content
    yaml_str = match.group(1)
    body = content[match.end():]
    meta = {}
    current_key = None
    for line in yaml_str.split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if line.startswith("  - ") and current_key and isinstance(meta.get(current_key), list):
            val = stripped[2:].strip()
            meta[current_key].append(val.strip("'\""))
            continue
        if ":" in stripped:
            key, val = stripped.split(":", 1)
            key = key.strip()
            val = val.strip()
            current_key = key
            if val.startswith("[") and val.endswith("]"):
                items = [x.strip().strip("'\"") for x in val[1:-1].split(",")]
                meta[key] = [i for i in items if i]
            elif val == "":
                meta[key] = []
            else:
                meta[key] = val.strip("'\"")
                current_key = None
    return meta, body


def build_frontmatter(meta):
    lines = ["---"]
    for key, val in meta.items():
        if isinstance(val, list):
            if val:
                lines.append(f"{key}:")
                for item in val:
                    lines.append(f"  - {item}")
            else:
                lines.append(f"{key}: []")
        else:
            lines.append(f"{key}: {val}")
    lines.append("---")
    return "\n".join(lines)


def update_tags(file_path, tags):
    content = read_file(file_path)
    meta, body = parse_frontmatter(content)
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",") if t.strip()]
    existing = meta.get("tags", [])
    if isinstance(existing, str):
        existing = [existing]
    merged = list(dict.fromkeys(existing + tags))
    meta["tags"] = merged
    new_content = build_frontmatter(meta) + "\n" + body
    write_file(file_path, new_content)
    print(f"Updated frontmatter: {file_path} -> tags: {merged}")


def get_tags(file_path):
    content = read_file(file_path)
    meta, _ = parse_frontmatter(content)
    tags = meta.get("tags", [])
    if isinstance(tags, str):
        tags = [tags]
    return tags


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python frontmatter.py <command> <file> [tags]")
        print("Commands: update <file> tag1,tag2,...")
        print("          get <file>")
        sys.exit(1)
    cmd = sys.argv[1]
    fp = sys.argv[2]
    if cmd == "update":
        if len(sys.argv) < 4:
            print("Error: 'update' requires tags argument")
            sys.exit(1)
        update_tags(fp, sys.argv[3])
    elif cmd == "get":
        tags = get_tags(fp)
        print(",".join(tags) if tags else "(no tags)")
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
