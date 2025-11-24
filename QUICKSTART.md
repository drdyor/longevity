# 🚀 Quick Start Guide

Get up and running in 15 minutes.

## Step-by-Step Setup

### 1. Get Reddit API Credentials (2 minutes)

1. Go to: https://www.reddit.com/prefs/apps
2. Scroll down and click **"create another app"**
3. Fill in:
   - **name:** `longevity-agent`
   - **type:** Select **"script"**
   - **description:** (optional)
   - **about url:** (leave blank)
   - **redirect uri:** `http://localhost`
4. Click **"create app"**
5. Note down:
   - **client_id** (under the app name)
   - **client_secret** (next to "secret")

### 2. Install Dependencies (3 minutes)

```bash
# Clone the repo (or you're already in it)
cd longevity-reddit-agent

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 3. Configure Environment (1 minute)

```bash
# Copy example file
cp .env.example .env

# Edit .env with your credentials
# Use nano, vim, or any text editor:
nano .env
```

Add your Reddit credentials:

```bash
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
REDDIT_USERNAME=your_reddit_username
REDDIT_PASSWORD=your_reddit_password
REDDIT_USER_AGENT=longevity-agent by u/your_username
```

Save and exit.

### 4. Install Ollama (5 minutes)

**Mac/Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3:8b
```

**Windows:**
1. Download from: https://ollama.com/download
2. Install and run
3. Open PowerShell and run: `ollama pull llama3:8b`

**Test it:**
```bash
ollama run llama3:8b "Hello"
```

If you see a response, you're good!

### 5. Run the Pipeline (90 minutes total, mostly automated)

```bash
# Collect Reddit posts (5-10 min)
python src/01_collect.py

# Extract claims (30-60 min - grab a coffee ☕)
python src/02_extract_claims.py

# Check evidence (60-90 min - grab lunch 🍕)
python src/03_evidence_check.py
```

**Or run all at once:**
```bash
make all
```

### 6. Launch Dashboard (instant)

```bash
streamlit run src/app.py
```

Opens in your browser at `http://localhost:8501`

## 🎉 You're Done!

Now you can:
- Filter claims by topic (rapamycin, NAD+, etc.)
- See evidence ratings from PubMed
- Export to CSV or Markdown
- Find the biggest hype-vs-evidence gaps

## ⚡ Too Slow? Use Cloud (Free)

If your laptop is struggling:

### Option A: Google Colab (Easiest)

1. Create a new notebook at colab.research.google.com
2. Copy this cell:

```python
# Install everything
!git clone https://github.com/yourname/longevity-reddit-agent.git
%cd longevity-reddit-agent
!pip install -q -r requirements.txt
!curl -fsSL https://ollama.com/install.sh | sh
!ollama pull llama3:8b

# Set credentials (replace with yours)
import os
os.environ["REDDIT_CLIENT_ID"] = "your_id"
os.environ["REDDIT_CLIENT_SECRET"] = "your_secret"
os.environ["REDDIT_USERNAME"] = "your_username"
os.environ["REDDIT_PASSWORD"] = "your_password"
os.environ["REDDIT_USER_AGENT"] = "longevity-agent by u/your_username"

# Run pipeline
!python src/01_collect.py
!python src/02_extract_claims.py
!python src/03_evidence_check.py

# Download results
from google.colab import files
files.download('data/processed/claims_evidence_*.csv')
```

3. Run it (90 min total, you can close the tab)
4. Download the CSV when done

### Option B: Cursor (AI-Assisted)

If you're using Cursor:

1. Open this project in Cursor
2. Ask: "Run the full pipeline for me"
3. It will execute all steps automatically

## 🐛 Troubleshooting

### "No module named 'praw'"
```bash
# Make sure virtual environment is activated
source .venv/bin/activate
pip install -r requirements.txt
```

### "connection refused" when running extract_claims
```bash
# Ollama isn't running
ollama serve  # In one terminal
# Then run the script in another terminal
```

### "Invalid credentials" from Reddit
- Double-check your `.env` file
- Make sure app type is "script" not "web app"
- Ensure no spaces in credentials

### Out of memory
```bash
# Use smaller model
ollama pull llama3:8b-q4_0

# Or edit the scripts to process fewer posts:
# In src/01_collect.py, change MAX_POSTS to 1000
```

## 💡 Tips

1. **Start small**: Test with 100 posts first (edit `MAX_POSTS` in `01_collect.py`)
2. **Run overnight**: The evidence check takes time, let it run while you sleep
3. **Save checkpoints**: Each step saves progress, you can stop and resume
4. **Check logs**: If something fails, read the error messages carefully

## 📧 Still Stuck?

Open an issue on GitHub with:
- The command you ran
- The full error message
- Your OS and Python version (`python --version`)

---

**Next:** Check out the full [README.md](README.md) for advanced usage!
