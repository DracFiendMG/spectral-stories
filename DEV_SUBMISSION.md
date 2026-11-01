---
title: Spectral Stories — Día de los Muertos Living Memorial & Paranormal Telemetry Archive
published: true
tags: python, ai, webdev, hacktoberfest
canonical_url: https://github.com/DracFiendMG/spectral-stories
cover_image: https://raw.githubusercontent.com/DracFiendMG/spectral-stories/main/preview.png
description: A heartfelt interactive Día de los Muertos community ofrenda paired with a gothic paranormal telemetry station, powered by Backboard SDK and TabPFN.
---

# Spectral Stories 🪔🕯️
### Día de los Muertos Living Memorial & Paranormal Telemetry Archive

> *"In the sacred wisdom of our ancestors, a soul never truly perishes so long as their name is spoken with warmth and their memory celebrated."*

GitHub Repository: [https://github.com/DracFiendMG/spectral-stories](https://github.com/DracFiendMG/spectral-stories)

---

## 💡 The Inspiration

For this project, I wanted to create something deeply human, atmospheric, and respectful. Every autumn, Día de los Muertos invites us to reflect upon memory, mortality, and the enduring bonds of family and heritage. Concurrently, centuries of folklore across the world tell tales of lingering spirits, mysterious sensory shifts, and the thin boundary between worlds.

**Spectral Stories** combines these two evocative realms into a cohesive dual-perspective application:
1. **The Community Ofrenda Altar**: A warm, candlelight sanctuary where visitors create personal memorial cards, offer virtual *cempasúchil* (marigolds) and pan de muerto, and inscribe poetic remembrances.
2. **The Paranormal Telemetry Station**: An investigative telemetry console monitoring environmental fluctuations (EMF spikes, temperature drops, acoustic harmonics) to detect spectral presences and weave gothic lore vignettes.

---

## 🛠️ How It's Built

### 1. Generative Memorial Inscriptions via Backboard SDK
To craft sincere, poetic memorial verses without generic AI jargon, the memorial altar utilizes the **Backboard SDK** (`backboard-sdk`) orchestrating `google/gemma-4-26b-a4b-it`. 

Each inscription integrates:
- The deceased loved one's name and relationship
- Cherished memories or personality traits
- Chosen ofrenda offerings (marigolds, glowing tapers, copal incense, guitars)

The resulting tributes sound like heartfelt poetry written by a loving descendant rather than robotic machine output.

```python
from backboard import BackboardClient

async with BackboardClient(api_key=BACKBOARD_API_KEY) as client:
    resp = await client.send_message(
        content=memorial_prompt,
        llm_provider="openrouter",
        model_name="google/gemma-4-26b-a4b-it"
    )
    tribute_text = resp.content
```

### 2. Spectral Anomaly Detection with TabPFN
The paranormal telemetry station takes real tabular sensor readings—tracking ambient temperature, electromagnetic field fluctuations, acoustic micro-vibrations, and barometric drops. 

Using **TabPFN** (Tabular Prior-data Fitted Network), the telemetry engine evaluates multidimensional sensor shifts against paranormal baseline patterns in real-time, classifying anomalies into specific manifestation tiers (Class I Poltergeist, Class II Apparition, Class III Spectral Manifestation).

### 3. Handcrafted Human UI Design
Instead of using standard template libraries or generic AI design patterns, the entire user interface was handcrafted with:
- **Cinzel Decorative** & **Cormorant Garamond** classic editorial typography
- Saturated marigold oranges, altar golds, and deep obsidian midnight hues
- Subtle micro-animations: gentle candle flame flickers, drifting golden cempasúchil petals, and parchment glow
- An interactive Web Audio synthesizer simulating atmospheric candle ambience and EVP frequencies

---

## 🚀 Running the Project Locally

Clone and run in under two minutes:

```bash
git clone https://github.com/DracFiendMG/spectral-stories.git
cd spectral-stories

python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

pip install -r requirements.txt
cp .env.example .env      # Add your BACKBOARD_API_KEY
python server.py
```

Then visit `http://localhost:8000` in your browser.

---

## 🕊️ A Note on Cultural Reverence

Día de los Muertos is recognized by UNESCO as an Intangible Cultural Heritage of Humanity. In building Spectral Stories, the goal was not to treat folklore as a novelty, but to create a dignified digital space where the joy of remembrance meets the atmospheric wonder of autumn nights.

GitHub Repository: [DracFiendMG/spectral-stories](https://github.com/DracFiendMG/spectral-stories)
