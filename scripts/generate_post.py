"""
generate_post.py
----------------
Automated blog post generator for Budget Desk HQ.
Calls Google Gemini API to write SEO-optimized affiliate posts,
saves them as Jekyll markdown files in _posts/.

Usage:
    python scripts/generate_post.py

Required env vars:
    GEMINI_API_KEY       - Your Google Gemini API key
    AMAZON_AFFILIATE_TAG - Your Amazon Associates tag (e.g. mysite-20)
"""

import os
import json
import re
import sys
import random
from datetime import datetime
from pathlib import Path

import google.generativeai as genai

# ── Config ───────────────────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).parent.parent
TOPICS_FILE = REPO_ROOT / "topics" / "topics.json"
USED_FILE = REPO_ROOT / "topics" / "topics_used.json"
POSTS_DIR = REPO_ROOT / "_posts"

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
AFFILIATE_TAG = os.environ.get("AMAZON_AFFILIATE_TAG", "YOURAFFLTAG-20")

if not GEMINI_API_KEY:
    print("ERROR: GEMINI_API_KEY environment variable is not set.")
    sys.exit(1)


# ── Topic selection ───────────────────────────────────────────────────────────
def pick_topic() -> dict:
    topics = json.loads(TOPICS_FILE.read_text(encoding="utf-8"))["topics"]
    used = json.loads(USED_FILE.read_text(encoding="utf-8"))["used_ids"]

    available = [t for t in topics if t["id"] not in used]

    if not available:
        print("All topics have been used. Resetting topic list.")
        USED_FILE.write_text(json.dumps({"used_ids": []}, indent=2), encoding="utf-8")
        available = topics

    # Prefer the first unused topic for consistent ordering, but add slight
    # randomness to avoid looking robotic.
    topic = random.choice(available[:5]) if len(available) >= 5 else available[0]

    used.append(topic["id"])
    USED_FILE.write_text(json.dumps({"used_ids": used}, indent=2), encoding="utf-8")
    return topic


# ── Gemini call ───────────────────────────────────────────────────────────────
def generate_post_content(topic: dict) -> str:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.0-flash")

    keyword_list = ", ".join(topic["keywords"])
    amazon_search_url = (
        f"https://www.amazon.com/s?k={topic['amazon_search'].replace(' ', '+')}"
        f"&tag={AFFILIATE_TAG}"
    )

    prompt = f"""You are an expert product reviewer and SEO content writer specializing in
budget home office gear. Write a comprehensive, honest, and helpful blog post.

Title: {topic["title"]}
Primary keyword: {topic["keywords"][0]}
Secondary keywords: {keyword_list}

REQUIREMENTS:
1. Length: 1,200–1,600 words (this is critical for SEO).
2. Structure:
   - Opening paragraph with the primary keyword in the first 100 words.
   - "What to Look For" section (3-4 key buying criteria with brief explanations).
   - "Our Top Picks" section with 4-5 specific product recommendations.
     For each product include: product name, estimated price range, 2-3 pros, 1 con,
     and who it is best for. Do NOT use markdown tables — use H3 headings per product.
   - "Budget Tips" section: 2-3 tips to get the best value.
   - Conclusion paragraph with a call to action linking to Amazon search.
3. Tone: Friendly, practical, and trustworthy. No fluff.
4. Include secondary keywords naturally throughout.
5. At the end of the post, include EXACTLY this markdown link for the Amazon call-to-action,
   replacing nothing:
   [Browse all options on Amazon →]({amazon_search_url})
6. Do NOT include any affiliate disclosure text — it is handled separately by the template.
7. Output ONLY the blog post body in markdown. No frontmatter. No title heading at the top
   (the title is already in the frontmatter). Start with the opening paragraph directly.
"""

    response = model.generate_content(prompt)
    return response.text.strip()


# ── Frontmatter builder ───────────────────────────────────────────────────────
def slugify(title: str) -> str:
    slug = title.lower()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"[\s]+", "-", slug.strip())
    slug = re.sub(r"-+", "-", slug)
    return slug[:80].rstrip("-")


def build_frontmatter(topic: dict, excerpt: str) -> str:
    today = datetime.utcnow().strftime("%Y-%m-%d")
    slug = slugify(topic["title"])
    description = excerpt[:155].replace('"', "'").strip()
    keywords = ", ".join(topic["keywords"])

    return f"""---
layout: post
title: "{topic["title"]}"
date: {today}
categories: [reviews, home-office]
tags: [{", ".join(k.replace(" ", "-") for k in topic["keywords"][:3])}]
description: "{description}"
keywords: "{keywords}"
image: /assets/images/og-default.png
amazon_search: "{topic["amazon_search"]}"
---
"""


# ── Save post ─────────────────────────────────────────────────────────────────
def save_post(topic: dict, content: str) -> Path:
    today = datetime.utcnow().strftime("%Y-%m-%d")
    slug = slugify(topic["title"])
    filename = POSTS_DIR / f"{today}-{slug}.md"

    # Extract first sentence as excerpt for description meta tag
    first_sentence = re.split(r"(?<=[.!?])\s", content)[0]
    frontmatter = build_frontmatter(topic, first_sentence)

    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    filename.write_text(frontmatter + "\n" + content, encoding="utf-8")
    print(f"✅ Post saved: {filename.name}")
    return filename


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("🤖 Budget Desk HQ — Automated Post Generator")
    print("=" * 50)

    topic = pick_topic()
    print(f"📝 Topic: {topic['title']}")
    print("⏳ Calling Gemini API...")

    content = generate_post_content(topic)
    path = save_post(topic, content)

    print(f"🎉 Done! New post written: {path}")


if __name__ == "__main__":
    main()
