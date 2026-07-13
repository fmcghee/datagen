#!/usr/bin/env bash
# Clone the ES POV Obsidian vault as a standalone git repo (valid for Obsidian Git).
set -euo pipefail

TARGET="${1:-$HOME/Obsidian/es-pov-customer-demo}"
REPO="${VAULT_REPO:-https://github.com/fmcghee/datagen.git}"
BRANCH="${VAULT_BRANCH:-obsidian-vault}"

if [[ -d "$TARGET/.git" ]]; then
  echo "Vault already exists at $TARGET"
  echo "Open this folder in Obsidian: $TARGET"
  exit 0
fi

if [[ -e "$TARGET" ]]; then
  echo "Error: $TARGET exists but is not a git repo. Remove it or choose another path."
  exit 1
fi

mkdir -p "$(dirname "$TARGET")"
git clone --branch "$BRANCH" --single-branch "$REPO" "$TARGET"

echo ""
echo "Vault ready. In Obsidian:"
echo "  Open folder as vault -> $TARGET"
echo "  Start note: ES POV Customer Demo Guide.md"
