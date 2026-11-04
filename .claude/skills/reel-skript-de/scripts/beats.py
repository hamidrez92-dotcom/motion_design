#!/usr/bin/env python3
"""Prüft ein Reel-Skript (skript.md) und schreibt skript.json + sprechtext.txt.

    python3 beats.py skript.md                    # Zeiten geschätzt (wpm)
    python3 beats.py skript.md --words voice.words.json   # Zeiten aus Aufnahme

voice.words.json: {"words": [{"word": "...", "start": s, "end": s}, ...]}
(Format von huashu-motion `om voice`; andere Tools lassen sich darauf umrechnen.)
Exit-Code 1, wenn es FEHLER gibt.
"""
import argparse
import difflib
import json
import re
import sys
import unicodedata
from pathlib import Path

ROLLEN = {"HOOK", "KONTEXT", "PUNKT", "WENDE", "PAYOFF", "CTA"}
TYPEN = {"chat", "zahl", "liste", "vergleich", "diagramm", "zitat", "logo",
         "screenshot", "text", "icon", "metapher", "ui"}
STOPP = set("""der die das den dem des ein eine einen einem einer eines und oder aber
nicht noch nur schon auch so wie was wer du dich dir dein deine ich mich mir es er sie
wir ihr ist sind war hat haben wird werden kann mit von zu zum zur im in an am auf aus
für bei nach vor über unter um als dass wenn dann da hier jetzt""".split())

PAUSE_SATZ = 0.20   # s nach . ! ?
PAUSE_BEAT = 0.15   # s zwischen Beats
MAX_HOOK_S = 4.0
MAX_BEAT_S = 8.0
MAX_LUECKE_S = 5.0
MAX_TEXT_WOERTER = 6
MAX_SATZ_WOERTER = 15


def norm(w):
    w = unicodedata.normalize("NFC", w.lower())
    return re.sub(r"[^\wäöüß]", "", w)


def sprechwoerter(text):
    """Wörter, wie sie gesprochen werden (Ziffern zählen länger)."""
    n = 0.0
    for tok in text.split():
        if re.search(r"\d", tok):
            digits = len(re.sub(r"\D", "", tok))
            n += 1 + 0.5 * max(0, digits - 1)
        elif norm(tok):
            n += 1
    return n


def lies_skript(pfad):
    raw = Path(pfad).read_text(encoding="utf-8")
    meta = {}
    m = re.match(r"^---\n(.*?)\n---\n", raw, re.S)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
        raw = raw[m.end():]
    beats = []
    for block in re.split(r"^## ", raw, flags=re.M)[1:]:
        lines = block.strip().splitlines()
        kopf = lines[0]
        hm = re.match(r"(B\d+)\s*[·\-–:]\s*([A-ZÄÖÜ]+)", kopf)
        beat = {"id": hm.group(1) if hm else kopf.split()[0],
                "rolle": hm.group(2) if hm else "?",
                "kopf": kopf, "sprech": "", "text": "", "visuals": []}
        for line in lines[1:]:
            line = line.strip()
            if line.startswith("SPRECH:"):
                beat["sprech"] = (beat["sprech"] + " " + line[7:].strip()).strip()
            elif line.startswith("TEXT:"):
                beat["text"] = line[5:].strip()
            elif line.startswith("VISUAL"):
                vm = re.match(r'VISUAL\s*(?:@(?:"([^"]+)"|(\S+)))?\s*(?:\[([^\]]+)\])?\s*:\s*(.*)', line)
                if vm:
                    anker = vm.group(1) or vm.group(2)
                    beat["visuals"].append({"anker": anker.rstrip(":") if anker else None,
                                            "typ": (vm.group(3) or "").strip().lower() or None,
                                            "beschreibung": vm.group(4).strip()})
                else:
                    beat.setdefault("_kaputt", []).append(line)
        beats.append(beat)
    return meta, beats


