# 🎯 Running This in Cursor

Since you're already in Cursor, here's how to run the entire pipeline.

## ✅ What's Already Done

The complete project has been created with all files in place. You're ready to run!

## 📋 Step-by-Step in Cursor

### Step 1: Setup Reddit API Credentials (2 minutes)

1. Open browser → https://www.reddit.com/prefs/apps
2. Click "create another app"
3. Choose "script" type
4. Set redirect to `http://localhost`
5. Copy your `client_id` and `client_secret`

### Step 2: Configure Environment

In Cursor's terminal (or ask Cursor to do this):

```bash
# Copy environment template
cp .env.example .env

# Edit .env file
# Replace these values with your actual Reddit credentials:
# REDDIT_CLIENT_ID=your_actual_id
# REDDIT_CLIENT_SECRET=your_actual_secret
# REDDIT_USERNAME=your_reddit_username
# REDDIT_PASSWORD=your_reddit_password
```

### Step 3: Install Dependencies

In Cursor's terminal:

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install Python packages
pip install -r requirements.txt
```

### Step 4: Install Ollama (Local LLM)

**Option A - Fast (if you have good internet):**

In Cursor's terminal:

```bash
# Mac/Linux
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3:8b

# Windows: Download from https://ollama.com/download
# Then run: ollama pull llama3:8b
```

**Option B - Ask Cursor:**

Just ask Cursor in chat:
> "Install Ollama and pull the llama3:8b model"

Cursor will handle it automatically.

### Step 5: Run the Pipeline

**Option A - All at once:**

```bash
make all
```

This runs all 3 steps:
- Collect posts (5-10 min)
- Extract claims (30-60 min)  
- Check evidence (60-90 min)

**Option B - Step by step:**

```bash
# Step 1: Collect Reddit posts
python src/01_collect.py

# Step 2: Extract claims
python src/02_extract_claims.py

# Step 3: Check evidence
python src/03_evidence_check.py
```

**Option C - Ask Cursor:**

Just ask Cursor:
> "Run the full pipeline: collect, extract claims, and check evidence"

Cursor will execute all steps for you.

### Step 6: View Results

```bash
make dashboard
```

Or:

```bash
streamlit run src/app.py
```

Opens dashboard at `http://localhost:8501`

## 🤖 Using Cursor as Your Assistant

You can ask Cursor to do ANY of these tasks:

### Example Commands:

**Setup:**
> "Set up my .env file with Reddit credentials"

**Running:**
> "Run the data collection script"
> "Extract claims from the posts"
> "Check all claims against PubMed"

**Debugging:**
> "Why is Ollama not responding?"
> "The Reddit API is giving an error, help me debug"

**Analysis:**
> "Show me the top 10 most hyped but least supported claims"
> "Export claims about rapamycin to CSV"
> "Generate a markdown report for my book"

**Customization:**
> "Modify the script to only collect posts from the last 6 months"
> "Add a new filter to the dashboard for 'study type'"
> "Change the evidence categories to include 'conflicting'"

## ⚡ Cloud Option (If Your Laptop is Slow)

If running locally is too slow, you have 2 options:

### Option 1: Google Colab

1. Upload `notebooks/colab_pipeline.ipynb` to Google Colab
2. Add your Reddit credentials in the notebook
3. Run all cells
4. Download results

Ask Cursor:
> "Prepare the Colab notebook for me with my credentials"

### Option 2: GitHub Codespaces

1. Push this repo to GitHub
2. Open in Codespaces (60 hrs/month free)
3. Run the pipeline there

Ask Cursor:
> "Push this to GitHub and set up Codespaces"

## 📊 What Happens Next

### During Collection (5-10 min):
```
Fetching posts from r/longevity...
  Fetched 100 posts...
  Fetched 200 posts...
  ...
✓ Fetched 6214 posts
```

### During Claim Extraction (30-60 min):
```
Extracting claims...
  Progress: 100/6214 posts processed (187 claims found)
  Progress: 200/6214 posts processed (398 claims found)
  ...
✓ Extracted 11847 claims
```

### During Evidence Check (60-90 min):
```
Checking evidence...
  Progress: 100/11847 (0.8%)
  Progress: 200/11847 (1.7%)
  ...
✓ Checked 11847 claims
```

### Dashboard Launch (instant):
```
You can now view your Streamlit app in your browser.
  Local URL: http://localhost:8501
```

## 🎯 Expected Output Files

After running, you'll have:

```
data/
├── raw/
│   └── posts_2024-11-23.csv           (~6,000 posts)
├── interim/
│   └── claims_2024-11-23.parquet      (~12,000 claims)
└── processed/
    ├── claims_evidence_2024-11-23.parquet
    └── claims_evidence_2024-11-23.csv  (~12,000 verified claims)
```

## 🐛 Troubleshooting in Cursor

### Issue: "Ollama not found"

Ask Cursor:
> "Ollama isn't working, help me install it"

Or manually:
```bash
# Check if installed
ollama --version

# Install if missing
curl -fsSL https://ollama.com/install.sh | sh
```

### Issue: "Reddit API error"

Ask Cursor:
> "Check my .env file for Reddit credentials"

Or manually:
```bash
# Verify .env has correct values
cat .env

# Test Reddit connection
python -c "from src.utils.reddit import get_reddit_client; print(get_reddit_client().user.me())"
```

### Issue: "Out of memory"

Ask Cursor:
> "I'm running out of memory, what can I do?"

Cursor will suggest:
- Use smaller model: `ollama pull llama3:8b-q4_0`
- Process fewer posts at once
- Use cloud option instead

## 💡 Advanced Usage

### Customize Data Collection

Ask Cursor:
> "Change the collection to only get posts with 50+ upvotes"

### Add New Topics

Ask Cursor:
> "Add 'senolytics' as a topic category in the claim extraction"

### Export Custom Reports

Ask Cursor:
> "Generate a report showing only strong evidence claims about supplements"

### Automate Refresh

Ask Cursor:
> "Set up a daily cron job to refresh the data"

## 🎓 Learning Opportunity

As you run this, you'll learn:

1. **API Integration** - How to work with Reddit & PubMed APIs
2. **LLM Applications** - Using local models for structured extraction
3. **Data Pipelines** - Building reproducible ETL workflows
4. **Web Dashboards** - Creating interactive visualizations

Ask Cursor to explain any part you don't understand!

## 🚀 You're Ready!

**Next steps:**

1. Set up `.env` with Reddit credentials (2 min)
2. Run `make install && make setup` (5 min)
3. Run `make all` (90 min, automated)
4. Run `make dashboard` (instant)
5. Explore your data!

**Or just ask Cursor:**
> "Set everything up and run the pipeline for me"

And Cursor will do it all automatically.

---

**See also:**
- [QUICKSTART.md](QUICKSTART.md) - Manual setup steps
- [WHAT_YOU_GET.md](WHAT_YOU_GET.md) - Preview of results
- [README.md](README.md) - Full documentation
