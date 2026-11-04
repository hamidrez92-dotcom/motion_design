# Vergleich: claude-plugins

Gleiche Eingabe für alle Skills: `skript/skript.json` (Stand: Commit mit QA 93/100, 79,9 s, geschätzte Wortzeiten bei 145 wpm), `quelle/`, **keine Aufnahme** (Hamid: „ohne meine Stimme, Texte als Untertitel“).

## Übersicht

| Skill | Datei | Länge | Render-Zeit | Iterationen | `om qa` / eigene Prüfung |
|---|---|---|---|---|---|
| huashu-motion 0.3.1 | `videos/huashu-motion/out/huashu-motion-v3.mp4` (9,5 MB, 1080×1920, 30 fps, AAC) | 80,5 s | ~3 min pro Render | 3 Renders, ~10 Still-Runden | 0 Fehler/Warnungen in `om check`; `om qa` ohne ✗ |

## huashu-motion

**Wie der Skill gearbeitet hat**
- Liest erst das Produkt: `om grab` holte Logo (Claude-Spark als SVG), Farben und Schriftnamen von claude.com und anthropic.com. Die Schriften (anthropicSans/Serif) sind nicht frei → Inter + EB Garamond.
- Der Skill verlangt drei Richtungen mit Keyframes und eine Rückfrage an den Nutzer. **Nicht gestellt**, weil Hamid gerade nicht verfügbar war; nach der Regel „just make it → A wählen, B/C anbieten“ selbst entschieden (`treatment.md`):
  - A (gebaut): kinetic-type + Karten im Anthropic-Look, Plugin-Leiste als Rückgrat.
  - B: Plugins als Karten im 3D-Studio. C: Flat-World-Büro mit Ausweis und Mappen.
- Musik: eingebaute Richtung `explainer` → Lo-fi, Es-Dur, ~90 BPM, Drop auf dem Payoff (68,2 s), 54 Effekte, −14,2 LUFS.
- Untertitel: kein eigenes Feature des Skills für stumme Untertitel aus einem Skript; gebaut als 1–4-Wort-Einblendungen aus den Wortzeiten von `skript.json`, aktives Wort im Akzent.
- Die eigenen Prüfwerkzeuge haben echte Fehler gefunden: doppelte ID, Kontrast des Spark-Orange als Schrift (3,0:1 → Text-Akzent #b4532f), „flat opening“ (Hook zu ruhig → Karten-Slams + Reißschwenk).
- Selbst gefunden beim Ansehen der Stills: Elemente vor ihrem Einsatz sichtbar (GSAP `immediateRender: false`), Mappe verdeckt Ausweis, Suchergebnisse im Untertitelband.

**Stärken**
- Sehr markentreu: echter Spark, Claude-Farben, ruhige Serif-Typografie. Wirkt wie von Anthropic.
- Alles ist Code und an das Skript gebunden: neue Skriptfassung oder echte Wortzeiten → `python3 tools/inject.py`, neu rendern, alle Einblendungen folgen.
- Bearbeitbar im Studio (`om studio`): Klick auf das Bild, Kommentar, gezielte Änderung.
- Gute Werkzeuge: `om check`, `om still`, `om qa`, `om sound` fangen viel ab.

**Schwächen / Beobachtungen**
- Viele Lesepausen ≥ 1 s (`om qa` listet 18): für ein Erklär-Reel mit Untertiteln okay, aber ruhiger als typische Reels.
- Ein Grund (Elfenbein) fast durchgehend; Kontrast kommt nur aus der dunklen „Grenze“-Szene und dem Payoff.
- Keine echte Plugin-Oberfläche, weil sie ohne Login nicht aufgenommen werden konnte; der Menüweg ist als beschriftete Schritte gezeigt, nicht als UI.
- Signatur „Made with huashu-motion“ in den letzten 1,2 s (abschaltbar).
- Musik ist nur über Spektrogramm und Lautheit geprüft, nicht angehört.

**Aufwand:** Skill gelesen (~1000 Zeilen Referenzen), ~600 Zeilen Komposition von Hand geschrieben. Ohne Erfahrung mit GSAP schwer selbst anzupassen; dafür ist das Studio da.

## Für den nächsten Skill
Gleiche Kriterien notieren: Markentreue, Lesbarkeit stumm, Rhythmus (`om qa`-ähnliche Messung oder Bild-für-Bild), Bindung an Wortzeiten, Rückfragen, Aufwand, Renderzeit.
