#!/bin/bash
# SDLC CLI Installation Script
# Usage: ./install-cli.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$HOME/.sdlcctl"

echo "🚀 Installing sdlcctl CLI..."

# Create virtual environment if not exists
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 Creating virtual environment at $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
fi

# Activate and install
echo "📥 Installing dependencies..."
source "$VENV_DIR/bin/activate"
pip install --upgrade pip -q
pip install -e "$SCRIPT_DIR" -q

# Create symlink in ~/.local/bin
mkdir -p "$HOME/.local/bin"
SYMLINK="$HOME/.local/bin/sdlcctl"

if [ -L "$SYMLINK" ]; then
    rm "$SYMLINK"
fi

ln -s "$VENV_DIR/bin/sdlcctl" "$SYMLINK"

echo ""
echo "✅ sdlcctl installed successfully!"
echo ""
echo "📍 Location: $SYMLINK"
echo ""

# Check if ~/.local/bin is in PATH
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo "⚠️  Add ~/.local/bin to your PATH:"
    echo ""
    echo "   echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.bashrc"
    echo "   source ~/.bashrc"
    echo ""
fi

echo "🎉 Run 'sdlcctl --help' to get started!"
