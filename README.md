# AutoTrade Demo

This project showcases a tiny automated trading dashboard with a FastAPI backend and optional Telegram bot. Prices come from Alpaca when API keys are provided, otherwise yfinance is used.

## Setup
1. Create and activate a Python virtual environment.
2. Copy `.env.sample` to `.env` and add your API keys.
3. Run `./setup_script.sh` to install dependencies.
4. Start the application with a single command:

```bash
python -m venv .venv && source .venv/bin/activate && \
pip install -r requirements.txt && python -m autotrade.run_all
```

Preview port 8000 in your browser to see the dashboard.
