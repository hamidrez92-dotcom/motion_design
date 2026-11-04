# motion_design

Ein Artikel rein, ein 60–90-Sekunden-Reel raus, gebaut von verschiedenen Motion-Design-Skills aus **demselben** Skript, damit man sie nebeneinander vergleichen kann.

```
Artikel ──► reel-skript-de ──► skript.json + sprechtext.txt
                                   │            │
                                   │      (einsprechen) ──► audio/voice.wav
                                   ▼
                 ┌─────────────────┼─────────────────┐
           huashu-motion      Skill B …          Skill C …
                 ▼                 ▼                 ▼
           videos/huashu-motion/  videos/…       videos/…   ──► vergleich.md
```

## Skills
- **`reel-skript-de`** (`.claude/skills/reel-skript-de/`): eigener deutscher Skript-Skill. Faktenextraktion mit Belegen, Hook-Muster mit Bewertung, Beat-Sheet, Text im Bild, Visual-Cues mit Wort-Anker (`VISUAL @Chat [chat]: …`). `scripts/beats.py` prüft Dauer, Hook-Länge, Abstände zwischen Visuals und Anker und exportiert `skript.json`. Mit `--words` übernimmt es die echten Wortzeiten aus der Aufnahme.
- **`huashu-motion`** (`vendor/huashu-motion/`): Motion-Design als HTML + GSAP, Render über Chrome und FFmpeg, Voiceover mit Wort-Synchronisation, Musik und Effekte. MIT-Lizenz, © Huashu.

## Ordner
```
projekte/<slug>/
  quelle/artikel.md
  skript/   fakten.md  skript.md  skript.json  sprechtext.txt  qa.md
  audio/    voice.wav
  videos/<skill>/...
  vergleich.md
```
