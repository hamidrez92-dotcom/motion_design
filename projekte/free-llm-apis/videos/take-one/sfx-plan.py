#!/usr/bin/env python3
"""Effektplan aus denselben Zeiten wie film.html (skript.json). Schreibt audio/plan.json."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent
S = json.loads((ROOT.parent.parent / "skript" / "skript.json").read_text(encoding="utf-8"))
B = {b["id"]: b for b in S["beats"]}
FPS = 30
norm = lambda w: re.sub(r"[^\w]", "", w.lower())
def vt(i, a): return next(v["zeit"] for v in B[i]["visuals"] if v["anker"] == a)
def wt(i, w, n=0): return [x["zeit"] for x in B[i]["woerter"] if norm(x["wort"]).startswith(norm(w))][n]
st = lambda i: B[i]["start"]
cues = []
def cue(kind, t, variant=None, label="", **kw):
    c = {"kind": kind, "frame": max(1, round(t * FPS)), "label": label, **kw}
    if variant: c["variant"] = variant
    cues.append(c)

cue("pop", vt("B01", "GitHub-Repo") + .05, "cork", "GitHub-Zeichen")
cue("pop", wt("B01", "kaum") + .05, "tiny", "Fragezeichen")
cue("swish", vt("B02", "KI-Modelle") - .05, "in", "Rechnung")
cue("press", vt("B02", "Cent") + .05, "thock", "0,00 €")
cue("swish", vt("B03", "listet") - .1, "in", "Repo-Karte")
cue("chime", vt("B03", "500") + .1, "glint", "513+ markiert")
cue("swish", vt("B04", "Dauerhaft") - .1, "in", "Tabelle")
cue("press", vt("B04", "Testguthaben"), "soft", "✗ Testguthaben")
cue("press", vt("B05", "Kreditkarte"), "soft", "✗ Kreditkarte")
t0 = vt("B06", "heißt") - .1
for i in range(0, 20, 2): cue("tick", t0 + i / 20 * .9 + .03, "key", f"Taste {i}")
names = ["Google", "Nvidia", "Mistral", "Groq", "DeepSeek"]
for n in names: cue("pop", wt("B07", n) + .05, "pop", f"Logo {n}")
for i in range(5, 12, 2): cue("pop", vt("B07", "viele") + (i - 5) * .09 + .05, "tiny", f"Logo {i}")
cue("whoosh", st("B08") + .1, "soft", "Logos sammeln sich")
for n in ["Claude", "Cursor", "Codex"]: cue("swish", wt("B09", n) - .05, "soft", f"Ast {n}")
cue("swish", vt("B09", "Konfigurationen") - .1, "in", "Schnipsel")
cue("press", vt("B10", "Setup"), "soft", "✗ Setup"); cue("press", vt("B10", "Wühlen"), "soft", "✗ Dokus")
cue("swish", vt("B10", "Kopieren") - .1, "in", "Codex-Schnipsel")
cue("chime", wt("B10", "fertig") + .1, "glint", "Haken fertig")
cue("pop", vt("B11", "Limits") - .1, "cork", "Limit-Meldung")
cue("whoosh", vt("B11", "wechseln") + .1, "fast", "Anbieter wechseln")
cue("chime", vt("B12", "täglich") - .1, "bell", "Globus")
cue("tick", vt("B12", "neues") + .1, "ui", "neue Zeile")
cue("chime", vt("B12", "steht") + .1, "glint", "schon drin")
cue("riser", vt("B13", "Entscheidung"), "soft", "Aufbau", lengthS=1.4)
cue("impact", vt("B13", "Entscheidung") + .05, "soft", "Entscheidung")
cue("pop", vt("B14", "Speicher") + .4, "cork", "Lesezeichen")
cue("whoosh", vt("B14", "kennt") - .35, "soft", "zurück zum Anfang")
cues.sort(key=lambda c: c["frame"])
(ROOT / "audio" / "plan.json").write_text(json.dumps({"fps": FPS, "seed": 11, "key": "A", "bpm": 120, "cues": cues}, ensure_ascii=False, indent=1))
print(len(cues), "cues")