def finde_anker(anker, woerter):
    """Index des ersten Worts der Anker-Phrase in der Wortliste (normalisiert)."""
    ziel = [norm(a) for a in anker.split() if norm(a)]
    if not ziel:
        return None
    w = [norm(x) for x in woerter]
    for i in range(len(w) - len(ziel) + 1):
        if all(w[i + j] == ziel[j] or (j == len(ziel) - 1 and w[i + j].startswith(ziel[j]))
               for j in range(len(ziel))):
            return i
    return None


def schaetze_zeiten(beats, wpm):
    sek_pro_wort = 60.0 / wpm
    t = 0.0
    for b in beats:
        b["start"] = round(t, 2)
        wortzeiten = []
        for tok in b["sprech"].split():
            wortzeiten.append(round(t, 2))
            if re.search(r"\d", tok):
                t += sprechwoerter(tok) * sek_pro_wort
            elif norm(tok):
                t += sek_pro_wort
            if re.search(r"[.!?]$", tok):
                t += PAUSE_SATZ
        b["_wortzeiten"] = wortzeiten
        b["ende"] = round(t, 2)
        t += PAUSE_BEAT
    return "geschätzt"


def gemessene_zeiten(beats, words_path):
    data = json.loads(Path(words_path).read_text(encoding="utf-8"))
    gehoert = [w for w in data.get("words", []) if norm(w.get("word", ""))]
    h_norm = [norm(w["word"]) for w in gehoert]
    skript = []  # (beat_idx, wort_idx)
    s_norm = []
    for bi, b in enumerate(beats):
        b["_wortzeiten"] = [None] * len(b["sprech"].split())
        for wi, tok in enumerate(b["sprech"].split()):
            if norm(tok):
                skript.append((bi, wi))
                s_norm.append(norm(tok))
    sm = difflib.SequenceMatcher(a=s_norm, b=h_norm, autojunk=False)
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            bi, wi = skript[blk.a + k]
            beats[bi]["_wortzeiten"][wi] = round(gehoert[blk.b + k]["start"], 2)
    # Lücken: lineare Interpolation zwischen bekannten Nachbarn
    flach = [(bi, wi) for bi, b in enumerate(beats) for wi in range(len(b["_wortzeiten"]))]
    werte = [beats[bi]["_wortzeiten"][wi] for bi, wi in flach]
    bekannt = [i for i, v in enumerate(werte) if v is not None]
    if not bekannt:
        raise SystemExit("FEHLER: Kein Wort aus dem Skript in der Aufnahme gefunden.")
    for i, v in enumerate(werte):
        if v is None:
            links = max((k for k in bekannt if k < i), default=None)
            rechts = min((k for k in bekannt if k > i), default=None)
            if links is None:
                werte[i] = werte[rechts]
            elif rechts is None:
                werte[i] = werte[links]
            else:
                f = (i - links) / (rechts - links)
                werte[i] = round(werte[links] + f * (werte[rechts] - werte[links]), 2)
    for (bi, wi), v in zip(flach, werte):
        beats[bi]["_wortzeiten"][wi] = v
    letzte = gehoert[-1]["end"] if gehoert else werte[-1]
    for i, b in enumerate(beats):
        b["start"] = b["_wortzeiten"][0] if b["_wortzeiten"] else 0.0
    for i, b in enumerate(beats):
        b["ende"] = beats[i + 1]["start"] if i + 1 < len(beats) else round(letzte, 2)
    abdeckung = sum(blk.size for blk in sm.get_matching_blocks()) / max(1, len(s_norm))
    return f"gemessen ({abdeckung:.0%} der Wörter erkannt)"


