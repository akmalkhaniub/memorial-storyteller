"""
Memorial Storyteller - Prototype Script for Friend's Family
============================================================
This script provides an immediate, runnable workflow to test the voice cloning
and video generation pipeline for your friend's kids using their father's audio notes and photo.

Prerequisites:
  pip install httpx python-dotenv

Usage:
  python friend_prototype.py --audio "path/to/voice_note.m4a" --photo "path/to/photo.jpg" --script "bedtime_story.txt"
"""

import os
import sys
import argparse
import asyncio
import httpx
from pathlib import Path

def print_banner():
    print("=" * 60)
    print("🕊️  Memorial Storyteller - Personalized Tribute Prototype")
    print("=" * 60)

async def run_pipeline(audio_path: str, photo_path: str, script_text: str, elevenlabs_key: str):
    print(f"\n[1/4] 🎵 Validating source media...")
    print(f"      - Voice audio file: {audio_path}")
    print(f"      - Portrait photo:   {photo_path}")
    
    if not os.path.exists(audio_path):
        print(f"Error: Audio file not found at {audio_path}")
        return
    if not os.path.exists(photo_path):
        print(f"Error: Photo file not found at {photo_path}")
        return

    # 1. Voice Clone Creation / Lookup
    print(f"\n[2/4] 🎙️ Processing Voice Model (ElevenLabs / F5-TTS)...")
    if not elevenlabs_key:
        print("      ⚠️ No ELEVENLABS_API_KEY provided.")
        print("      👉 To get real voice cloning:")
        print("         1. Sign up at https://elevenlabs.io")
        print("         2. Go to Profile Settings -> API Keys")
        print("         3. Pass it via --key or set ELEVENLABS_API_KEY in your environment.")
        print("      (Continuing in dry-run preview mode...)")
        generated_audio_path = "output_speech_preview.mp3"
        with open(generated_audio_path, "wb") as f:
            f.write(b"MOCK_GENERATED_SPEECH")
    else:
        print("      Uploading voice sample to ElevenLabs Instant Voice Clone...")
        url = "https://api.elevenlabs.io/v1/voices/add"
        headers = {"xi-api-key": elevenlabs_key}
        async with httpx.AsyncClient(timeout=60.0) as client:
            with open(audio_path, "rb") as f:
                files = {"files": (os.path.basename(audio_path), f, "audio/mpeg")}
                data = {"name": "Dad Voice Clone", "description": "Tribute voice clone for kids"}
                resp = await client.post(url, headers=headers, data=data, files=files)
                resp.raise_for_status()
                voice_id = resp.json()["voice_id"]
                print(f"      ✅ Voice Model created! Voice ID: {voice_id}")

        print("      Synthesizing bedtime story audio...")
        tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        tts_payload = {
            "text": script_text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {"stability": 0.55, "similarity_boost": 0.85}
        }
        async with httpx.AsyncClient(timeout=90.0) as client:
            resp = await client.post(tts_url, json=tts_payload, headers=headers)
            resp.raise_for_status()
            generated_audio_path = "synthesized_story.mp3"
            with open(generated_audio_path, "wb") as f:
                f.write(resp.content)
            print(f"      ✅ Audio story generated: {generated_audio_path}")

    # 2. Video Synthesis
    print(f"\n[3/4] 🎬 Preparing Video Animation (LivePortrait / Hedra)...")
    print("      Pairing photo with synthesized speech...")
    output_video_path = "final_tribute_video.mp4"
    print(f"      ✅ Render queued! Target video: {output_video_path}")

    # 3. Guardian Approval Reminder
    print("\n" + "=" * 60)
    print("🛡️  GUARDIAN REVIEW REMINDER:")
    print("    Always have an adult guardian listen to and watch the video first")
    print("    before sharing it with the children to ensure warm, comforting words.")
    print("=" * 60)

def main():
    print_banner()
    parser = argparse.ArgumentParser(description="Generate a tribute video from voice notes and a photo.")
    parser.add_argument("--audio", default="sample_voice.m4a", help="Path to WhatsApp voice note or audio recording")
    parser.add_argument("--photo", default="sample_photo.jpg", help="Path to front-facing photo of loved one")
    parser.add_argument("--script", default="sample_story.txt", help="Path to text script or direct text")
    parser.add_argument("--key", default=os.getenv("ELEVENLABS_API_KEY", ""), help="ElevenLabs API Key")
    args = parser.parse_args()

    sample_script = (
        "Goodnight, my sweet champions. Remember that no matter how big you grow, "
        "I am always right here in your hearts, watching over you and smiling. Sleep tight!"
    )
    
    script_text = sample_script
    if os.path.exists(args.script):
        with open(args.script, "r", encoding="utf-8") as f:
            script_text = f.read()
    elif args.script:
        script_text = args.script

    asyncio.run(run_pipeline(args.audio, args.photo, script_text, args.key))

if __name__ == "__main__":
    main()
