# Specification-Driven Development (SDD): Memorial Storyteller & Milestone Companion

**Project Codename:** Project Remembrance / LegacyNarrator  
**Document Version:** 1.0.0  
**Target Platforms:** iOS & Android (React Native / Expo), Cloud API (FastAPI)  
**Date:** September 2026  

---

## 1. Executive Summary & Product Vision

### 1.1 Problem Statement
When a loved one passes away, families (especially young children) grieve the loss of connection. While existing photos and voice notes exist, they are often scattered, noisy, and static. Bereaved family members wish they could preserve and hear their loved one's voice narrating meaningful life moments, milestones, and comforting bedtime stories.

### 1.2 The "Grief Tech" Solution & Child-Safe Product Framing
* **The Antipattern to Avoid:** An unconstrained, interactive conversational chatbot pretending to be alive. Child psychologists caution this can cause severe confusion, prolong grief denial, and trigger distress through hallucinations.
* **The Selected Solution:** **"Curated Legacy & Milestone Storyteller"**
  * The application creates **scripted, loving videos** (bedtime stories, birthday wishes, graduation letters, holiday greetings).
  * **Strict Guardian Gate:** An adult family member writes or approves all scripts, previews generated videos behind a biometric/PIN lock, and controls child access.
  * **In-the-Wild Media Recovery:** Specialized AI algorithms denoise raw, compressed WhatsApp voice notes and candid phone photos into clean, photorealistic synthetic videos.

---

## 2. System Architecture & Tech Stack

```
┌────────────────────────────────────────────────────────┐
│           MOBILE FRONTEND (React Native / Expo)        │
│  - Expo SDK 52+ (Bridgeless / New Architecture)        │
│  - TypeScript 5.x & NativeWind v4 (Tailwind CSS)       │
│  - expo-video (High-performance video player)          │
│  - expo-audio (In-app audio recorder & player)         │
│  - expo-secure-store + expo-local-authentication (PIN) │
│  - TanStack Query v5 (Data fetching & caching)         │
└───────────────────────────┬────────────────────────────┘
                            │ HTTPS (REST) + WebSockets
┌───────────────────────────▼────────────────────────────┐
│          API GATEWAY & BACKEND (FastAPI 0.115+)        │
│  - Python 3.12 Runtime                                 │
│  - Pydantic v2 (Strict Schema Validation)              │
│  - Supabase Auth (JWT, Apple & Google OAuth)           │
│  - Redis + Celery (Task Queue & Job Orchestration)     │
└─────────────┬────────────────────────────┬─────────────┘
              │                            │
┌─────────────▼──────────┐      ┌──────────▼─────────────┐
│  PostgreSQL (Supabase) │      │   Cloudflare R2 / S3   │
│  - Users & Profiles    │      │  - Encrypted raw audio │
│  - Avatar Encodings    │      │  - Denoised stems      │
│  - Story Jobs & State  │      │  - Final rendered MP4s │
│  - Row-Level Security  │      │  - Zero egress fees    │
└────────────────────────┘      └────────────────────────┘
              │
┌─────────────▼──────────────────────────────────────────┐
│             GPU SERVERLESS WORKERS (Modal / RunPod)    │
│  - Container Runtime: Python 3.11/3.12 + PyTorch 2.4   │
│  - Stage 1: Audio Denoise (DeepFilterNet3 / Demucs v4) │
│  - Stage 2: Voice Cloning (ElevenLabs API / F5-TTS)    │
│  - Stage 3: Portrait Video (LivePortrait / Hedra API)  │
│  - Stage 4: Post-Processing & Watermarking (FFmpeg 7)  │
└────────────────────────────────────────────────────────┘
```

---

## 3. Database Schema (PostgreSQL)

```sql
-- Enable UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Users / Guardians
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT UNIQUE NOT NULL,
    full_name TEXT NOT NULL,
    guardian_pin_hash TEXT, -- Stored hashed PIN for parental control
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Loved One (Avatar Profiles)
CREATE TABLE avatar_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    relationship TEXT NOT NULL, -- e.g. "Father", "Grandmother"
    consent_attested BOOLEAN NOT NULL DEFAULT FALSE,
    consent_attested_at TIMESTAMP WITH TIME ZONE,
    portrait_image_url TEXT NOT NULL,
    voice_sample_url TEXT NOT NULL,
    voice_model_id TEXT, -- Vendor or self-hosted voice ID
    audio_snr_score FLOAT, -- Quality score of source audio
    face_alignment_score FLOAT, -- Quality score of source photo
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. Milestone Stories / Jobs
CREATE TYPE story_category AS ENUM (
    'bedtime_story',
    'birthday_wish',
    'milestone_congrats',
    'life_advice',
    'custom_tribute'
);

CREATE TYPE job_status AS ENUM (
    'QUEUED',
    'DENOISING_AUDIO',
    'SYNTHESIZING_VOICE',
    'ANIMATING_PORTRAIT',
    'POST_PROCESSING',
    'AWAITING_APPROVAL',
    'APPROVED',
    'REJECTED',
    'FAILED'
);

CREATE TABLE story_jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    avatar_id UUID NOT NULL REFERENCES avatar_profiles(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    category story_category NOT NULL,
    title TEXT NOT NULL,
    script_text TEXT NOT NULL,
    status job_status NOT NULL DEFAULT 'QUEUED',
    progress_percentage INTEGER DEFAULT 0,
    error_message TEXT,
    synthesized_audio_url TEXT,
    final_video_url TEXT,
    duration_seconds FLOAT,
    approved_by_guardian BOOLEAN DEFAULT FALSE,
    approved_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Row Level Security (RLS)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE avatar_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE story_jobs ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can only view their own data" 
ON avatar_profiles FOR ALL 
USING (auth.uid() = user_id);

CREATE POLICY "Users can only view their own story jobs" 
ON story_jobs FOR ALL 
USING (auth.uid() = user_id);
```