def pruefe(meta, beats):
    fehler, warn = [], []
    if not beats:
        return ["Keine Beats gefunden (Überschriften müssen mit '## B01 · HOOK' beginnen)."], []
    if beats[0]["rolle"] != "HOOK":
        fehler.append(f"{beats[0]['id']}: Der erste Beat muss HOOK sein.")
    for b in beats:
        bid = b["id"]
        if b["rolle"] not in ROLLEN:
            fehler.append(f"{bid}: Unbekannte Rolle '{b['rolle']}' (erlaubt: {', '.join(sorted(ROLLEN))}).")
        if not b["sprech"]:
            fehler.append(f"{bid}: SPRECH fehlt.")
        for line in b.get("_kaputt", []):
            fehler.append(f"{bid}: VISUAL-Zeile nicht lesbar: {line}")
        if "{{" in b["sprech"] or "{{" in b["text"] or any("{{" in v["beschreibung"] for v in b["visuals"]):
            fehler.append(f"{bid}: Offener Platzhalter {{{{…}}}} — Fakt fehlt noch.")
        dauer = b["ende"] - b["start"]
        if b["rolle"] == "HOOK" and dauer > MAX_HOOK_S:
            warn.append(f"{bid}: Hook dauert {dauer:.1f} s (Ziel ≤ 3 s, max. 8 Wörter).")
        elif dauer > MAX_BEAT_S:
            warn.append(f"{bid}: Beat dauert {dauer:.1f} s — aufteilen (Ziel 3–8 s).")
        tw = len(b["text"].split())
        if tw > MAX_TEXT_WOERTER:
            warn.append(f"{bid}: TEXT hat {tw} Wörter (max. {MAX_TEXT_WOERTER}).")
        # Ein einzelnes Stichwort aus dem Sprechtext ist gewollt; ganze Satzteile nicht.
        if tw >= 3 and " ".join(map(norm, b["text"].split())) in " ".join(map(norm, b["sprech"].split())):
            warn.append(f"{bid}: TEXT wiederholt nur den Sprechtext — lieber das Stichwort.")
        for satz in re.split(r"(?<=[.!?])\s+", b["sprech"]):
            n = len([w for w in satz.split() if norm(w)])
            if n > MAX_SATZ_WOERTER:
                warn.append(f"{bid}: Satz mit {n} Wörtern — zum Sprechen kürzen: „{satz[:60]}…“")
        if re.search(r"[—–]|\(|\)|/|;", b["sprech"]):
            warn.append(f"{bid}: Gedankenstrich, Klammer, Schrägstrich oder Semikolon im Sprechtext — so spricht niemand.")
        if not b["visuals"]:
            warn.append(f"{bid}: Kein VISUAL.")
        woerter = b["sprech"].split()
        for v in b["visuals"]:
            if v["typ"] and v["typ"] not in TYPEN:
                warn.append(f"{bid}: Unbekannter Visual-Typ [{v['typ']}] (bekannt: {', '.join(sorted(TYPEN))}).")
            if v["anker"]:
                idx = finde_anker(v["anker"], woerter)
                if idx is None:
                    fehler.append(f"{bid}: Anker @{v['anker']} kommt im SPRECH nicht vor.")
                    v["zeit"] = b["start"]
                else:
                    v["wort_index"] = idx
                    v["zeit"] = b["_wortzeiten"][idx]
            else:
                v["zeit"] = b["start"]
    # Lücken zwischen Visuals
    zeiten = sorted([v["zeit"] for b in beats for v in b["visuals"]] + [beats[-1]["ende"]])
    vorher = 0.0
    for z in zeiten:
        if z - vorher > MAX_LUECKE_S:
            warn.append(f"{vorher:5.1f}–{z:5.1f} s: {z - vorher:.1f} s ohne neues Visual (Ziel ≤ {MAX_LUECKE_S:.0f} s).")
        vorher = z
    # Gesamtdauer
    gesamt = beats[-1]["ende"]
    if gesamt < 55 or gesamt > 95:
        fehler.append(f"Gesamtdauer {gesamt:.0f} s — Ziel 60–90 s.")
    elif gesamt < 60 or gesamt > 90:
        warn.append(f"Gesamtdauer {gesamt:.0f} s — knapp außerhalb 60–90 s.")
    ziel = meta.get("zieldauer")
    if ziel and ziel.replace(".", "").isdigit() and abs(gesamt - float(ziel)) > 10:
        warn.append(f"Gesamtdauer {gesamt:.0f} s weicht > 10 s von zieldauer {ziel} s ab.")
    # Loop
    hook = {norm(w) for w in beats[0]["sprech"].split()} - STOPP - {""}
    schluss = {norm(w) for w in beats[-1]["sprech"].split()} - STOPP - {""}
    if not hook & schluss:
        warn.append("Kein Loop: Der letzte Beat greift kein Wort aus dem Hook auf.")
    rollen = [b["rolle"] for b in beats]
    if "PAYOFF" not in rollen:
        warn.append("Kein PAYOFF-Beat — die Kernaussage wird nicht ausgesprochen.")
    punkte = rollen.count("PUNKT")
    if punkte < 2:
        warn.append(f"Nur {punkte} PUNKT-Beat(s) — für 60–90 s sind 2–3 Kernpunkte üblich.")
    return fehler, warn


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("skript")
    ap.add_argument("--words", help="Wortzeiten aus der Aufnahme (voice.words.json)")
    ap.add_argument("--wpm", type=float, help="Sprechtempo für die Schätzung (Default: aus Frontmatter oder 145)")
    ap.add_argument("--out-dir", help="Zielordner für skript.json und sprechtext.txt (Default: neben skript.md)")
    args = ap.parse_args()

    meta, beats = lies_skript(args.skript)
    wpm = args.wpm or float(meta.get("wpm", 145) or 145)
    if not beats:
        print("FEHLER  Keine Beats gefunden.")
        sys.exit(1)
    quelle = gemessene_zeiten(beats, args.words) if args.words else schaetze_zeiten(beats, wpm)
    fehler, warn = pruefe(meta, beats)

    gesamt = beats[-1]["ende"]
    woerter = int(sum(len([w for w in b["sprech"].split() if norm(w)]) for b in beats))
    print(f"{meta.get('titel', Path(args.skript).stem)} — {gesamt:.1f} s, {woerter} Wörter, Zeiten {quelle}"
          + ("" if args.words else f" bei {wpm:.0f} wpm"))
    print()
    for b in beats:
        print(f"{b['start']:5.1f}–{b['ende']:5.1f}  {b['id']} {b['rolle']:<8} {b['sprech'][:70]}{'…' if len(b['sprech']) > 70 else ''}")
        if b["text"]:
            print(f"{'':13}TEXT  {b['text']}")
        for v in b["visuals"]:
            anker = f"@{v['anker']}" if v["anker"] else "@Beat"
            print(f"{'':6}{v.get('zeit', b['start']):5.1f}  ▸ {anker} [{v['typ'] or '-'}] {v['beschreibung'][:60]}")
    print()
    for f in fehler:
        print(f"FEHLER   {f}")
    for w in warn:
        print(f"WARNUNG  {w}")
    if not fehler and not warn:
        print("OK — keine Fehler, keine Warnungen.")

    out_dir = Path(args.out_dir) if args.out_dir else Path(args.skript).parent
    out_dir.mkdir(parents=True, exist_ok=True)
    export = {
        "titel": meta.get("titel"),
        "quelle": meta.get("quelle"),
        "zeiten": quelle,
        "wpm": None if args.words else wpm,
        "dauer": round(gesamt, 2),
        "format": {"breite": 1080, "hoehe": 1920, "safe_zone": {"oben": 230, "unten": 1440, "rechts": 230}},
        "beats": [{
            "id": b["id"], "rolle": b["rolle"], "start": b["start"], "ende": b["ende"],
            "sprech": b["sprech"], "text": b["text"] or None,
            "visuals": [{"zeit": v.get("zeit"), "anker": v["anker"], "typ": v["typ"],
                         "beschreibung": v["beschreibung"]} for v in b["visuals"]],
        } for b in beats],
    }
    (out_dir / "skript.json").write_text(json.dumps(export, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    saetze = []
    for b in beats:
        saetze += [s.strip() for s in re.split(r"(?<=[.!?])\s+", b["sprech"]) if s.strip()]
    (out_dir / "sprechtext.txt").write_text("\n".join(saetze) + "\n", encoding="utf-8")
    print(f"\n→ {out_dir / 'skript.json'}\n→ {out_dir / 'sprechtext.txt'}")
    sys.exit(1 if fehler else 0)


if __name__ == "__main__":
    main()
