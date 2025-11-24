# GitHub Actions Workflows

## `daily_refresh.yml` - Pipeline Validation

**What it does:**
- ✅ Validates project structure on every push
- ✅ Tests demo data generation
- ✅ Ensures code runs without errors

**What it doesn't do:**
- ❌ Run full LLM inference (too resource-intensive for CI)
- ❌ Process real Reddit data (no API credentials in CI)
- ❌ Run PubMed evidence checking (takes 60+ minutes)

## Why Not Run the Full Pipeline in CI?

1. **Ollama in CI is problematic** - Requires GPU, large downloads, background service
2. **Long runtime** - Full pipeline takes 90+ minutes (CI has timeouts)
3. **API rate limits** - PubMed might rate-limit GitHub's IPs
4. **No credentials** - Reddit API needs private credentials

## For Full Pipeline Updates:

**Run locally or on a scheduled server:**

```bash
# On your machine or a cloud VM
make all
git add data/
git commit -m "Update evidence data"
git push
```

**Or use GitHub Actions with cloud LLM:**
- Replace Ollama with OpenAI/Anthropic API
- Add API keys as GitHub Secrets
- Would cost ~$5-10/month but runs reliably in CI

