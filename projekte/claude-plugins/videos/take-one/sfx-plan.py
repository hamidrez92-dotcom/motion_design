#!/usr/bin/env python3
"""Effektplan für film.html, aus denselben Zeiten wie der Film (skript.json). Schreibt audio/plan.json.
Jeder Cue sitzt auf dem Frame seines sichtbaren Ereignisses (Landung, Klick, Stempel)."""
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

LAND = .32  # a 'heavy' spring is visually down after about a third of a second
slam = [0, .34, .68, 1.0, max(1.2, vt("B01", "Plugins"))]
for i, t in enumerate(slam): cue("pop" if i == 0 else "paper", t + LAND, "cork" if i == 0 else "slide", f"Mappe {i+1} landet")
cue("chime", wt("B01", "Claude") + .15, "glint", "Dann Claude.")
# cuts get only soft whooshes
for t, l in [(st("B02"), "Schnitt Laptop"), (st("B04"), "Schnitt Mappe"), (vt("B05", "Marketing"), "Schnitt Plugin-Reihe"),
             (st("B10"), "Schnitt Installation"), (st("B11"), "Schnitt Setup"), (st("B14"), "Schnitt Payoff")]:
    cue("whoosh", max(.1, t - .05), "soft", l)
cue("pop", wt("B02", "Claude") + .1, "tiny", "Antwort im Chat")
cue("paper", vt("B02", "Chatbot") + .12, "slide", "Zettel Chatbot")
cue("paper", vt("B02", "Mitarbeiter") - .25 + LAND, "slide", "Ausweis landet")
cue("paper", vt("B03", "Einarbeitungsmappe") - .35 + LAND, "slide", "Mappe Marketing")
cue("paper", st("B04") + .45, "flip", "Mappe klappt auf")
tP = vt("B04", "Plugin")
for i in range(3): cue("paper", tP + .15 + i * .28 + .18, "rustle" if i else "slide", f"Skill-Blatt {i+1}")
tc = wt("B04", "Verbindungen")
for i in range(3): cue("pop", tc + i * .16 + .5, "tiny", f"Connector {i+1}")
cue("press", vt("B04", "Job") + .05, "thock", "Stempel Ein Plugin")
# the row: a soft travel between stations
for i, n in [("B06", "Finance"), ("B07", "Legal"), ("B08", "Design"), ("B09", "Productivity")]:
    cue("swish", vt(i, n) - .1, "soft", f"Fahrt zu {n}")
tK = vt("B05", "Kampagnen")
for k in range(3): cue("ink", tK + .15 + k * .35, "plip", f"Post gestempelt {k+1}")
cue("paper", vt("B06", "Tabelle") - .25 + .35, "slide", "GuV-Blatt")
tCl = vt("B07", "Klauseln")
for k in range(3): cue("swish", tCl + k * .42 + .1, "in", f"Textmarker {k+1}")
tKI = vt("B08", "KI")
cue("paper", tKI - .55 + .2, "slide", "Zettel wirkt generisch"); cue("paper", tKI + .05 + .2, "slide", "Zettel schwer lesbar")
tA = vt("B09", "Aufgaben")
for k in range(3): cue("tick", tA + k * .32 + .12, "ui", f"Haken {k+1}")
tPr = wt("B09", "Projekte")
cue("paper", tPr - .55 + .25, "slide", "Karte Personen"); cue("paper", tPr - .25 + .25, "slide", "Karte Projekte")
# install
cue("paper", vt("B10", "zwei") + .4, "slide", "Zettel bezahlter Plan")
for t in [vt("B10", "Customize"), wt("B10", "Plugins"), wt("B10", "Discover")]: cue("press", t + .1, "soft", "Haken Menüweg")
tAn = vt("B10", "Anthropic")
cue("chime", tAn + .15, "glint", "by Anthropic bleibt")
# setup
cue("pop", vt("B11", "Prompt") + .05, "pop", "Setup-Prompt")
cue("pop", vt("B12", "Frage"), "tiny", "Frage 1"); cue("pop", vt("B12", "schreibst") - .15, "tiny", "Frage 2")
cue("paper", vt("B12", "Woche") - .5 + .3, "slide", "Block Prioritäten")
# the turn: quiet, one stamp
cue("press", vt("B13", "Anwalt") + .02, "thock", "Stempel Kein Anwalt", gainDb=3)
cue("paper", vt("B13", "Anwalt") + .55, "slide", "Zettel Anwalt fragen")
# payoff: the one riser, the one impact
cue("riser", wt("B14", "Fünf"), "soft", "Aufbau in den Payoff", lengthS=1.6)
cue("impact", wt("B14", "Fünf") + .05, "bloom", "5 Plugins")
cue("paper", wt("B14", "zwei") + .2, "slide", "2 Minuten"); cue("paper", wt("B14", "ein") + .2, "slide", "1 Prompt")
cue("paper", vt("B14", "Kollege") - .2 + LAND, "slide", "Ausweis auf dem Stapel")
cue("chime", vt("B14", "Kollege") + .35, "sparkle", "Kollege")
cue("swish", vt("B15", "Speicher") + .05, "in", "Lesezeichen")
cue("whoosh", vt("B15", "nächste Mal") - .45, "soft", "zurück zum Anfang")

cues.sort(key=lambda c: c["frame"])
plan = {"fps": FPS, "seed": 7, "key": "G", "bpm": 65.7, "cues": cues}
out = ROOT / "audio" / "plan.json"; out.write_text(json.dumps(plan, ensure_ascii=False, indent=1))
print(f"{len(cues)} cues -> {out}")
