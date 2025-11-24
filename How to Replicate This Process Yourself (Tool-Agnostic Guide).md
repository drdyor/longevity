# How to Replicate This Process Yourself (Tool-Agnostic Guide)

This guide shows you how to implement the exact process I used, using **any tools you want** - whether that's Python scripts, Cursor, n8n, Make.com, or even manual work with ChatGPT.

---

## The Core Logic (Independent of Tools)

The entire process can be broken down into **4 distinct operations** that you can automate with any tool:

```
INPUT → SEARCH → VERIFY → SYNTHESIZE → OUTPUT
```

Let me show you how to implement each operation.

---

## Operation 1: SEARCH (Find Reddit Content)

**Goal:** Get recent, high-quality Reddit posts on your topics of interest.

### Method A: Use Reddit RSS (Easiest, Free Forever)

**How it works:**
- Reddit provides RSS feeds for any subreddit
- No authentication needed
- Works immediately

**The URL pattern:**
```
https://www.reddit.com/r/{SUBREDDIT}.rss
https://www.reddit.com/r/{SUBREDDIT}/search.rss?q={KEYWORD}&restrict_sr=1&sort=new
```

**Concrete example:**
```
https://www.reddit.com/r/longevity.rss
https://www.reddit.com/r/Biohacking/search.rss?q=peptides&restrict_sr=1&sort=new
```

**How to use it:**

**Option 1: Python Script**
```python
import feedparser

url = "https://www.reddit.com/r/longevity.rss"
feed = feedparser.parse(url)

for entry in feed.entries:
    print(f"Title: {entry.title}")
    print(f"Link: {entry.link}")
    print(f"Published: {entry.published}")
    print(f"Summary: {entry.summary[:200]}")
    print("---")
```

**Option 2: Cursor/AI Agent**
```
Prompt: "Fetch the RSS feed from https://www.reddit.com/r/longevity.rss and extract all post titles, links, and summaries. Save to a file called reddit_posts.json"
```

