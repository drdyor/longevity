.PHONY: help install setup collect extract evidence dashboard all clean

help:
	@echo "Reddit Longevity Evidence Agent - Commands:"
	@echo ""
	@echo "  make install    - Install Python dependencies"
	@echo "  make setup      - Setup Ollama and pull model"
	@echo "  make collect    - Collect Reddit posts"
	@echo "  make extract    - Extract claims from posts"
	@echo "  make evidence   - Check claims against PubMed"
	@echo "  make dashboard  - Launch Streamlit dashboard"
	@echo "  make all        - Run full pipeline (collect -> extract -> evidence)"
	@echo "  make clean      - Clean generated data files"
	@echo ""

install:
	pip install -r requirements.txt

setup:
	@echo "Installing Ollama..."
	@if ! command -v ollama &> /dev/null; then \
		curl -fsSL https://ollama.com/install.sh | sh; \
	else \
		echo "Ollama already installed"; \
	fi
	@echo "Pulling llama3.2:3b model..."
	ollama pull llama3.2:3b

collect:
	python src/01_collect.py

extract:
	python src/02_extract_claims.py

evidence:
	python src/03_evidence_check.py

dashboard:
	streamlit run src/app.py

all: collect extract evidence
	@echo ""
	@echo "✓ Pipeline complete! Run 'make dashboard' to view results."

clean:
	rm -f data/raw/*.csv
	rm -f data/interim/*.parquet
	rm -f data/processed/*.parquet
	rm -f data/processed/*.csv
