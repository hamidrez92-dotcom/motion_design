# DIRECTION · claude-plugins · take-one

Eingabe wie bei allen Skills: `../../skript/skript.json` (79,9 s, geschätzte Wortzeiten), `../../quelle/`. Keine Aufnahme.

## Haltepunkte des Skills und was angenommen wurde
take-one hält auf einem „Run“ an genau zwei Stellen an: erste Antwort (Run oder in Etappen, Größe) und Pitch (Route, Kosten, Dienste). Hamid hat beides vorab beantwortet bzw. nicht verfügbar:
- **Run**, nicht in Etappen („mach weiter“, „ok nun mit diesem“).
- **Route: nur Code, kostenlos.** Keine Bild-, Video-, Stimm- oder Musikdienste (kein Codex, kein Higgsfield-Connector, kein Claude in Chrome in dieser Umgebung). Der Skill würde die bessere, bezahlte Route zuerst pitchen (siehe unten); sie ist für den nächsten Durchgang notiert, nicht still weggelassen.
- **Keine Stimme**, gesprochener Text als Untertitel (Hamid).
- **Skript fest:** Die Writer-Rolle schreibt nicht um (Regel des Vergleichs in `CLAUDE.md`). Wo take-one am Skript etwas ändern würde, steht es unten als Notiz.
- **Echtes Produkt** (der Skill will die eingeloggte Oberfläche aufnehmen): nicht möglich ohne Hamids Login. Darum keine nachgebaute Claude-Oberfläche.
- **Größe:** take-one schätzt 0,4–0,7 Mio. Tokens pro 30 s → hier etwa 1–1,8 Mio. Tokens, 2–3 h.

## Strategist
Für Instagram/TikTok-Nutzer, die Claude als Chat kennen. Eine Sache: *Fünf Plugins in zwei Minuten machen aus dem Chatbot einen Kollegen.* Konkurrenzstudie übersprungen (kein Produktlaunch, Erklär-Reel; die Kategorie „KI-Tipps-Reel“ ist fast immer Gesicht + Bildschirmaufnahme + Untertitel).

**Brand-Pack (claude.com, 2026-11-04):** Schriften anthropicSans / anthropicSerif / anthropicMono (echte Dateien, lokal, nicht im Git); Farben nach Häufigkeit #e3dacc (warmes Beige), #faf9f5, #dedcd1, #141413, #d97757 (Spark), #ebc9b7, #b0aea5, #87867f; Logo: Spark-SVG von claude.com; Claim der Startseite „Question what’s next“ (nicht benutzt, das Skript hat eigene Zeilen).
**Was heute wahr ist:** Alle Aussagen stammen aus dem Artikel (`skript/fakten.md`). Plugins und Menüweg nicht selbst geprüft (kein Login).

## Art director: der Weg zu erklären
Aus `directed-look.md`: **„Eine Welt, ein Schreibtisch“** (One committed world). Das Skript trägt schon das Bild: der neue Kollege und seine Einarbeitungsmappen. Also ein Schreibtisch von oben, unter einer Lampe: Ausweis, fünf Mappen, Laptop, Stoppuhr, Papiere. Jede Aussage ist ein Ereignis auf dem Tisch (eine Mappe landet, ein Textmarker fährt über eine Klausel, ein Stempel fällt). Die fünf Plugins sind **eine Kamerafahrt an fünf offenen Mappen vorbei**, jede mit eigenem Gegenstand und eigener Einstellungsgröße, nicht fünfmal dieselbe Karte.

**Bann-Liste (im Code oben):** abgerundete Karte mit weichem Schatten im Leeren · Pillen und Chips · Icon-Kacheln · alles zentriert · alles poppt mit Overshoot · Karaoke-Kästen · derselbe Rahmen für jedes Listenelement · lila/blaue Verläufe, Glow, Partikel · dunkler „Premium“-Grund (die Marke ist hell).

**Zahlen statt Adjektive:** Tischgrund #e3dacc mit Papierfaser-Rauschen (seeded); eine Lampe oben links (radialer Lichtkegel, Ecken −14 %); jedes Objekt mit Kontaktschatten (2/3 px, 4 px Blur, 0,22) und Raumschatten (14/22 px, 34 px Blur, 0,16); Papier #faf9f5, Mappen #dedcd1, Druck #141413/#87867f; Akzent #d97757 nur für Spark, Stempel, den „hoch“-Marker und das gerade gesagte Wort. Kamera nie geparkt: 2–4 % Kriechen in jedem Halten; Fahrten auf `camera`-Springs, Zooms im Log-Raum.

## Storyboard (Zeiten aus `skript.json`)
P = Bild, G = Seite; E = Ereignis, S = Zustand.

