from fastapi import APIRouter, HTTPException, status
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
from ...services.engine_orchestrator import engine_settings, VoiceProvider, VideoProvider

router = APIRouter(prefix="/admin", tags=["Admin Control Panel"])

class UpdateEngineSettingsRequest(BaseModel):
    voice_provider: Optional[VoiceProvider] = None
    video_provider: Optional[VideoProvider] = None

@router.get("/engine-settings")
async def get_engine_settings():
    """
    Returns current active generative AI providers and health status.
    """
    return engine_settings.get_status()

@router.post("/engine-settings")
async def update_engine_settings(request: UpdateEngineSettingsRequest):
    """
    Switches active generative AI engine on the fly without downtime.
    """
    engine_settings.update_settings(
        voice_provider=request.voice_provider,
        video_provider=request.video_provider
    )
    return {
        "status": "success",
        "message": "Engine settings updated successfully",
        "current_state": engine_settings.get_status()
    }

@router.get("/dashboard", response_class=HTMLResponse)
async def admin_dashboard():
    """
    Visual Web Admin Control Panel to toggle between ElevenLabs and In-House F5-TTS / LivePortrait.
    """
    status_data = engine_settings.get_status()
    active_voice = status_data["active_voice_provider"]
    active_video = status_data["active_video_provider"]

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Memorial Storyteller - AI Engine Control Panel</title>
        <style>
            :root {{
                --bg: #0b0f19;
                --surface: #161e2e;
                --surface-hover: #1e293b;
                --primary: #38bdf8;
                --success: #10b981;
                --text: #f8fafc;
                --text-muted: #94a3b8;
                --border: #334155;
            }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                background-color: var(--bg);
                color: var(--text);
                margin: 0;
                padding: 40px 20px;
                display: flex;
                justify-content: center;
            }}
            .container {{
                max-width: 800px;
                width: 100%;
            }}
            .header {{
                margin-bottom: 30px;
            }}
            .header h1 {{
                font-size: 28px;
                margin: 0 0 8px 0;
                display: flex;
                align-items: center;
                gap: 12px;
            }}
            .header p {{
                color: var(--text-muted);
                margin: 0;
            }}
            .card {{
                background-color: var(--surface);
                border: 1px solid var(--border);
                border-radius: 16px;
                padding: 24px;
                margin-bottom: 24px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
            }}
            .card-title {{
                font-size: 18px;
                font-weight: 600;
                margin-bottom: 6px;
            }}
            .card-desc {{
                color: var(--text-muted);
                font-size: 14px;
                margin-bottom: 20px;
            }}
            .toggle-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 12px;
            }}
            .toggle-btn {{
                background: #0f172a;
                border: 2px solid var(--border);
                color: var(--text);
                padding: 16px;
                border-radius: 12px;
                cursor: pointer;
                text-align: left;
                transition: all 0.2s ease;
            }}
            .toggle-btn:hover {{
                border-color: var(--primary);
                background: var(--surface-hover);
            }}
            .toggle-btn.active {{
                border-color: var(--primary);
                background: rgba(56, 189, 248, 0.1);
            }}
            .btn-title {{
                font-weight: 700;
                font-size: 15px;
                margin-bottom: 4px;
                display: block;
            }}
            .btn-subtitle {{
                font-size: 12px;
                color: var(--text-muted);
            }}
            .cost-banner {{
                background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(56, 189, 248, 0.1));
                border: 1px solid rgba(16, 185, 129, 0.3);
                border-radius: 12px;
                padding: 16px 20px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-top: 10px;
            }}
            .cost-label {{
                font-size: 14px;
                color: var(--text-muted);
            }}
            .cost-value {{
                font-size: 20px;
                font-weight: 800;
                color: var(--success);
            }}
            .badge {{
                display: inline-block;
                padding: 3px 8px;
                font-size: 11px;
                font-weight: 700;
                border-radius: 6px;
                background: #334155;
                color: #e2e8f0;
                margin-left: 8px;
            }}
            .badge-active {{
                background: var(--success);
                color: #064e3b;
            }}
            #save-toast {{
                display: none;
                position: fixed;
                bottom: 24px;
                right: 24px;
                background: var(--success);
                color: #064e3b;
                padding: 12px 20px;
                border-radius: 10px;
                font-weight: 700;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎛️ Generative Engine Switchboard</h1>
                <p>Hot-swap AI generation backends in real time without downtime or server restarts.</p>
            </div>

            <!-- Voice Engine Card -->
            <div class="card">
                <div class="card-title">1. Voice Synthesis Engine</div>
                <div class="card-desc">Choose between zero-maintenance managed APIs or private in-house models.</div>
                
                <div class="toggle-grid">
                    <button class="toggle-btn {'active' if active_voice == 'elevenlabs' else ''}" onclick="setVoice('elevenlabs')">
                        <span class="btn-title">ElevenLabs API</span>
                        <span class="btn-subtitle">Managed Cloud • Instant Setup • ~$0.30/min</span>
                    </button>

                    <button class="toggle-btn {'active' if active_voice == 'self_hosted_f5tts' else ''}" onclick="setVoice('self_hosted_f5tts')">
                        <span class="btn-title">In-House F5-TTS</span>
                        <span class="btn-subtitle">Flow Matching DiT • 100% Private • ~$0.005/min</span>
                    </button>

                    <button class="toggle-btn {'active' if active_voice == 'auto_fallback' else ''}" onclick="setVoice('auto_fallback')">
                        <span class="btn-title">Auto-Optimizer & Fallback</span>
                        <span class="btn-subtitle">Uses F5-TTS first, fails over to ElevenLabs</span>
                    </button>
                </div>
            </div>

            <!-- Video Engine Card -->
            <div class="card">
                <div class="card-title">2. Video Portrait Animation Engine</div>
                <div class="card-desc">Select how photos are animated to sync with synthesized speech.</div>
                
                <div class="toggle-grid">
                    <button class="toggle-btn {'active' if active_video == 'hedra' else ''}" onclick="setVideo('hedra')">
                        <span class="btn-title">Hedra / HeyGen API</span>
                        <span class="btn-subtitle">Managed Portrait Generator</span>
                    </button>

                    <button class="toggle-btn {'active' if active_video == 'self_hosted_liveportrait' else ''}" onclick="setVideo('self_hosted_liveportrait')">
                        <span class="btn-title">In-House LivePortrait</span>
                        <span class="btn-subtitle">Implicit Motion Transfer on Modal GPU</span>
                    </button>

                    <button class="toggle-btn {'active' if active_video == 'auto_fallback' else ''}" onclick="setVideo('auto_fallback')">
                        <span class="btn-title">Auto-Fallback</span>
                        <span class="btn-subtitle">Dynamic failover resilience</span>
                    </button>
                </div>
            </div>

            <!-- Cost Comparison Box -->
            <div class="cost-banner">
                <div>
                    <div class="cost-label">In-House Cost Savings</div>
                    <div style="font-size: 13px; color: var(--text);">F5-TTS & LivePortrait reduce generative costs by:</div>
                </div>
                <div class="cost-value">~98.3%</div>
            </div>
        </div>

        <div id="save-toast">✓ Settings Updated Live!</div>

        <script>
            async function updateEngine(voice, video) {{
                const payload = {{}};
                if (voice) payload.voice_provider = voice;
                if (video) payload.video_provider = video;

                const res = await fetch('/api/v1/admin/engine-settings', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify(payload)
                }});
                
                if (res.ok) {{
                    const toast = document.getElementById('save-toast');
                    toast.style.display = 'block';
                    setTimeout(() => {{ toast.style.display = 'none'; location.reload(); }}, 600);
                }}
            }}

            function setVoice(provider) {{ updateEngine(provider, null); }}
            function setVideo(provider) {{ updateEngine(null, provider); }}
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
