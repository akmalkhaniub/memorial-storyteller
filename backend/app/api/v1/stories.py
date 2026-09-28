from fastapi import APIRouter, HTTPException, status, BackgroundTasks
import uuid
from datetime import datetime
from ...models.schemas import (
    StoryGenerateRequest,
    StoryJobStatusResponse,
    JobStatus,
    GuardianApprovalRequest
)
from .avatars import AVATARS_DB

router = APIRouter(prefix="/stories", tags=["Stories"])

JOBS_DB = {}

async def run_story_pipeline(job_id: str, avatar_id: str, script_text: str):
    """
    Simulates or executes the 4-stage async generative pipeline:
    1. Denoise -> 2. Voice Clone -> 3. Video Animation -> 4. Awaiting Guardian Approval
    """
    job = JOBS_DB[job_id]
    
    # Stage 1: Denoise
    job["status"] = JobStatus.DENOISING_AUDIO
    job["progress_percentage"] = 25
    job["updated_at"] = datetime.utcnow()
    
    # Stage 2: Voice Synthesis
    job["status"] = JobStatus.SYNTHESIZING_VOICE
    job["progress_percentage"] = 55
    job["synthesized_audio_url"] = f"https://cdn.memorialstory.app/audio/{job_id}.mp3"
    job["updated_at"] = datetime.utcnow()
    
    # Stage 3: Portrait Video Generation
    job["status"] = JobStatus.ANIMATING_PORTRAIT
    job["progress_percentage"] = 85
    job["updated_at"] = datetime.utcnow()
    
    # Stage 4: Ready for Guardian Review
    job["status"] = JobStatus.AWAITING_APPROVAL
    job["progress_percentage"] = 100
    job["final_video_url"] = f"https://cdn.memorialstory.app/video/{job_id}.mp4"
    job["updated_at"] = datetime.utcnow()

@router.post("/generate", response_model=StoryJobStatusResponse, status_code=status.HTTP_202_ACCEPTED)
async def generate_story(request: StoryGenerateRequest, background_tasks: BackgroundTasks):
    if str(request.avatar_id) not in AVATARS_DB:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Avatar not found.")

    job_id = uuid.uuid4()
    now = datetime.utcnow()
    job_record = {
        "job_id": job_id,
        "avatar_id": request.avatar_id,
        "title": request.title,
        "category": request.category,
        "status": JobStatus.QUEUED,
        "progress_percentage": 0,
        "error_message": None,
        "synthesized_audio_url": None,
        "final_video_url": None,
        "approved_by_guardian": False,
        "created_at": now,
        "updated_at": now
    }
    JOBS_DB[str(job_id)] = job_record
    
    # Dispatch processing in background
    background_tasks.add_task(run_story_pipeline, str(job_id), str(request.avatar_id), request.script_text)
    
    return job_record

@router.get("/{job_id}/status", response_model=StoryJobStatusResponse)
async def get_story_status(job_id: uuid.UUID):
    record = JOBS_DB.get(str(job_id))
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Story job not found.")
    return record

@router.post("/{job_id}/approve", response_model=StoryJobStatusResponse)
async def approve_story(job_id: uuid.UUID, approval: GuardianApprovalRequest):
    record = JOBS_DB.get(str(job_id))
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Story job not found.")
    
    # Guardian PIN check (e.g. 1234 in test environment)
    if approval.guardian_pin != "1234":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Guardian PIN.")

    record["approved_by_guardian"] = approval.approve
    record["status"] = JobStatus.APPROVED if approval.approve else JobStatus.REJECTED
    record["updated_at"] = datetime.utcnow()
    return record
