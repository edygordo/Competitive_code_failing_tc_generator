from __future__ import annotations
import re
from typing import List, Dict, Any


def parse_inline(text: str) -> List[Dict[str, Any]]:
    """Parse inline bold markers (**bold**) into segments.

    Returns list of segments: {type: 'text'|'bold', text: str}
    """
    parts: List[Dict[str, Any]] = []
    idx = 0
    # regex to find **bold** segments
    pattern = re.compile(r"\*\*(.+?)\*\*")
    for m in pattern.finditer(text):
        if m.start() > idx:
            parts.append({"type": "text", "text": text[idx:m.start()]})
        parts.append({"type": "bold", "text": m.group(1)})
        idx = m.end()
    if idx < len(text):
        parts.append({"type": "text", "text": text[idx:]})
    if not parts:
        return [{"type": "text", "text": text}]
    return parts


def parse_explanation(text: str) -> List[Dict[str, Any]]:
    """Parse a multi-line explanation into structured blocks.

    Supported block types:
      - heading (lines starting with '#')
      - subheading (line that ends with ':')
      - bullet_list (consecutive lines starting with '-' or '*')
      - numbered_list (consecutive lines starting with '1.' etc.)
      - arrow_line (line containing '->')
      - paragraph (default)

    Inline bold markers (**bold**) are parsed into segments.
    """
    if not text:
        return []

    lines = text.splitlines()
    blocks: List[Dict[str, Any]] = []
    i = 0
    n = len(lines)

    def flush_bullets(items: List[str], ordered: bool = False):
        if not items:
            return
        block = {"type": "ordered_list" if ordered else "bullet_list", "items": []}
        for it in items:
            block["items"].append({"inline": parse_inline(it.strip())})
        blocks.append(block)

    while i < n:
        line = lines[i].rstrip()
        if not line.strip():
            i += 1
            continue

        # heading
        if line.lstrip().startswith('#'):
            lvl = len(line) - len(line.lstrip('#'))
            text_content = line.lstrip('#').strip()
            blocks.append({"type": "heading", "level": lvl, "inline": parse_inline(text_content)})
            i += 1
            continue

        # subheading detection (line ends with ':' and short)
        if line.endswith(':') and len(line) < 120:
            blocks.append({"type": "subheading", "text": line.rstrip(':'), "inline": parse_inline(line.rstrip(':'))})
            i += 1
            continue

        # bullet list
        if re.match(r"^\s*[-*]\s+", line):
            items = []
            while i < n and re.match(r"^\s*[-*]\s+", lines[i]):
                items.append(re.sub(r"^\s*[-*]\s+", "", lines[i]))
                i += 1
            flush_bullets(items, ordered=False)
            continue

        # numbered list
        if re.match(r"^\s*\d+\.\s+", line):
            items = []
            while i < n and re.match(r"^\s*\d+\.\s+", lines[i]):
                items.append(re.sub(r"^\s*\d+\.\s+", "", lines[i]))
                i += 1
            flush_bullets(items, ordered=True)
            continue

        # arrow line
        if '->' in line:
            parts = [p.strip() for p in line.split('->') if p.strip()]
            blocks.append({"type": "arrow_line", "steps": [parse_inline(p) for p in parts]})
            i += 1
            continue

        # default paragraph: gather consecutive non-empty non-special lines
        para_lines = [line]
        i += 1
        while i < n and lines[i].strip() and not re.match(r"^\s*[-*\d#]", lines[i]) and '->' not in lines[i] and not lines[i].endswith(':'):
            para_lines.append(lines[i].rstrip())
            i += 1
        para_text = "\n".join(para_lines).strip()
        blocks.append({"type": "paragraph", "inline": parse_inline(para_text)})

    return blocks


if __name__ == '__main__':
    sample = """The goal was to print **\"hello world\"**. However, your code `print("hello wld")` has a small typo.

Dry run:
1. Start program
2. Call main()
-> prints wrong string -> fails exact match
"""
    import json
    print(json.dumps(parse_explanation(sample), indent=2))
