#!/usr/bin/env bash
set -e

poetry install
cp .env.example .env
cat <<MSG
Dependencies installed. Edit .env with your API keys (OPENAI_API_KEY, FINANCIAL_DATASETS_API_KEY, ALPACA_API_KEY, etc.)
Then run: poetry run python src/main.py --ticker AAPL
MSG
