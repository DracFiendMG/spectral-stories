# 🎬 AI-Powered Demo Video Creation Guide for "Spectral Stories"

This guide outlines how to create a high-impact, professional 60–90 second demo video for your Dev.to Hacktoberfest submission using modern AI tools.

---

## 🚀 Recommended AI Workflow (Fastest & Highest Quality)

### Step 1: Record 4 Short Screen Clips (No audio needed yet)
Use any free screen recording tool (Windows Game Bar `Win + G`, OBS Studio, or Chrome):
- **Clip 1 (0:00 - 0:15)**: Hero screen of Spectral Stories, showing candle flickering, floating marigold petals, and warm ambient glow.
- **Clip 2 (0:15 - 0:35)**: Lighting a candle on the Digital Ofrenda, uploading a sample memorial photo, selecting offerings (Pan de Muerto, Cempasúchil), and clicking **"Invoke Remembrance"** to watch the memorial text generate in real time.
- **Clip 3 (0:35 - 0:55)**: Switching to **"Ghost in the Machine" Mode**, loading the sensor CSV dataset (or custom logs), clicking **"Run TabPFN Anomaly Scan"**, and showing the detected 3:03 AM paranormal temperature anomaly with probability score.
- **Clip 4 (0:55 - 1:15)**: Playing the eerie voice narration with ambient sound chimes, showing the Render deployment and GitHub repository badges.

---

## 🎙️ Step 2: Generate the Voiceover using AI

Generate realistic, high-quality narration using one of these AI tools:

1. **Option A: ElevenLabs (Top Quality)**
   - Voice: "Adam" or "Rachel" or "Marcus" (warm, expressive, slightly reverent tone).
   - Paste the script below into [ElevenLabs](https://elevenlabs.io).

2. **Option B: Edge-TTS (100% Free, High Quality, No Account Needed)**
   - You can run it via Python directly:
     ```bash
     pip install edge-tts
     edge-tts --text "Welcome to Spectral Stories..." --voice "en-US-ChristopherNeural" --write-media narration.mp3
     ```

3. **Option C: Piper TTS / Coqui (Local Open-Source)**
   - Run fully locally to align with the open-source spirit!

---

## 📜 Complete 75-Second Demo Video Script

| Time | Visual on Screen | Voiceover Script (Word-for-Word) |
|---|---|---|
| **0:00 - 0:12** | Cinematic pan across the candlelit altar with falling petals. | *"Every October, we celebrate both the thrills of Halloween and the sacred remembrance of Día de los Muertos. But in our modern world... what if the ghost in the machine was both a protector of our memories and an anomaly in our data?"* |
| **0:12 - 0:32** | User enters loved one's name, lights an altar candle, selects offerings, and generates the memorial. | *"Meet Spectral Stories. First, the Digital Ofrenda. Here, you can honor those you've lost in complete privacy. Powered by local, open-weight AI, your sacred memories are woven into heartfelt eulogies without ever being sold to commercial cloud APIs."* |
| **0:32 - 0:52** | Switching to Haunted Data tab, running TabPFN scan on CSV logs, showing anomaly chart. | *"Next, the Ghost in the Machine. Using Prior Labs' TabPFN tabular foundation model, Spectral Stories scans your sensor and system logs for eerie statistical outliers—like unexplained cold spots and phantom motion spikes during the witching hour."* |
| **0:52 - 1:07** | Showing the audio player, narration voice speaking, and Render live link. | *"With built-in ambient generative audio and open speech synthesis, the spirits speak directly to you. Deployed seamlessly on Render with full open-source code under the MIT license."* |
| **1:07 - 1:15** | Closing hero banner, GitHub link, Hacktoberfest badges. | *"Spectral Stories: where open-source AI honors the past and listens to the machines of today. Check out the link below and light a candle."* |

---

## ✂️ Step 3: Auto-Assemble & Captions using AI

1. **CapCut (Desktop or Web - 100% Free)**:
   - Import your 4 screen clips + the generated `narration.mp3`.
   - Click **"Auto Captions"** -> AI automatically generates animated captions with perfect timing.
   - Add a subtle slow zoom or transition between clips.
   - Export 1080p MP4.

2. **Descript (AI Timeline Editor)**:
   - Paste the voiceover and drop the screen clips; it automatically aligns your footage to the spoken script.

3. **Fully Automated Python Assembly (No manual editing)**:
   - If preferred, we can use `moviepy` in Python to automatically join the screen recordings and mix the AI narration audio into an output video with one command!

---

## 🌌 Bonus: AI-Generated Intro Hook (Runway / Pika / Kling)
For the first 3 seconds, you can generate a cinematic 3-second establishing shot using an AI video generator with this prompt:
> *"Cinematic close-up of a glowing Mexican Día de los Muertos altar with flickering candles, orange cempasúchil petals floating in dark air, soft golden bokeh, hyper-realistic 4K, eerie warm atmosphere."*