---

## 4. API Endpoints (OpenAPI / REST Specifications)

### 4.1 Authentication & Security
* `POST /api/v1/auth/signup` – Register guardian account.
* `POST /api/v1/auth/login` – Authenticate & retrieve JWT.
* `POST /api/v1/guardian/verify-pin` – Validate parent/guardian PIN for unlocking restricted views.

### 4.2 Avatar Profile Management
* `POST /api/v1/avatars/upload-url` – Generate pre-signed Cloudflare R2 / S3 URLs for photo and audio notes.
* `POST /api/v1/avatars` – Create avatar profile:
  ```json
  {
    "name": "David",
    "relationship": "Father",
    "consent_attested": true,
    "portrait_storage_key": "avatars/photo_david_123.jpg",
    "voice_storage_key": "avatars/voice_david_123.m4a"
  }
  ```
* `POST /api/v1/avatars/{avatar_id}/validate-media` – Validates resolution, face clarity, and audio SNR.

### 4.3 Story Generation & Job Engine
* `POST /api/v1/stories/draft-script` – Optional AI prompt helper (e.g. "Write a 1-minute bedtime story about space exploration for a 7-year-old").
* `POST /api/v1/stories/generate` – Dispatch rendering job:
  ```json
  {
    "avatar_id": "4b971a25-9df0-4b2a-a92e-1e43c5b8b9ef",
    "category": "bedtime_story",
    "title": "The Starlight Journey",
    "script_text": "Goodnight my champion. Look up at the stars tonight..."
  }
  ```
* `GET /api/v1/stories/{job_id}/status` – Polls state (`progress_percentage`, current phase).
* `WS /api/v1/stories/{job_id}/ws` – Real-time progress updates via WebSocket.
* `POST /api/v1/stories/{job_id}/approve` – Guardian approves the video after previewing.

---

## 5. Asynchronous Pipeline State Machine

```
[ Ingest Media: Audio & Photo ]
             │
             ▼
   [ Silero-VAD + DeepFilterNet3 ] ──► (Denoised, normalized 24kHz .wav)
             │
             ▼
   [ Voice Clone: F5-TTS / ElevenLabs ] ──► (Synthesized Speech .wav)
             │
             ▼
   [ LivePortrait / Hedra Generator ] ──► (Audio-Driven Lip-Sync Video)
             │
             ▼
   [ FFmpeg 7 Post-Processor ] ──► (Color matching, synthetic media watermark)
             │
             ▼
   [ Locked: Awaiting Guardian Review ] ──► (Only playable by Guardian with PIN)
             │
      (Guardian Approves)
             ▼
   [ Unlocked for Child Playback Vault ]
```

---

## 6. Mobile Application (React Native / Expo) Wireframe & Flow

### Screen Flow:
1. **Onboarding & Legal Attestation Screen:**
   * Empathetic introduction explaining that this is a memory companion.
   * Guardian confirmation and posthumous consent checkbox.
2. **Guardian Setup & PIN Creation:**
   * Configure 4-digit PIN / FaceID used to access settings, script editing, and approval.
3. **Media Vault (The "Memory Box"):**
   * Upload voice notes directly from WhatsApp file shares or phone recordings.
   * Real-time audio analyzer: Visual meter indicating noise level and voice clarity.
   * Photo selector: Real-time face detection ensuring eyes and lips are visible.
4. **Story Studio:**
   * Select template: *Bedtime Story*, *Birthday Card*, *Life Lesson*, or *Custom*.
   * Script editor with length counter and estimated video duration.
5. **Guardian Review Gate (Protected by PIN):**
   * High-definition video player (`expo-video`).
   * "Approve for Child" or "Regenerate / Edit Script" buttons.
6. **Child Experience ("Dad's Storybook"):**
   * Simple, distraction-free UI designed for children.
   * Displays only guardian-approved story videos in a cozy, calming interface.

---

## 7. Child Safety & App Store Compliance Checklist

* **Apple Guideline 5.1.1 & 1.2 (Impersonation / Deepfakes):**
  * Consent affidavit signed at profile creation.
  * Disallowed generation of political, harmful, or unverified public figures.
* **Synthetic Media Disclosures:**
  * Mandatory subtle watermark embedded in corner: *"Created with love by Family Memorial Companion"*.
* **Child Well-being Protection:**
  * No unrestricted freeform conversational bot mode. All dialogue is scripted and reviewed by a parent.

---

## 8. Implementation Milestones

* **Milestone 1:** Backend Media Denoising & API Contracts (FastAPI + DeepFilterNet + Celery).
* **Milestone 2:** Voice & Video Synthesis Engine (ElevenLabs/F5-TTS + LivePortrait).
* **Milestone 3:** React Native Mobile Client UI (Expo SDK 52, Media Vault, Story Creator).
* **Milestone 4:** Guardian PIN Gate & End-to-End Encryption.
* **Milestone 5:** Beta testing with select families and App Store submission.