| # | Zeit | Was passiert | Muss gelesen werden | P/G | E/S |
|---|---|---|---|---|---|
| 1 | 0–3,7 | Blatt „Erst die Plugins.“ liegt da, fünf Mappen fallen nacheinander daneben, „Dann Claude.“ steigt auf dem Wort ein | 5 Mappen mit Namen | P | E |
| 2 | 3,7–9,6 | Laptop von oben, ein Chat: Frage, Antwort. Kamera fährt nach rechts, ein Ausweis „Neu im Team“ wird hingelegt | Chatbot → Mitarbeiter | P | E |
| 3 | 9,6–16,4 | Ausweis groß; auf „Einarbeitungsmappe“ rutscht die Mappe „Marketing“ daneben | Kollege + Mappe | P | E |
| 4 | 16,4–23,1 | Mappe klappt auf: drei Blätter (Skills), drei Kabel zu E-Mail/Kalender/Chat (Connectors); Stempel „1 Plugin · 1 Job“ | Plugin = Skills + Connectors | P | E |
| 5 | 23,1–43,3 | Eine Fahrt an fünf offenen Mappen: Kalender bekommt Posts gestempelt · Tabelle wird zur GuV · Textmarker über drei Klauseln · zwei Notizzettel auf einer Website · Haken auf einer Liste | je ein Plugin, je eine Tat | P | E |
| 6 | 43,5–50 | Stoppuhr läuft auf ~2 Min; Zettel „Customize › Plugins › Discover“ wird abgehakt; von drei Mappen bleibt nur die mit „by Anthropic“ | Weg + nur Anthropic | P | E |
| 7 | 50–62,1 | Laptop + Ausweis: der Setup-Prompt, Claude fragt eine Frage nach der anderen; Block mit drei leeren Kästchen | ein Prompt, Fragen | P | E |
| 8 | 62,3–68,1 | Licht wird dunkel, nur noch ein Kegel auf dem Vertrag; Stempel „Kein Anwalt“ | die Grenze | P | E |
| 9 | 68,2–73,6 | Licht voll: drei Karten klatschen auf: 5 Plugins, 2 Minuten, 1 Prompt; Ausweis landet auf dem Mappenstapel | 5 · 2 · 1, Kollege | P | E |
| 10 | 73,7–80,5 | Ein Lesezeichen „Speichern“ wird in den Stapel gesteckt; Kamera fährt zurück auf Bild 1 | speichern, Loop | P | E |

Seiten: 0 von 10. Zustände: 0 von 10.

## Konzept-Check (Selbst-Lesung, kein frischer Leser: der Skill erlaubt das, wenn es gesagt wird)
1. *Nacherzählt:* Ein Schreibtisch, auf dem Claude als neuer Kollege Ausweis und fünf Einarbeitungsmappen bekommt; jede Mappe zeigt, was ihr Plugin tut; am Ende liegt alles gestapelt da: 5 Plugins, 2 Minuten, 1 Prompt.
2. *Drei Antworten stumm:* Was: fünf Claude-Plugins von Anthropic (Mappen mit Namen, Schritt 1/5). Was es bringt: jede Mappe zeigt die Tat (Schritt 5). Was tun: installieren über Customize › Plugins › Discover, speichern (Schritt 6, 10).
3. *Worte aus:* Jede Einstellung hat ein Objekt und ein Ereignis; kein Text auf leerem Grund außer den Untertiteln.
4. *Bekannte Fehl-Defaults:* keiner (kein „Film über sich selbst“, kein Prompt auf Schwarz).
5. *Das eine Bild:* der Ausweis „Neu im Team · Claude“ neben der Mappe „Marketing“.
- *Selbst-Score:* 7/10 (Selbst-Lesungen liegen laut Skill ~2 Punkte zu hoch). Grenze: ohne echte Oberfläche bleibt der Teil „Installieren“ eine Illustration.

## Was die bezahlte Route hinzufügen würde (für Hamid, nicht gekauft)
- Echte Plugin-Oberfläche als Aufnahme (Login nötig, kostenlos): stärkster Hebel laut Skill („show, don't tell“).
- Ein echtes Foto eines Schreibtischs/Händen pro Schlüsselmoment (Bildmodell): von ~7 auf ~8 laut Skill-Erfahrung.
- Eine gesungene Fassung (Suno) aus den Skriptzeilen: der Skill bevorzugt sie für Filme, die von Worten leben.

## Skript-Notizen der Writer-Rolle (nicht umgesetzt, Skript ist fest)
- „Customize, Plugins, Discover“ sind englische Menünamen in einem deutschen Satz; gut zum Nachklicken, gesprochen sperrig.
- Der Aufruf am Ende hat keinen Link (es gibt keinen); laut Skill ist „Speichern“ als einfache Handlung in Ordnung.
