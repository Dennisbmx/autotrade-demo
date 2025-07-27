#!/usr/bin/env bash
set -e
echo "🔧 Updating pip"
python -m pip install --upgrade pip

echo "🔧 Installing backend deps"
python -m pip install --no-cache-dir -r requirements.txt

echo "✅  Setup finished"