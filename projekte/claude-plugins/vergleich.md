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

## take-one 0.1.0

`videos/take-one/out/claude-plugins.mp4` (25 MB, 1080×1920, 30 fps, AAC) · 80,5 s · ~7 min pro Render (3 parallele Chrome) · 4 Renders · ~2,5 h insgesamt.

**Wie der Skill gearbeitet hat**
- Arbeitet wie ein Studio mit zwölf Rollen und harten Prüfungen. Hält bei einem „Run“ an zwei Stellen an (Run oder Etappen, Pitch mit Route und Kosten). **Beide nicht gestellt**: Hamid hatte „mach weiter“ gesagt, angenommen wurde *Run, nur Code, kostenlos, keine Stimme* (`videos/take-one/DIRECTION.md`). Der Skill hätte zuerst die bezahlte Route gepitcht (echte Plugin-Oberfläche per Login aufnehmen, Bilder per Bildmodell, ein gesungener Song).
- Brand-Pass vom Live-Site: **echte Anthropic-Schriften** (anthropicSans/Serif/Mono, lokal, nicht im Git) und die gemessenen Farben (#e3dacc als Grund). huashu-motion hatte Ersatzschriften genommen.
- Art Direction nach einer Bann-Liste gegen den „KI-Look“ (keine schwebenden Karten, Pillen, Chips, kein Karaoke). Gewählt: **eine Welt, ein Schreibtisch unter einer Lampe** – Ausweis, Mappen, Laptop, Stoppuhr, Papiere; jede Aussage ein Ereignis auf dem Tisch.
- Film als Canvas, `renderFrame(t)`, Springs, Kamera über die Welt. Musik aus der eigenen Code-Engine (Klavier + Streicher, auf 80,5 s gefittet), 61 synthetische Effekte auf den Frame genau.
- Prüfungen, die echte Fehler gefunden haben: **Text-Audit** (24 Fehler: zu kleine Beschriftungen fürs Handy, Untertitel-Wörter < 0,6 s sichtbar, überlappende Texte, ein Bug, der Chatblasen verschwinden ließ), **Gate** (Stillstand: Kamera parkte; Sprünge bei Untertitelwechseln), **frischer Reviewer** (zwei Runden, je ein neuer Agent ohne Vorwissen).

**Ergebnis der Reviews:** Runde 1: **6/10 RETURN** (Untertitel überlappen beim Wechsel, Dinge am Rand angeschnitten, fünfmal dieselbe Mappe, statischer Laptop). Nach Korrektur Runde 2: **6/10 RETURN** (bessere Untertitel, aber: Plugin-Liste wirkt weiter wie Schablone, Laptop-Strecke 50–61 s tot, Menüweg als Zettel statt als Oberfläche, viel leerer Raum unten). Laut Skill sind zwei gleiche Runden die Decke dieser Route; die Hebel wären die echte Oberfläche und mehr Ideen pro Plugin. Ausgeliefert mit dieser Punktzahl. Gate am Ende 7/7, vier Grenzfall-Sprünge (3,0–4,1×) als Treffer bzw. Untertitel-Ausgänge deklariert.

**Stärken**
- Die eigenständigste Bildidee: Schreibtisch, Licht, Schatten, echte Markenschrift. Wirkt nicht wie Template-Motion-Design.
- Die strengsten Prüfwerkzeuge; der fremde Reviewer ist ehrlich und deckt sich mit eigenen Zweifeln.
- Untertitel groß, Satz für Satz, Wort für Wort aufleuchtend; gut stumm lesbar.
- Ton deterministisch und messbar (−16,8 LUFS, jeder Effekt hörbar über dem Bett).

**Schwächen / Beobachtungen**
- Langsam und teuer: ~2,5 h, viel mehr Tokens als huashu-motion. Der Prozess (Pitch, Fragen, Reviewer) ist für ein menschliches Gegenüber gebaut; ohne Antworten muss man vieles annehmen.
- Ohne Login/Bezahldienste läuft er unter seinen Möglichkeiten; er sagt das selbst (Code-only „~7 von 10“).
- Studio zum Kommentieren („Review Room“) läuft lokal; aus dieser Cloud-Sitzung für Hamid nicht erreichbar, Notizen also per Chat.

## Kurzvergleich

| | huashu-motion | take-one |
|---|---|---|
| Ansatz | DOM + GSAP, Templates, Studio | Canvas, eigene Welt, Studio-Rollen + Reviewer |
| Look | Anthropic-Website in Bewegung, Karten + Chips | Schreibtisch von oben, Papier, Licht |
| Markenschrift | Ersatz (Inter, EB Garamond) | echt (anthropicSans/Serif/Mono) |
| Untertitel | 1–4 Wörter, unten | ganze Sätze, groß, Wort für Wort |
| Musik | Lo-fi, eingebaute Richtung, Drop auf Payoff | Klavier/Streicher, Code-Partitur |
| Prüfung | `om check`, `om qa` | Text-Audit, Gate, frischer Reviewer (6/10) |
| Aufwand | ~1 h, 3 Renders à ~3 min | ~2,5 h, 4 Renders à ~7 min |
| Rückfragen (ausgelassen) | 3 Richtungen wählen | Run/Etappen, Route + Kosten |

## Für den nächsten Skill
Gleiche Kriterien notieren: Markentreue, Lesbarkeit stumm, Rhythmus (`om qa`-ähnliche Messung oder Bild-für-Bild), Bindung an Wortzeiten, Rückfragen, Aufwand, Renderzeit.
