"""
Fix existing posts:
1. Remove stray lone # lines
2. Convert plain ### Product Name headings to linked Amazon search headings
"""
import re
from pathlib import Path

AFFILIATE_TAG = "wfhpicks-20"
POSTS_DIR = Path(__file__).parent.parent / "_posts"


def heading_to_amazon_link(match: re.Match) -> str:
    hashes = match.group(1)  # e.g. "###"
    name = match.group(2).strip()
    # Skip if already a markdown link
    if name.startswith("["):
        return match.group(0)
    search_query = name.replace(" ", "+")
    url = f"https://www.amazon.com/s?k={search_query}&tag={AFFILIATE_TAG}"
    return f"{hashes} [{name}]({url})"


def fix_post(text: str) -> str:
    # Strip lone # / ## / ### lines
    text = re.sub(r"(?m)^(#{1,3})\s*$", "", text)
    # Convert plain H2/H3 product headings to Amazon links (skip section headings)
    section_headings = {
        "what to look for", "our top picks", "budget tips",
        "conclusion", "final thoughts", "buying guide"
    }
    def maybe_link(m: re.Match) -> str:
        hashes = m.group(1)
        name = m.group(2).strip()
        if not name:
            return ""
        if name.lower().rstrip(":") in section_headings:
            return m.group(0)
        if name.startswith("["):
            return m.group(0)
        # Linkify both ## and ### product headings
        query = name.replace(" ", "+")
        url = f"https://www.amazon.com/s?k={query}&tag={AFFILIATE_TAG}"
        return f"{hashes} [{name}]({url})"

    text = re.sub(r"(?m)^(#{2,3}) (.+)$", maybe_link, text)
    # Collapse extra blank lines left by removed headings
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def main():
    for f in sorted(POSTS_DIR.glob("*.md")):
        raw = f.read_text(encoding="utf-8")
        # Split off frontmatter
        parts = raw.split("---", 2)
        if len(parts) != 3:
            continue
        body = fix_post(parts[2])
        fixed = "---" + parts[1] + "---" + body
        if fixed != raw:
            f.write_text(fixed, encoding="utf-8")
            # Count how many ### links we added
            links = len(re.findall(r"### \[", fixed))
            print(f"Fixed: {f.name} ({links} product links)")
        else:
            print(f"OK (no changes): {f.name}")


if __name__ == "__main__":
    main()
