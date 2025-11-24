# 🧬 Reddit Longevity Evidence Agent

A free, open-source system that analyzes longevity claims from r/longevity and verifies them against scientific literature.

## 🎯 What This Does

1. **Collects** the last year of posts from r/longevity
2. **Extracts** specific longevity-related claims using AI
3. **Verifies** each claim against PubMed research
4. **Displays** results in an interactive dashboard

**Total Cost: $0** (100% free and runs locally)

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- 8GB+ RAM
- Reddit API credentials (free)

### 1. Clone & Install

```bash
git clone <your-repo-url>
cd longevity-reddit-agent
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
make install
```

### 2. Setup Reddit API

1. Go to https://www.reddit.com/prefs/apps
2. Click "create another app"
3. Choose "script" type
4. Set redirect URI to `http://localhost`
5. Copy your credentials

Create `.env` file:

```bash
cp .env.example .env
# Edit .env and add your Reddit credentials
```

### 3. Install Ollama (Local LLM)

```bash
make setup
# This installs Ollama and downloads the llama3:8b model (~5GB)
```

**Alternative:** If your laptop is slow, see [Cloud Options](#-cloud-deployment-free) below.

### 4. Run the Pipeline

```bash
make all
```

This will:
- Collect ~6,000 posts from r/longevity (5-10 min)
- Extract claims using local AI (30-60 min)
- Check evidence on PubMed (60-90 min)

### 5. View Dashboard

```bash
make dashboard
```

Opens interactive dashboard at `http://localhost:8501`

## 📁 Project Structure

```
longevity-reddit-agent/
├── README.md
├── requirements.txt
├── Makefile
├── .env.example
├── data/
│   ├── raw/              # Reddit posts (CSV)
│   ├── interim/          # Extracted claims (Parquet)
│   └── processed/        # Final evidence results (Parquet/CSV)
├── src/
│   ├── 01_collect.py     # Fetch Reddit posts
│   ├── 02_extract_claims.py  # Extract claims with LLM
│   ├── 03_evidence_check.py  # Verify against PubMed
│   ├── app.py            # Streamlit dashboard
│   └── utils/
│       ├── reddit.py     # Reddit API wrapper
│       ├── llm.py        # Ollama LLM utilities
│       └── pubmed.py     # PubMed search utilities
└── notebooks/
```

## 🎮 Usage

### Individual Steps

```bash
# Step 1: Collect posts
make collect

# Step 2: Extract claims
make extract

# Step 3: Check evidence
make evidence

# View dashboard
make dashboard
```

### Command Line

```bash
# Collect
python src/01_collect.py

# Extract claims
python src/02_extract_claims.py

# Check evidence
python src/03_evidence_check.py

# Dashboard
streamlit run src/app.py
```

## 📊 Dashboard Features

- **Filter by topic** (rapamycin, NAD+, metformin, etc.)
- **Filter by evidence level** (strong, moderate, weak, none)
- **Search claims** with full-text search
- **Analytics** showing hype vs evidence gaps
- **Export** to CSV or Markdown report
- **Direct PubMed links** for each claim

## ☁️ Cloud Deployment (Free)

If your laptop is too slow, use these free cloud options:

### Option 1: Google Colab (Recommended)

1. Upload the repo to Google Drive
2. Open `notebooks/colab_pipeline.ipynb` in Colab
3. Run all cells
4. Download results

### Option 2: GitHub Codespaces

1. Push to GitHub
2. Open in Codespaces (60 hours/month free)
3. Run `make all`

### Option 3: Fly.io

1. Install flyctl
2. Run `fly launch`
3. Deploy the Streamlit app for free

## 🔧 Configuration

Edit these in `.env`:

```bash
# Reddit
REDDIT_CLIENT_ID=your_id
REDDIT_CLIENT_SECRET=your_secret
REDDIT_USERNAME=your_username
REDDIT_PASSWORD=your_password

# Data directory (optional)
DATA_DIR=data

# LLM Model (optional)
OLLAMA_MODEL=llama3:8b
```

## 📈 Performance

**Local (16GB RAM, M1 Pro):**
- Collection: 5-10 minutes
- Claim extraction: 30-45 minutes
- Evidence check: 60-90 minutes

**Google Colab (Free GPU):**
- Collection: 5 minutes
- Claim extraction: 15-20 minutes
- Evidence check: 45-60 minutes

## 🎯 Use Cases

### For Research
- Identify gaps between public perception and science
- Find under-discussed but well-supported interventions
- Track emerging longevity trends

### For Writing
- Generate evidence tables for books/articles
- Find case studies and anecdotes
- Fact-check popular claims

### For Analysis
- Sentiment analysis of longevity communities
- Track dosing patterns mentioned on Reddit
- Compare hype vs evidence

## 🛠️ Troubleshooting

### Ollama not responding
```bash
# Start Ollama service
ollama serve

# Test it
ollama run llama3:8b "Hello"
```

### Reddit API errors
- Check credentials in `.env`
- Verify app type is "script" not "web"
- Ensure rate limits (60 req/min)

### Out of memory
- Use smaller model: `ollama pull llama3:8b-q4_0`
- Process in batches (edit MAX_POSTS in scripts)
- Use cloud option instead

### No claims extracted
- Verify Ollama is running: `ollama list`
- Check model is downloaded: `ollama pull llama3:8b`
- Try with verbose logging: `python -v src/02_extract_claims.py`

## 🔄 Keeping Data Fresh

### Manual Refresh
```bash
make all  # Run pipeline again
```

### Automated (GitHub Actions)

Create `.github/workflows/daily_refresh.yml`:

```yaml
name: Daily Data Refresh
on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight
  workflow_dispatch:

jobs:
  refresh:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: make install
      - run: make all
      - uses: actions/upload-artifact@v3
        with:
          name: evidence-data
          path: data/processed/
```

## 📝 Export Formats

The dashboard supports:

- **CSV** - For Excel, Pandas, R
- **Markdown** - For Notion, Obsidian, Jekyll
- **JSON** - For APIs, web apps
- **Parquet** - For data science tools

## 🤝 Contributing

Contributions welcome! Areas to improve:

- [ ] Add comment analysis (not just posts)
- [ ] Support more subreddits
- [ ] Better claim deduplication
- [ ] Dose/frequency extraction
- [ ] Sentiment analysis
- [ ] Multi-language support

## 📄 License

MIT License - feel free to use for your book, research, or commercial projects.

## 🙏 Credits

Built with:
- [PRAW](https://praw.readthedocs.io/) - Reddit API wrapper
- [Ollama](https://ollama.com/) - Local LLM inference
- [Streamlit](https://streamlit.io/) - Dashboard framework
- [NCBI E-utilities](https://www.ncbi.nlm.nih.gov/books/NBK25501/) - PubMed API

## 📧 Questions?

Open an issue or reach out at [your contact]

---

**Star this repo if you find it useful! ⭐**
