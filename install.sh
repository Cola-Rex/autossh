#!/bin/bash

set -e

echo "🔧 Installing ausossh..."

INSTALL_DIR="/usr/local/bin"
BINARY_URL="https://github.com/Cola-Rex/autossh/releases/latest/download/autossh"
TARGET="$INSTALL_DIR/ausossh"

# Ensure curl exists
if ! command -v curl &> /dev/null; then
  echo "❌ curl is required but not installed."
  exit 1
fi

# Download binary
echo "⬇️  Downloading ausossh from: $BINARY_URL"
sudo curl -fsSL "$BINARY_URL" -o "$TARGET"
sudo chmod +x "$TARGET"

echo "✅ ausossh installed at: $TARGET"
echo ""
echo "📦 Example usage:"
echo "  ausossh -L 5433:remote-db:5432 user@remote-host"
echo ""
echo "🎉 All done!"
