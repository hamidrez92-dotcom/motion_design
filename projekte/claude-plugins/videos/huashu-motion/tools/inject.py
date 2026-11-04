#!/usr/bin/env python3
"""Bettet ../../skript/skript.json in index.html ein (zwischen den skript-Tags).

    python3 tools/inject.py            # aus dem Projektordner
Danach `om check` / `om render`. So folgt der Film jeder neuen Skriptfassung
(oder den echten Wortzeiten nach `beats.py --words`).
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKRIPT = ROOT.parent.parent / "skript" / "skript.json"
html = (ROOT / "index.html").read_text(encoding="utf-8")
data = json.dumps(json.loads(SKRIPT.read_text(encoding="utf-8")), ensure_ascii=False).replace("</", "<\\/")
new, n = re.subn(r'(<script type="application/json" id="skript">)(.*?)(</script>)',
                 lambda m: m.group(1) + data + m.group(3), html, flags=re.S)
if n != 1:
    raise SystemExit("skript-Tag nicht gefunden")
(ROOT / "index.html").write_text(new, encoding="utf-8")
print(f"skript.json eingebettet ({len(data)} Zeichen)")
