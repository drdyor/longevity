# 🚀 How to Launch Your Dashboard

## Your Data is Ready!

You have **21 verified longevity claims** with PubMed evidence.

## To Launch the Dashboard:

### Option 1: From This Terminal
```bash
.venv/bin/streamlit run src/app.py
```

### Option 2: If You're in Your Regular Terminal
```bash
cd /workspace
streamlit run src/app.py
```

## What Opens:

A web page at `http://localhost:8501` with:

### 📊 Main Dashboard Features:

1. **Summary Metrics**
   - Total claims analyzed
   - Unique topics
   - Claims with strong evidence
   - Total Reddit score

2. **Interactive Filters** (sidebar)
   - Filter by topic (rapamycin, NAD+, metformin, etc.)
   - Filter by evidence level
   - Filter by direction (benefit/harm/neutral)
   - Search claims

3. **Three Tabs:**

   **📋 Claims List Tab:**
   - Expandable cards for each claim
   - Evidence level with emoji (✅ strong, 🟡 moderate, 🟠 weak, ❌ none)
   - Full explanation from PubMed analysis
   - Direct links to PubMed papers
   - Reddit score and comments

   **📊 Analytics Tab:**
   - Evidence distribution bar chart
   - Top topics bar chart
   - "Hype vs Evidence Gap" section
     Shows claims with high Reddit scores but weak evidence

   **📥 Export Tab:**
   - Download filtered data as CSV
   - Generate markdown report for your book
   - Export button with one click

## Your Results Preview:

Based on the data we just processed:
- **21 total claims** from 20 demo posts
- **9 with moderate support** (some scientific backing)
- **6 with weak support** (limited evidence)
- **6 with no clear support** (lacking research)

**Top topics:**
- Rapamycin (4 claims)
- GLP-1 agonists (3 claims)
- Spermidine, Metformin, NAD+, Exercise, and more

## Can't Launch Now?

View the raw data:
```bash
cat data/processed/claims_evidence_2025-11-23.csv
```

Or open in Excel/Google Sheets!

---

**Note:** The dashboard runs a local web server, so you need to run it in a terminal where you can access a web browser.
