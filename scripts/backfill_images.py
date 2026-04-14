"""One-time script to backfill Pexels hero images into existing posts."""
import os
import re
from pathlib import Path

import requests

PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY", "")
POSTS_DIR = Path(__file__).parent.parent / "_posts"


def fetch_image(query: str) -> dict | None:
    resp = requests.get(
        "https://api.pexels.com/v1/search",
        headers={"Authorization": PEXELS_API_KEY},
        params={"query": query, "per_page": 5, "orientation": "landscape"},
        timeout=10,
    )
    resp.raise_for_status()
    photos = resp.json().get("photos", [])
    if not photos:
        return None
    p = photos[0]
    return {
        "url": p["src"]["large"],
        "photographer": p["photographer"],
        "photographer_url": p["photographer_url"],
        "pexels_url": p["url"],
    }


def main():
    for f in sorted(POSTS_DIR.glob("*.md")):
        text = f.read_text(encoding="utf-8")

        if "hero-image" in text:
            print(f"SKIP (already has image): {f.name}")
            continue

        m = re.search(r'amazon_search: "(.+?)"', text)
        if not m:
            print(f"SKIP (no amazon_search): {f.name}")
            continue
        query = m.group(1)

        img = fetch_image(query)
        if not img:
            print(f"SKIP (no image found for '{query}'): {f.name}")
            continue

        hero_md = (
            f'<figure class="hero-image">\n'
            f'  <img src="{img["url"]}" alt="{query}" loading="lazy" />\n'
            f'  <figcaption>Photo by <a href="{img["photographer_url"]}" '
            f'target="_blank" rel="noopener">{img["photographer"]}</a> on '
            f'<a href="{img["pexels_url"]}" target="_blank" rel="noopener">Pexels</a>'
            f"</figcaption>\n</figure>\n\n"
        )

        parts = text.split("---", 2)
        new_text = "---" + parts[1] + "---\n\n" + hero_md + parts[2].lstrip("\n")
        f.write_text(new_text, encoding="utf-8")
        print(f"OK: {f.name}")
        print(f"    Image: {img['url'][:70]}...")


if __name__ == "__main__":
    main()
