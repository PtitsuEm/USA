#!/usr/bin/env bash
set -e

# Change directory to the root of the repository
cd "$(dirname "$0")"

echo "=========================================================="
echo "    U.S. Public Officials & Economic Leadership System    "
echo "=========================================================="
echo ""

# Check for required tools
if ! command -v node &> /dev/null; then
    echo "❌ Error: Node.js is not installed."
    echo "Please install Node.js 18+ to run the Next.js web application."
    echo ""
    echo "Alternative: You can open dist/index.html in any browser directly!"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo "❌ Error: npm is not installed. Please install npm."
    exit 1
fi

# Initialize SQLite database if missing
if [ ! -f "data/officials.db" ]; then
    if command -v python3 &> /dev/null; then
        echo "📦 Initializing SQLite database (data/officials.db)..."
        python3 scripts/init_db.py
    fi
fi

# Build offline dist if missing
if [ ! -f "dist/index.html" ]; then
    if command -v python3 &> /dev/null; then
        echo "📦 Building standalone offline index (dist/index.html)..."
        python3 scripts/build.py
    fi
fi

# Check if site dependencies are installed
if [ ! -d "site/node_modules" ]; then
    echo "📥 Installing dependencies in ./site..."
    (cd site && npm install)
fi

echo ""
echo "🚀 Starting Next.js web portal on http://localhost:3000"
echo "Press Ctrl+C to stop the server."
echo ""

cd site && npm run dev
