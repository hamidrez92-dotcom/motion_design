---
name: reel-skript-de
description: Schreibt deutsche Voiceover-Skripte für Instagram-Reels und TikToks (60–90 s) aus einem Artikel oder Thema — mit Hook, Beat-Sheet, Text im Bild und wortgenauen Visual-Cues, die ein Motion-Design-Skill (huashu-motion, Remotion, Hyperframes …) direkt umsetzen kann. IMMER verwenden, wenn aus einem Artikel, Link, Thema oder Stichpunkten ein Reel-, TikTok- oder Shorts-Skript entstehen soll, auch bei "mach daraus ein Reel", "kürz den Artikel auf 90 Sekunden", "Skript fürs Video".
---

# Reel-Skript (Deutsch)

Du machst aus einer Quelle ein **gesprochenes** Skript für ein vertikales Reel von **60–90 Sekunden**, das später ein Motion-Design-Skill bebildert. Das Skript ist die gemeinsame Vorlage: Verschiedene Motion-Skills bekommen exakt dasselbe Skript, damit man ihre Videos fair vergleichen kann. Deshalb beschreibt es **was** im Bild erklärt wird, nie **wie** es animiert wird.

Alles landet in `projekte/<slug>/` (Slug: kurz, klein, mit Bindestrichen, z. B. `mcp-erklaert`).

## Ablauf

### 1. Quelle sichern
Artikeltext nach `projekte/<slug>/quelle/artikel.md`, oben: Titel, URL (falls vorhanden), Autor, Datum, Abrufdatum. Bei einer URL den Artikel lesen und den Text vollständig ablegen, nicht nur zusammenfassen. Bei einem bloßen Thema ohne Quelle: Nutzer fragen, ob du recherchieren sollst, und jede Quelle hier mit URL eintragen.

### 2. Fakten extrahieren → `skript/fakten.md`
- **Kernaussage** in einem Satz: das eine, was der Zuschauer nach 90 s weiß.
- **Zielgruppe** in einem Satz (Default: interessierte Laien, keine Fachleute).
- **5–10 Fakten**, je mit wörtlicher Belegstelle aus der Quelle. Zahlen, Namen und Daten exakt übernehmen.
- **Gestrichen**: was interessant ist, aber nicht in 90 s passt, mit einem Wort Begründung.
- **Nichts erfinden.** Fehlt eine Zahl, die das Skript braucht, schreib `{{Zahl fehlt: …}}` — `beats.py` blockiert, bis sie ersetzt ist.

Für 60–90 s passen **2–3 Kernpunkte**. Lieber zwei Punkte, die sitzen, als vier, die vorbeirauschen.

### 3. Dramaturgie

| Zeit | Beat | Aufgabe |
|---|---|---|
| 0–3 s | `HOOK` | Behauptung, Zahl oder Widerspruch. Max. **8 gesprochene Wörter**. Ab Frame 1 sichtbar. |
| 3–12 s | `KONTEXT` | Warum betrifft mich das? Was steht auf dem Spiel? |
| 12–70 s | `PUNKT` × 2–3 | Je ein Gedanke, je 12–20 s, gern in 2–3 Beats aufgeteilt. Jeder Punkt hat ein konkretes Beispiel oder eine Zahl. |
| optional | `WENDE` | Die Überraschung / das Aber, kurz vor Schluss. |
| letzte ~8 s | `PAYOFF` | Die Kernaussage, ausgesprochen. |
| letzte ~4 s | `CTA` | Eine Handlung (folgen, speichern, kommentieren). Kein Wortsalat. |

**Wortbudget** bei 145 Wörtern/Minute (deutsches Voiceover): 60 s ≈ 145 Wörter, 75 s ≈ 180, 90 s ≈ 215. Ein Beat dauert 3–8 s.
**Loop:** Der letzte Satz greift ein Wort oder Bild aus dem Hook auf, damit das Reel nahtlos neu startet.

### 4. Hook
Lies [references/hooks.md](references/hooks.md). Schreib **drei** Hooks nach verschiedenen Mustern, bewerte jeden mit dem 10-Punkte-Raster dort, nimm den besten. Zeig dem Nutzer alle drei mit Punktzahl; er kann tauschen.

### 5. Skript schreiben → `skript/skript.md`
Format (genau so, `beats.py` liest es):

