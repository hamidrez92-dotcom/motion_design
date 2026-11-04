# motion_design

Reels (60–90 s, 1080×1920, deutsch) aus Artikeln: erst ein Skript, dann bebildern verschiedene Motion-Design-Skills **dasselbe** Skript, damit man sie vergleichen kann.

## Ablauf
1. **Skript** mit dem Skill `reel-skript-de` → `projekte/<slug>/quelle/`, `projekte/<slug>/skript/` (`skript.md`, `skript.json`, `sprechtext.txt`, `fakten.md`, `qa.md`).
2. **Aufnahme** (Hamids Stimme) → `projekte/<slug>/audio/voice.wav|m4a`. Dieselbe Aufnahme für alle Motion-Skills.
3. **Video je Motion-Skill** → `projekte/<slug>/videos/<skill-name>/` (das Projekt des Skills, Render unter `out/`).
4. **Vergleich** → `projekte/<slug>/vergleich.md`.

## Regeln für den Vergleich
- Jeder Motion-Skill bekommt nur `skript/skript.json` (+ `skript.md`), `quelle/` und `audio/`. Kein Skill sieht das Video eines anderen.
- Das Skript wird für einen Skill nicht umgeschrieben. Änderungen gehen in `skript.md` und gelten für alle.
- Jeder Skill arbeitet nach seinem eigenen SKILL.md, mit seinen Defaults. Notiere in `vergleich.md`, welche Rückfragen der Skill gestellt hat und was du dafür angenommen hast.
- Alles bleibt auf Deutsch.

## Motion-Skills
| Skill | Ort | Aufruf |
|---|---|---|
| huashu-motion 0.3.1 | `vendor/huashu-motion` (Kopie von github.com/alchaincyf/huashu-motion, Commit in `.upstream-commit`), verlinkt nach `.claude/skills/huashu-motion` | `.claude/skills/huashu-motion/bin/om …` |
| take-one 0.1.0 | `vendor/take-one` (Kopie von github.com/talsiach/take-one, Commit in `.upstream-commit`), verlinkt nach `.claude/skills/take-one`; Anthropic-Schriften pro Projekt mit `fetch-fonts.sh` holen (nicht im Git) | `node <projekt>/frames.mjs`, `bash vendor/take-one/scripts/render-parallel.sh` |

Neue Skills genauso: unter `vendor/<name>/` ablegen, nach `.claude/skills/<name>` verlinken, Zeile hier ergänzen.
