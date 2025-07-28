# AutoTrade Demo

This demo includes a FastAPI web server and optional Telegram bot. Install dependencies with the provided setup script and run the combined server.

## Setup

1. Create a Python virtualenv and activate it.
2. Copy `.env.sample` to `.env` and fill in your API keys.
3. Run `./setup_script.sh` to install packages. If you have a directory `./wheels` with prebuilt packages, set `USE_LOCAL_WHEELS=true` in the environment settings so the script installs from that directory.
4. Start the app:

```bash
source .venv/bin/activate
python -m autotrade.run_all
```

Open your browser to port 8000 to view the dashboard.