```markdown
---
titel: Was ist MCP?
quelle: ../quelle/artikel.md
zieldauer: 75
wpm: 145
---

## B01 · HOOK
SPRECH: Deine KI kann alles erklären. Aber nichts anfassen.
TEXT: KI kann nichts anfassen
VISUAL @KI [chat]: Ein Chatfenster, die KI antwortet sofort und selbstsicher.
VISUAL @anfassen [metapher]: Eine Hand greift ins Leere neben einer Datei.

## B02 · KONTEXT
SPRECH: …
```

- `## Bnn · ROLLE` — Rollen: `HOOK`, `KONTEXT`, `PUNKT`, `WENDE`, `PAYOFF`, `CTA`.
- `SPRECH:` — genau das, was gesprochen wird. Eine Zeile pro Beat.
- `TEXT:` — optionaler Text im Bild, **max. 6 Wörter**. Nicht der Sprechtext wiederholt, sondern das Stichwort.
- `VISUAL @Anker [typ]: Beschreibung` — beliebig viele pro Beat.
  - `@Anker` ist ein Wort (oder `@"zwei Wörter"`) aus dem `SPRECH` dieses Beats. Dort erscheint das Visual — **genau auf dem Wort**. Ohne Anker: Beat-Beginn.
  - `[typ]`: `chat`, `zahl`, `liste`, `vergleich`, `diagramm`, `zitat`, `logo`, `screenshot`, `text`, `icon`, `metapher`, `ui`.
  - Beschreibung: **was** gezeigt und erklärt wird, mit den echten Inhalten (welche Zahl, welcher Chat-Text, welche Listenpunkte). **Nicht** wie es animiert wird (keine Farben, Kamerafahrten, Übergänge) — das entscheidet der Motion-Skill.
- Spätestens alle **5 Sekunden** ein neues Visual. Das ist der häufigste Grund, warum `beats.py` warnt.

**Sprechsprache:**
- Schreib, wie du es sagen würdest. Sätze max. ~15 Wörter, Hauptsätze vor Nebensätzen.
- „du“, aktiv, Präsens. Keine Klammern, keine Abkürzungen, keine Schrägstriche, keine Gedankenstriche.
- Zahlen so, wie man sie spricht: „rund zwei Drittel“ statt „66,7 %“, wenn die Quelle das trägt.
- Fachbegriff → sofort ein Bild oder Vergleich dazu.
- Wenn verfügbar, Hamids Skills anwenden: **hamid-erklaertexte** (Aufbau, Analogien), **hamid-ton-stil** (Ton, Rhythmus), am Ende **humanizer-de** als Edit-Pass.

### 6. Prüfen
```sh
python3 .claude/skills/reel-skript-de/scripts/beats.py projekte/<slug>/skript/skript.md
```
Schreibt `skript.json` (Beats, geschätzte Zeiten, Visuals mit Zeitpunkt) und `sprechtext.txt` (ein Satz pro Zeile, zum Einsprechen und für `om voice --text`). Alle `FEHLER` beheben, `WARNUNG`en bewusst entscheiden.

Dann die QA aus [references/qa-rubrik.md](references/qa-rubrik.md): bewerten, unter **90/100** überarbeiten, max. drei Runden. Ergebnis als `skript/qa.md`.

### 7. Übergabe
Dem Nutzer zeigen: die drei Hooks mit Punkten, das Skript (nur Sprechtext, als Fließtext zum Lesen), Dauer, QA-Punkte. Hinweis: `sprechtext.txt` einsprechen und als `projekte/<slug>/audio/voice.wav` (oder .m4a) ablegen.

Sobald die Aufnahme da ist und ein Motion-Skill Wortzeiten erzeugt hat (z. B. huashu-motion: `assets/voice.words.json`), die echten Zeiten übernehmen:
```sh
python3 .claude/skills/reel-skript-de/scripts/beats.py projekte/<slug>/skript/skript.md --words <pfad>/voice.words.json
```
Dann stehen in `skript.json` die gemessenen statt geschätzten Zeitpunkte.

## Regeln
- Das Skript ist für alle Motion-Skills gleich. Nach der Freigabe nicht mehr pro Skill umschreiben; Änderungen gehen in `skript.md` und gelten für alle.
- Keine Fakten ohne Beleg in `fakten.md`.
- Nichts veröffentlichen.