**Option 3: Manual (if you're broke and have time)**
1. Open `https://www.reddit.com/r/longevity.rss` in your browser
2. Copy the XML content
3. Paste into ChatGPT: "Extract all post titles and links from this RSS feed"
4. Save the output

### Method B: Web Scraping (More Powerful)

**When to use:** When you need comments, upvote counts, or more than 25 posts.

**The logic:**
1. Navigate to Reddit search URL: `https://www.reddit.com/r/longevity/search/?q=peptides&restrict_sr=1&sort=new`
2. Extract post containers (HTML elements with class/data attributes)
3. Parse title, link, upvotes, comments from each container
4. Save to file

**Python example:**
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://www.reddit.com/r/longevity/search/?q=peptides&restrict_sr=1&sort=new")
    page.wait_for_selector('h3')  # Wait for posts to load
    
    posts = []
    for title_element in page.query_selector_all('h3'):
        posts.append(title_element.inner_text())
    
    browser.close()
    print(posts)
```

**Cursor/AI Agent equivalent:**
```
Prompt: "Use Playwright to scrape https://www.reddit.com/r/longevity and extract the top 50 post titles and links. Save to reddit_posts.json"
```

---

## Operation 2: VERIFY (Check Against Science)

**Goal:** For each claim found on Reddit, find peer-reviewed evidence.

### The Verification Logic:

```
FOR EACH claim:
    1. Extract the core assertion (e.g., "MOTS-C improves insulin sensitivity")
    2. Search PubMed/Google Scholar for that exact claim
    3. Navigate to the top 3-5 results
    4. Read the abstract/conclusion
    5. Determine: TRUE / PARTIALLY TRUE / MISLEADING / UNSUPPORTED
    6. Save the evidence with citation
```

### How to Search PubMed (Free API, No Auth)

**The URL pattern:**
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={QUERY}&retmax=5&retmode=json
```

**Concrete example:**
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=MOTS-C+insulin+sensitivity&retmax=5&retmode=json
```

**Python implementation:**
```python
import requests

def search_pubmed(query):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        'db': 'pubmed',
        'term': query,
        'retmax': 5,
        'retmode': 'json'
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    # Get list of PubMed IDs
    pmids = data['esearchresult']['idlist']
    
    # For each PMID, get the article details
    for pmid in pmids:
        article_url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
        print(f"Found: {article_url}")
    
    return pmids

# Example
search_pubmed("semaglutide weight loss STEP trial")
```

**Cursor/AI Agent equivalent:**
```
Prompt: "Search PubMed for 'semaglutide weight loss STEP trial'. Get the top 5 results. For each result, navigate to the PubMed page and extract the title, abstract, and publication year. Save to semaglutide_evidence.md"
```

**Manual method (free, slow):**
1. Go to https://pubmed.ncbi.nlm.nih.gov/
2. Search: "semaglutide weight loss STEP trial"
3. Open top 5 results in new tabs
4. Copy-paste abstracts into a document
5. Ask ChatGPT: "Based on these abstracts, is the claim that semaglutide causes 15% weight loss supported?"

---

## Operation 3: SYNTHESIZE (Create the Final Document)

**Goal:** Transform raw evidence into a clean, readable document.

### The Synthesis Logic:

```
FOR EACH topic:
    1. Read all verified evidence files
    2. Create a new document section with:
       - Claim statement
       - Verdict (TRUE/FALSE/PARTIALLY TRUE)
       - Evidence summary (in plain language)
       - Citation to primary source
       - Critical caveats (what Reddit missed)
    3. Append to master document
```

**Python implementation:**
```python
def create_chapter(topic, claims_verified):
    chapter = f"## Chapter: {topic}\n\n"
    
    for claim in claims_verified:
        chapter += f"**Claim:** {claim['statement']}\n\n"
        chapter += f"**Verdict:** {claim['verdict']}\n\n"
        chapter += f"{claim['evidence_summary']}\n\n"
        chapter += f"**Source:** {claim['citation']}\n\n"
        chapter += "---\n\n"
    
    return chapter

# Example
semaglutide_claims = [
    {
        'statement': 'Semaglutide causes 15% weight loss',
        'verdict': 'TRUE',
        'evidence_summary': 'The STEP 1 trial showed 14.9% mean weight loss at 68 weeks.',
        'citation': 'Wilding et al. NEJM 2021'
    }
]

chapter_text = create_chapter("GLP-1 Agonists", semaglutide_claims)
print(chapter_text)
```

**Cursor/AI Agent equivalent:**
```
Prompt: "Read the file verified_semaglutide.md. Create a book chapter with the following structure:
- Chapter title
- For each claim: statement, verdict, evidence summary, citation
- Write in professional, paragraph form
- Save to book_chapter_glp1.md"
```

**Manual method:**
1. Open all your `verified_*.md` files
2. Create a new Google Doc
3. For each topic, write:
   - "Claim: [copy from verified file]"
   - "Verdict: [TRUE/FALSE/etc]"
   - "Evidence: [summarize in your own words]"
   - "Source: [paste the link]"
4. Format nicely

---

## Operation 4: OUTPUT (Package and Deliver)

**Goal:** Create the final files in a usable format.

### The Output Logic:

```
1. Combine all chapters into one master document
2. Add table of contents
3. Add consolidated references section
4. Export to desired format (Markdown, PDF, etc.)
```

**Python implementation:**
```python
import os

def compile_book(chapters_dir, output_file):
    book = "# The Longevity Blueprint\n\n"
    book += "## Table of Contents\n\n"
    
    # Get all chapter files
    chapters = sorted([f for f in os.listdir(chapters_dir) if f.endswith('.md')])
    
    # Add TOC
    for i, chapter_file in enumerate(chapters, 1):
        chapter_title = chapter_file.replace('.md', '').replace('_', ' ').title()
        book += f"{i}. {chapter_title}\n"
    
    book += "\n---\n\n"
    
    # Add each chapter
    for chapter_file in chapters:
        with open(os.path.join(chapters_dir, chapter_file), 'r') as f:
            book += f.read()
            book += "\n\n---\n\n"
    
    # Save final book
    with open(output_file, 'w') as f:
        f.write(book)
    
    print(f"Book compiled: {output_file}")

# Example
compile_book("./chapters", "longevity_book_final.md")
```

**Cursor/AI Agent equivalent:**
```
Prompt: "Combine all files in the ./chapters directory into one master document called longevity_book_final.md. Add a table of contents at the top. Separate each chapter with a horizontal rule."
```

---

## Complete Automation Workflow

Here's how to tie it all together into a single, automated system:

### Weekly Automation Script (Python)

```python
#!/usr/bin/env python3
"""
Weekly Longevity Research Automation
Run this script once a week to update your book with new verified claims
"""

import feedparser
import requests
import time
from datetime import datetime

# 1. SEARCH: Get new Reddit posts
def get_reddit_posts(subreddit, keywords):
    url = f"https://www.reddit.com/r/{subreddit}.rss"
    feed = feedparser.parse(url)
    
    relevant_posts = []
    for entry in feed.entries:
        text = (entry.title + entry.summary).lower()
        if any(kw.lower() in text for kw in keywords):
            relevant_posts.append({
                'title': entry.title,
                'link': entry.link,
                'summary': entry.summary
            })
    
    return relevant_posts

# 2. VERIFY: Check against PubMed
def verify_claim(claim_text):
    # Search PubMed
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        'db': 'pubmed',
        'term': claim_text,
        'retmax': 3,
        'retmode': 'json'
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    pmids = data['esearchresult']['idlist']
    
    if len(pmids) > 0:
        return {
            'verdict': 'EVIDENCE FOUND',
            'pubmed_ids': pmids,
            'links': [f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" for pmid in pmids]
        }
    else:
        return {
            'verdict': 'NO EVIDENCE FOUND',
            'pubmed_ids': [],
            'links': []
        }

# 3. SYNTHESIZE: Create report
def create_report(posts_with_evidence):
    report = f"# Weekly Longevity Research Report - {datetime.now().strftime('%Y-%m-%d')}\n\n"
    
    for post in posts_with_evidence:
        report += f"## {post['title']}\n\n"
        report += f"**Verdict:** {post['verdict']}\n\n"
        if post['evidence_links']:
            report += "**Evidence:**\n"
            for link in post['evidence_links']:
                report += f"- {link}\n"
        report += "\n---\n\n"
    
    return report

# 4. MAIN WORKFLOW
def main():
    # Configuration
    subreddits = ['longevity', 'Biohacking', 'Peptides']
    keywords = ['GLP-1', 'semaglutide', 'MOTS-C', 'peptide', 'mitochondria']
    
    all_posts = []
    
    # Step 1: Gather posts
    for sub in subreddits:
        posts = get_reddit_posts(sub, keywords)
        all_posts.extend(posts)
        time.sleep(2)  # Be polite
    
    # Step 2: Verify each post
    posts_with_evidence = []
    for post in all_posts:
        evidence = verify_claim(post['title'])
        posts_with_evidence.append({
            'title': post['title'],
            'verdict': evidence['verdict'],
            'evidence_links': evidence['links']
        })
        time.sleep(1)  # Be polite to PubMed
    
    # Step 3: Create report
    report = create_report(posts_with_evidence)
    
    # Step 4: Save
    filename = f"report_{datetime.now().strftime('%Y%m%d')}.md"
    with open(filename, 'w') as f:
        f.write(report)
    
    print(f"Report saved: {filename}")
    print(f"Found {len(all_posts)} posts, verified {len(posts_with_evidence)}")

if __name__ == "__main__":
    main()
```

### How to Run This Weekly (Free Options)

**Option 1: GitHub Actions (100% Free, Cloud-Based)**
1. Create a GitHub repository
2. Add the script above as `weekly_research.py`
3. Create `.github/workflows/weekly.yml`:
```yaml
name: Weekly Research
on:
  schedule:
    - cron: '0 9 * * 0'  # Every Sunday at 9 AM
jobs:
  research:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run research
        run: |
          pip install feedparser requests
          python weekly_research.py
      - name: Commit results
        run: |
          git config user.name "Bot"
          git add .
          git commit -m "Weekly update" || echo "No changes"
          git push
```

**Option 2: Cron Job (Your Computer)**
```bash
# Edit crontab
crontab -e

# Add this line (runs every Sunday at 9 AM)
0 9 * * 0 cd /path/to/project && python3 weekly_research.py
```

**Option 3: Cursor Agent (Your Approach)**
1. Save the Python script
2. Create a Cursor rule: "Every Sunday, run weekly_research.py and save the output"
3. Let Cursor handle the automation

---

## The Minimal Manual Version (If You're Completely Broke)

If you can't code and don't want to learn, here's the absolute minimum manual process:

**Weekly Checklist (30 minutes):**

1. **Search Reddit** (5 min)
   - Visit https://www.reddit.com/r/longevity
   - Scan top posts from this week
   - Copy interesting claims to a Google Doc

2. **Verify on PubMed** (15 min)
   - Go to https://pubmed.ncbi.nlm.nih.gov/
   - For each claim, search for keywords
   - Open top 3 results
   - Read abstracts
   - Note: TRUE / FALSE / UNCLEAR

3. **Update Your Book** (10 min)
   - Open your book document
   - Add a new section for verified claims
   - Write: Claim → Verdict → Evidence → Link

4. **Repeat Weekly**
   - Set a calendar reminder
   - Do this every Sunday

**Cost:** $0  
**Time:** 30 min/week  
**Tools:** Browser + Google Docs + Calendar

---

## Summary: What You Need to Replicate My Process

1. **A way to get Reddit data** → RSS feeds (free, no auth)
2. **A way to search scientific literature** → PubMed API (free, no auth)
3. **A way to synthesize information** → ChatGPT / Claude / Cursor / Manual writing
4. **A way to run it regularly** → GitHub Actions / Cron / Manual reminder

That's it. Everything else is just optimization.
