# Spectral Stories 🪔🕯️
### Día de los Muertos Interactive Memorial & Ghost Telemetry Archive

[![GitHub Repository](https://img.shields.io/badge/GitHub-DracFiendMG%2Fspectral--stories-orange?style=flat&logo=github)](https://github.com/DracFiendMG/spectral-stories)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> *"No one is truly gone as long as their name is spoken with warmth and their memory cherished."*

**Spectral Stories** is a dual-perspective interactive web application that bridges folkloric remembrance and supernatural intrigue. It pairs an authentic **Día de los Muertos Community Ofrenda Altar** with a **Gothic Paranormal Telemetry Station**.

Repository: [https://github.com/DracFiendMG/spectral-stories](https://github.com/DracFiendMG/spectral-stories)

---

## 🌟 The Experience

### 1. The Living Ofrenda Altar 🕯️
A tribute to Día de los Muertos tradition where visitors can:
- **Build & Dedicate Memorials**: Inscribe personal stories, photographs, and memories for departed ancestors and loved ones.
- **Select Traditional Offerings**: Place golden *cempasúchil* (marigolds), glowing tapers, copal incense, *pan de muerto*, guitars, handcrafted calaveras, or water.
- **Poetic Inscriptions**: Generate evocative, respectful remembrance verses powered by the **Backboard SDK** running `google/gemma-4-26b-a4b-it`.
- **Dynamic Altar Atmosphere**: Candle flame flickers, floating marigold petal animations, and warm parchment aesthetics designed to evoke genuine reverence.

### 2. The Paranormal Telemetry Station 👻
An investigative console monitoring anomalies in sensory data:
- **Sensor Telemetry Analysis**: Continuous tracking of ambient temperature, electromagnetic field (EMF) flux, acoustic micro-vibrations, and barometric drops.
- **Spectral Density Detection**: Uses **TabPFN** (Tabular Prior-data Fitted Network) architecture to classify anomalous environmental shifts into spectral manifestations.
- **Narrative Lore Synthesis**: Generates atmospheric gothic vignettes explaining the lingering presence behind each detected anomaly.
- **Audio Verification Frequency**: Interactive sound synthesis to detect EVP (electronic voice phenomena) harmonics.

---

## 🛠️ Architecture & Technology

- **Backend**: FastAPI (Python asynchronous web framework) with Uvicorn
- **Language Intelligence**: [Backboard SDK](https://pypi.org/project/backboard-sdk/) (`backboard-sdk`) orchestrating `google/gemma-4-26b-a4b-it`
- **Tabular Modeling**: TabPFN (Tabular Prior-data Fitted Network) & PyTorch for ghost telemetry classification
- **Frontend**: Pure Vanilla HTML5, CSS3, and JavaScript
  - Rich typography: *Cinzel Decorative*, *Cinzel*, and *Cormorant Garamond*
  - Authentic Día de los Muertos gold and marigold color palettes with warm candlelight amber glow
  - Handcrafted micro-animations (candle illumination, marigold petal drift, parchment scrolls)
  - No bloated CSS frameworks or generic AI templates

---

## 🚀 Quickstart Guide

### 1. Clone the Repository
```bash
git clone https://github.com/DracFiendMG/spectral-stories.git
cd spectral-stories
```

### 2. Set Up Virtual Environment & Dependencies
```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Add your Backboard API key:
```env
BACKBOARD_API_KEY=your_backboard_api_key_here
BACKBOARD_MODEL=google/gemma-4-26b-a4b-it
BACKBOARD_PROVIDER=openrouter
```

### 4. Run the Application
```bash
python server.py
```
Open your browser and navigate to:
**`http://localhost:8000`**

---

## 📁 Project Structure

```
spectral-stories/
├── index.html              # Handcrafted dual-view UI (Ofrenda Altar & Telemetry)
├── styles.css              # Custom gothic & Día de los Muertos styling & animations
├── app.js                  # Interactive application logic & audio synthesis
├── server.py               # FastAPI backend & telemetry endpoints
├── requirements.txt        # Python dependencies
├── .env.example            # Environment configuration template
├── README.md               # Documentation & setup instructions
├── data/
│   └── sensor_readings.csv # Real-world sensory baseline dataset
└── engine/
    ├── story_engine.py     # Backboard SDK integration with Gemma 4 26B
    └── tabpfn_detector.py  # TabPFN spectral anomaly detector
```

---

## 📜 Cultural Note & Heritage

Día de los Muertos (Day of the Dead) is recognized by UNESCO as an Intangible Cultural Heritage of Humanity. This project approaches the tradition with dignity, love, and respect—celebrating memory as the bridge between past and present.

Created with devotion for Hacktoberfest 2026.
GitHub: [DracFiendMG/spectral-stories](https://github.com/DracFiendMG/spectral-stories)
