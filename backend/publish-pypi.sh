#!/bin/bash
# Publish sdlcctl to PyPI
# Usage: ./publish-pypi.sh [test|prod]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

VENV_DIR="$HOME/.sdlcctl"

# Ensure virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Activate venv
source "$VENV_DIR/bin/activate"

# Check if twine is installed
if ! command -v twine &> /dev/null; then
    echo "📦 Installing twine and build..."
    pip install --upgrade pip
    pip install twine build
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info/

# Build package
echo "📦 Building package..."
python -m build

# Check the package
echo "🔍 Checking package..."
twine check dist/*

# Publish
if [ "$1" == "test" ]; then
    echo "🚀 Publishing to TestPyPI..."
    twine upload --repository testpypi dist/*
    echo ""
    echo "✅ Published to TestPyPI!"
    echo "📦 Install with: pip install -i https://test.pypi.org/simple/ sdlcctl"
elif [ "$1" == "prod" ]; then
    echo "🚀 Publishing to PyPI..."
    twine upload dist/*
    echo ""
    echo "✅ Published to PyPI!"
    echo "📦 Install with: pip install sdlcctl"
else
    echo ""
    echo "📦 Package built successfully!"
    echo ""
    echo "To publish:"
    echo "  ./publish-pypi.sh test   # Publish to TestPyPI first"
    echo "  ./publish-pypi.sh prod   # Publish to production PyPI"
    echo ""
    echo "Built files:"
    ls -la dist/
fi
