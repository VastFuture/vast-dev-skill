#!/usr/bin/env python3
"""Convert markdown to PDF using markdown-it-py and headless Chrome."""

import subprocess
import sys
from pathlib import Path

try:
    from markdown_it import MarkdownIt
except ImportError:
    print("Install markdown-it-py: pip3 install markdown-it-py")
    sys.exit(1)


CSS = """
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans SC', sans-serif;
    max-width: 800px;
    margin: 0 auto;
    padding: 40px 20px;
    line-height: 1.6;
    color: #333;
}
h1 { font-size: 2em; border-bottom: 2px solid #eee; padding-bottom: 10px; }
h2 { font-size: 1.5em; border-bottom: 1px solid #eee; padding-bottom: 8px; margin-top: 30px; }
h3 { font-size: 1.2em; margin-top: 24px; }
table { border-collapse: collapse; width: 100%; margin: 16px 0; }
th, td { border: 1px solid #ddd; padding: 8px 12px; text-align: left; }
th { background-color: #f5f5f5; font-weight: bold; }
tr:nth-child(even) { background-color: #f9f9f9; }
code { background-color: #f4f4f4; padding: 2px 6px; border-radius: 3px; font-size: 0.9em; }
pre { background-color: #f4f4f4; padding: 16px; border-radius: 6px; overflow-x: auto; }
pre code { background: none; padding: 0; }
blockquote { border-left: 4px solid #ddd; margin: 16px 0; padding: 8px 16px; color: #666; }
hr { border: none; border-top: 2px solid #eee; margin: 30px 0; }
ul, ol { padding-left: 24px; }
li { margin: 4px 0; }
"""


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} input.md output.pdf")
        sys.exit(1)

    md_path = Path(sys.argv[1])
    pdf_path = Path(sys.argv[2])

    if not md_path.exists():
        print(f"File not found: {md_path}")
        sys.exit(1)

    md_content = md_path.read_text(encoding="utf-8")

    # Strip YAML frontmatter
    if md_content.startswith("---"):
        parts = md_content.split("---", 2)
        if len(parts) >= 3:
            md_content = parts[2].strip()

    md = MarkdownIt("commonmark", {"html": True}).enable("table")
    html_body = md.render(md_content)

    html_full = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>提示词工程系统教程</title>
<style>{CSS}</style>
</head>
<body>
{html_body}
</body>
</html>"""

    html_path = pdf_path.with_suffix(".html")
    html_path.write_text(html_full, encoding="utf-8")

    browser = "/usr/bin/google-chrome"
    cmd = [
        browser,
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=3000",
        f"--print-to-pdf={pdf_path}",
        html_path.resolve().as_uri(),
    ]

    subprocess.run(cmd, check=True)
    print(f"PDF exported: {pdf_path}")
    print(f"HTML exported: {html_path}")


if __name__ == "__main__":
    main()
