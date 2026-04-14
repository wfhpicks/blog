# 🖥️ Budget Desk HQ — Automated SEO Affiliate Blog

An automated blog that publishes one SEO-optimized, Amazon-affiliate-monetized
article per day using Google Gemini AI. Zero ongoing effort after setup.

**Revenue model:** Google organic traffic → Amazon affiliate commissions
**Target:** $100–$500/month after 3–6 months of consistent posting

---

## 🚀 One-Time Setup (30 minutes)

### Step 1 — Fork this repository

1. Click **Fork** at the top-right of this GitHub page
2. Name it `budget-office-blog` (keeps the URL clean)
3. Make sure it's a **public** repo (required for free GitHub Pages)

### Step 2 — Get a free Google Gemini API key

1. Go to [aistudio.google.com](https://aistudio.google.com)
2. Sign in with your Google account
3. Click **Get API key** → **Create API key in new project**
4. Copy the key — you'll need it in Step 4

### Step 3 — Sign up for Amazon Associates (free)

1. Go to [affiliate-program.amazon.com](https://affiliate-program.amazon.com)
2. Sign up with your Amazon account (free)
3. During signup, enter your GitHub Pages URL:
   `https://YOUR_USERNAME.github.io/budget-office-blog`
4. Once approved, find your **Associate tag** (format: `yourname-20`)
5. Keep this for Step 4

> **Note:** Amazon sometimes takes 24-48 hours to approve new accounts.
> The blog will still publish posts during this time — links will just use your
> tag once you add it.

### Step 4 — Add secrets to GitHub Actions

1. In your forked repo, go to **Settings → Secrets and variables → Actions**
2. Click **New repository secret** and add:

| Secret name            | Value                    |
|------------------------|--------------------------|
| `GEMINI_API_KEY`       | Your Gemini API key      |
| `AMAZON_AFFILIATE_TAG` | Your tag, e.g. `mysite-20` |

### Step 5 — Enable GitHub Pages

1. In your repo, go to **Settings → Pages**
2. Under **Source**, select **Deploy from a branch**
3. Choose branch: `main`, folder: `/ (root)`
4. Click **Save**
5. Your site will be live at: `https://YOUR_USERNAME.github.io/budget-office-blog`

### Step 6 — Update your site URL

Open `_config.yml` and update:
```yaml
url: "https://YOUR_USERNAME.github.io"
```
Also update `robots.txt` with your real URL.

Commit and push. GitHub Pages will rebuild automatically.

### Step 7 — Generate your first posts

1. Go to **Actions** tab in your repo
2. Click **Daily Post Generator** → **Run workflow**
3. Run it 5 times to seed the blog with initial content
4. Your posts will appear at your GitHub Pages URL within 2-3 minutes

After this, GitHub Actions runs automatically every day at 8am UTC. 🎉

---

## 📅 Automation Schedule

| What                  | When                | How                        |
|-----------------------|---------------------|----------------------------|
| New blog post         | Daily at 8am UTC    | GitHub Actions + Gemini AI |
| Site rebuild          | On every push       | GitHub Pages (automatic)   |
| Sitemap update        | On every push       | jekyll-sitemap plugin      |

The blog has **50 pre-loaded topics** to start. After all 50 are used,
the system automatically loops back and regenerates fresh content.

---

## 💰 Revenue Expectations

| Timeframe   | Monthly Sessions | Estimated Revenue     |
|-------------|------------------|-----------------------|
| Month 1–2   | 10–100           | $0–$5                 |
| Month 3–4   | 200–1,000        | $5–$40                |
| Month 5–6   | 1,000–5,000      | $40–$150              |
| Month 6–12  | 5,000–20,000     | $150–$600             |

SEO takes 3–6 months to gain momentum. The more posts published, the more
long-tail keywords you rank for. At 180 posts (6 months), you'll cover a wide
range of purchase-intent keywords.

**Amazon Associates commission rates for home office category:** 3–8%
A visitor who buys a $150 office chair = **$4.50–$12 commission**.

---

## 🔧 Optional Enhancements

- **Google Search Console** — Submit your sitemap for faster indexing:
  `https://YOUR_USERNAME.github.io/budget-office-blog/sitemap.xml`
- **Google Analytics** — Add your GA4 tracking ID to `_config.yml`
- **Custom domain** — Point a cheap `.com` domain to GitHub Pages for
  better SEO authority (Namecheap has domains for ~$10/year)
- **More topics** — Edit `topics/topics.json` to add more niche keywords
- **Pinterest automation** — Pin post images to Pinterest boards for
  extra traffic (use a free Make.com automation)

---

## 📂 File Structure

```
.github/workflows/generate-post.yml  ← Daily automation (DO NOT EDIT)
_posts/                              ← Auto-generated blog posts
scripts/generate_post.py             ← AI content generator
scripts/requirements.txt             ← Python dependencies
topics/topics.json                   ← 50 pre-loaded topic ideas
topics/topics_used.json              ← Tracks which topics were published
_config.yml                          ← Site settings (UPDATE URL HERE)
_layouts/                            ← Jekyll templates
assets/css/style.css                 ← Site styling
```

---

## ⚠️ Legal Notes

- The affiliate disclosure on every post satisfies FTC requirements
- Amazon Associates requires a privacy policy (included at `/privacy/`)
- Google Gemini free tier: 1,500 requests/day — far more than needed
- AI-generated content is fully legal; Google does not penalize quality
  AI content that is helpful to users

---

## ❓ Troubleshooting

**Posts not appearing?**
→ Check Actions tab for workflow errors. Most common: invalid API key secret name.

**Amazon links not tracking?**
→ Ensure `AMAZON_AFFILIATE_TAG` secret is set exactly (e.g. `yourname-20`).

**GitHub Pages not building?**
→ Check Settings → Pages → ensure source branch is `main`.

**Gemini rate limit error?**
→ The free tier allows 15 requests/minute. Running the workflow once per day
will never hit this limit.
