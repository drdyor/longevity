#!/bin/bash
# Quick setup script for Mac

echo "🚀 Setting up Reddit Longevity Evidence Agent on your Mac..."
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.9+ first."
    exit 1
fi

echo "✓ Python3 found: $(python3 --version)"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv .venv

# Activate and install
echo "Installing dependencies..."
.venv/bin/pip install --upgrade pip -q
.venv/bin/pip install -r requirements.txt -q

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Install Ollama: https://ollama.com/download"
echo "2. Run: ollama pull llama3:8b"
echo "3. Launch dashboard: .venv/bin/streamlit run src/app.py"
echo ""
