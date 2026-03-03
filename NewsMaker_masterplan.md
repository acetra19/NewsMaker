# NewsMaker Masterplan: The 'Sales-Free' Automated Video Bot

## 1. Strategie-Vergleich: Warum NewsMaker > Solar-Lead-Bot?

### Das Problem mit dem Solar-Lead-Bot (Der "Mensch-Faktor")
Das ursprüngliche Modell ("Solar-Lead-AI") basierte auf B2B-Vertrieb. Dies bringt massive operative Hürden für Solopreneure mit sich:
- **Gatekeeper:** E-Mails landen im Spam, Sekretariate blocken Anrufe.
- **Verkaufszyklus:** Erfordert aktive Überzeugungsarbeit, Demos und Follow-ups.
- **Client-Management:** Kunden haben Erwartungen, beschweren sich und kündigen Retainer-Verträge.
- **Skalierungsgrenze:** Linearer Aufwand (mehr Kunden = mehr Support).

### Die Lösung: NewsMaker (Permissionless Revenue)
Das NewsMaker-Modell eliminiert den Faktor "Kunde" vollständig.
- **Kein Verkauf:** Der Algorithmus (YouTube/TikTok) ist der einzige "Abnehmer". Er sagt nicht "Nein", er bewertet nur Metriken.
- **Permissionless:** Niemand muss um Erlaubnis gefragt werden, um zu starten oder zu skalieren.
- **Unendlicher Leverage:** Einmal geschriebener Code produziert tausende Videos. Ein Video kann 10 oder 10 Millionen Views generieren (gleicher Arbeitsaufwand).
- **Fokus:** Reines Engineering und Content-Qualität statt Kaltakquise.

---

## 2. Technische Architektur

Der Bot wird als modularer Python-Service aufgebaut.

### Core Stack
- **Sprache:** Python 3.10+
- **Umgebung:** Docker (Debian-based)
- **IDE-Support:** Optimiert für Cursor (VS Code Fork)

### Bibliotheken & APIs
1.  **Content & Skripting (The Brain):**
    -   `openai` (GPT-4o): Für Skripterstellung, Kernaussagen-Extraktion und Bild-Prompts.
    -   `praw` (Python Reddit API Wrapper): Zum Scrapen von viralen Geschichten/News.

2.  **Audio (The Voice):**
    -   `elevenlabs` (Official SDK): Für ultra-realistische "Narrator"-Stimmen (High-End TTS).
    -   *Fallback:* `edge-tts` (kostenlos, akzeptable Qualität für MVP).

3.  **Visuals (The Eyes):**
    -   `requests` (oder `httpx`): Zugriff auf Pexels Video API (Stock Footage).
    -   `replicate` (oder `openai` DALL-E 3): Generierung von spezifischen AI-Bildern via Flux/Midjourney Modellen für Szenen, wo Stock-Footage fehlt.

4.  **Video Engine (The Studio):**
    -   `moviepy`: Programmgesteuerter Videoschnitt, Komposition von Audio/Video/Bildern.
    -   `ffmpeg-python`: Low-Level-Optimierung und Rendering.
    -   `pillow`: Bildbearbeitung (Overlays, Resizing).
    -   `imagemagick`: Für Text-Overlays (Captions).

---

## 3. Workflow-Logik: Von Reddit zum Upload

Der Prozess läuft vollautomatisch ("Hands-off") ab:

### Schritt 1: Scouting & Filterung
- **Quelle:** Subreddits `r/singularity`, `r/ArtificialInteligence`, `r/futurology`, `r/technews`.
- **Logik:**
    - Hole "Top Posts" der letzten 24h.
    - **Filter:** Mindestens 1000 Upvotes (sozialer Beweis für Interesse).
    - Ausschluss von reinen Link-Posts ohne Diskussion (wir brauchen Kontext).

### Schritt 2: Content Transformation (Scripting)
- **Input:** Reddit Titel + Top 3 Kommentare (für Kontroverse/Meinung).
- **LLM-Prompt:**
    - "Act as a Viral Short Video Creator."
    - Erstelle ein 45-60 Sekunden Skript.
    - Struktur: **Hook** (0-3s, reißerisch) -> **Story/Info** (Fakten + "Fear of Missing Out") -> **Conclusion/CTA** (Frage an Zuschauer).

### Schritt 3: Asset Generierung
- **Audio:** Skript an ElevenLabs senden -> Erhalte `audio.mp3`.
- **Visual Analysis:** LLM analysiert das Skript Satz für Satz und entscheidet:
    - *Keyword:* "Robot walking" -> Suche auf Pexels.
    - *Abstract:* "AI taking over the world" -> Generiere Image-Prompt für Flux/DALL-E.
- **Download/Gen:** Alle Assets in temporären Ordner laden.

### Schritt 4: Video Assembly (Rendering)
- **Timeline:** Audio-Länge bestimmt Video-Länge.
- **Visueller Rhythmus:** Schnitt alle 3-5 Sekunden (zur Erhöhung der Retention).
- **Effekte:** "Ken Burns" (leichter Zoom) auf statische KI-Bilder.
- **Captions:**
    - Generierung von `.srt` oder Hard-Coding ins Video.
    - **Style:** "Hormozi-Style" (Große Schrift, Gelb/Weiß, mittig, Wort-für-Wort Animation).

### Schritt 5: Deployment
- **Upload:** Upload via YouTube Data API v3 (oder Selenium Fallback, falls API Quota limitiert).
- **Metadaten:** LLM generiert Titel, Beschreibung und Hashtags basierend auf SEO.

---

## 4. Monetarisierung

Das Ziel ist Cashflow ohne direkten Verkauf.

### Primär: Creator Funds
- **YouTube Shorts Fund / AdSense:** Bezahlung pro 1.000 Views (RPM).
- **Voraussetzung:** Hohe Retention Rate (durch Schnittfrequenz und Hook) und Originalität (durch KI-Bilder und individuelles Skripting, kein reiner Repost).

### Sekundär: Affiliate (The "Link in Bio")
- **Nische:** Future Tech & AI.
- **Produkte:**
    - AI Tools (Jasper, Midjourney Kurse, Trading Bots).
    - Tech Gadgets (Amazon Affiliate).
    - Krypto-Exchanges.
- **Integration:** "Link in Bio" (Linktree) und angepinnter Kommentar unter jedem Video ("Das Tool, das ich nutze: [Link]").

### Tertiär: Brand Deals (Später)
- Sobald der Kanal >50k Abos hat, können Produktplatzierungen für SaaS-Startups automatisiert eingebaut werden (Pre-Roll Clips).
