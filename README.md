# 🕊️ Memorial Storyteller & Milestone Companion

> **A thoughtful, child-safe generative AI platform enabling bereaved families to transform preserved voice notes and portrait photos into comforting, milestone tribute videos.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![React Native](https://img.shields.io/badge/React%20Native-Expo%20SDK%2052-black)](https://reactnative.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB.svg)](https://python.org)

---

## 🌟 The Vision & Origin

When a loved one passes away, families often retain treasured WhatsApp voice notes and candid photos. Young children miss hearing their parents' voices at bedtime or during major life milestones (birthdays, graduations, first day of school). 

Unlike open-ended conversational avatars—which child psychologists caution can prolong grief denial or generate distressing hallucinations—**Memorial Storyteller** is built strictly as a **"Curated Legacy & Milestone Storyteller"**:

1. **Structured Scripting:** Messages and bedtime stories are crafted and reviewed by adult guardians.
2. **Guardian Review Gate:** Every synthetic video is held behind a parental PIN or biometric check before children can view it.
3. **In-the-Wild Media Restoration:** State-of-the-art speech enhancement cleans noisy, compressed mobile recordings into clear vocal models.

---

## 🏗️ System Architecture

```
┌────────────────────────────────────────────────────────┐
│            MOBILE CLIENT (React Native / Expo)         │
│  - Media Vault (Upload WhatsApp Audio & Photos)        │
│  - Story Studio (Bedtime Stories & Milestones)         │
│  - Guardian Review Gate (PIN-Protected Approval)       │
│  - Child Storybook Player (Calm, Distraction-Free UI)  │
└───────────────────────────┬────────────────────────────┘
                            │ HTTPS (REST) + WebSockets
┌───────────────────────────▼────────────────────────────┐
│              BACKEND API (FastAPI / Python 3.12)       │
│  - Pydantic v2 Schema Validation                       │
│  - Task Dispatcher & Background Pipeline               │
│  - Media SNR & Clarity Quality Analyzers               │
└─────────────┬────────────────────────────┬─────────────┘
              │                            │
┌─────────────▼──────────┐      ┌──────────▼─────────────┐
│  Database (PostgreSQL) │      │  Cloud Storage (R2/S3) │
│  - Avatar Profiles     │      │  - Encrypted Raw Stems │
│  - Story Job State     │      │  - Final Rendered MP4s │
└────────────────────────┘      └────────────────────────┘
              │
┌─────────────▼──────────────────────────────────────────┐
│             AI & GENERATIVE PIPELINE                   │
│  Stage 1: Denoise & VAD (DeepFilterNet3 / Silero-VAD)  │
│  Stage 2: Voice Cloning (ElevenLabs API / F5-TTS)      │
│  Stage 3: Portrait Video (LivePortrait / Hedra API)    │
│  Stage 4: Post-Processing & Watermarking (FFmpeg 7)    │
└────────────────────────────────────────────────────────┘
```

---

## 🚀 Key Features

* **🎙️ Audio Denoising & Enhancement:** Recovers high-frequency harmonics from low-bitrate WhatsApp audio (`.m4a`, `.ogg`) and suppresses ambient background noise.
* **🗣️ Few-Shot Voice Synthesis:** Zero-shot flow matching TTS requiring as little as 15–30 seconds of reference audio.
* **👤 Talking Portrait Animation:** Generates natural facial dynamics, eye blinks, and lip-syncing from a single front-facing photograph.
* **🛡️ Parental Guardian Gate:** Biometric or 4-digit PIN verification to inspect and approve every video before it enters the child's playlist.
* **✨ Child Storybook Mode:** A cozy, peaceful mobile interface where children can listen to Dad or Mom reading bedtime stories.

---

## 📂 Project Structure

```
memorial-storyteller/
├── backend/
│   ├── app/
│   │   ├── main.py                     # FastAPI entrypoint with CORS & routes
│   │   ├── core/config.py              # Environment configuration & API keys
│   │   ├── models/schemas.py           # Pydantic v2 schemas for Avatars & Jobs
│   │   ├── services/
│   │   │   ├── audio_processor.py      # Noise reduction & audio quality scoring
│   │   │   ├── voice_cloner.py         # ElevenLabs / F5-TTS voice synthesis
│   │   │   └── portrait_animator.py    # LivePortrait / Hedra video generation
│   │   └── api/v1/
│   │       ├── avatars.py              # Profile management & consent attestation
│   │       └── stories.py              # Story jobs & Guardian approval gate
│   └── requirements.txt                # Python backend dependencies
│
├── scripts/
│   └── friend_prototype.py             # Standalone runner for testing real audio & photo
│
└── mobile/                             # React Native (Expo SDK 52)
    ├── package.json                    # expo-video, expo-audio, expo-secure-store
    ├── app.json                        # Expo app configuration
    ├── App.tsx                         # Stack Navigation root
    └── src/screens/
        ├── MediaVaultScreen.tsx        # Upload media with visual quality scores
        ├── StoryStudioScreen.tsx       # Milestone & Bedtime story composer
        ├── GuardianGateScreen.tsx      # PIN-protected preview & approval gate
        └── ChildVaultScreen.tsx        # Child-facing storybook player
```

---

## ⚡ Quick Start

### 1. Run the Friend Prototype Script (Immediate Test)
To generate a test tribute video using a voice note and a portrait photo:

```bash
cd scripts
python friend_prototype.py \
  --audio "path/to/voice_sample.m4a" \
  --photo "path/to/photo.jpg" \
  --key "YOUR_ELEVENLABS_API_KEY"
```

### 2. Start the Backend API

```bash
cd backend

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Launch FastAPI development server
uvicorn app.main:app --reload --port 8000
```
* **Swagger API Documentation:** `http://localhost:8000/docs`
* **Health Check:** `http://localhost:8000/health`

### 3. Launch the React Native Mobile App

```bash
cd mobile

# Install dependencies
npm install

# Start Expo development server
npx expo start
```
* Scan the QR code with the **Expo Go** app on iOS or Android, or press `a` for Android Emulator / `i` for iOS Simulator.

---

## 📜 Ethical AI, Privacy, & App Store Compliance

* **Posthumous Consent:** All users must attest to family relationship and legal guardianship during profile onboarding.
* **Child Grief Protection:** The app explicitly does **not** feature an unconstrained, live AI conversational chatbot.
* **Synthetic Media Transparency:** Subtle, respectful watermark (*"Created with love by Family Memorial Companion"*) embedded on all exports in compliance with Apple Guideline 5.1/1.2 and Google Play Synthetic Media policies.
* **Data Isolation:** All personal recordings and synthetic stems are encrypted at rest with zero data retention for training public models.

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).
