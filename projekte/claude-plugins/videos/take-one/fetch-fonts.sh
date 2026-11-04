#!/bin/sh
# Lädt die Anthropic-Schriften von claude.com in assets/brand-fonts/ (nicht im Git: proprietäre Markenschriften).
set -e
cd "$(dirname "$0")"; mkdir -p assets/brand-fonts
B=https://claude.com/_next/static/media
for f in AnthropicSans_Roman_Web-s.p.050e7498 AnthropicSans_Italic_Web-s.p.6550bf15 AnthropicSerif_Roman_Web-s.p.c28786b4 AnthropicSerif_Italic_Web-s.p.43888cc6 AnthropicMono_Roman_Web-s.p.80d4607c; do
  [ -s "assets/brand-fonts/$f.woff2" ] || curl -sfL "$B/$f.woff2" -o "assets/brand-fonts/$f.woff2"
done
ls -la assets/brand-fonts
