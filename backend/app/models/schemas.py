from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from enum import Enum
from datetime import datetime
import uuid

class StoryCategory(str, Enum):
    BEDTIME_STORY = "bedtime_story"
    BIRTHDAY_WISH = "birthday_wish"
    MILESTONE_CONGRATS = "milestone_congrats"
    LIFE_ADVICE = "life_advice"
    CUSTOM_TRIBUTE = "custom_tribute"

class JobStatus(str, Enum):
    QUEUED = "QUEUED"
    DENOISING_AUDIO = "DENOISING_AUDIO"
    SYNTHESIZING_VOICE = "SYNTHESIZING_VOICE"
    ANIMATING_PORTRAIT = "ANIMATING_PORTRAIT"
    POST_PROCESSING = "POST_PROCESSING"
    AWAITING_APPROVAL = "AWAITING_APPROVAL"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    FAILED = "FAILED"

# --- Avatar Profile Schemas ---
class AvatarCreateRequest(BaseModel):
    name: str = Field(..., example="David")
    relationship: str = Field(..., example="Father")
    consent_attested: bool = Field(..., description="Legal confirmation of kinship and posthumous consent")
    portrait_storage_key: str
    voice_storage_key: str

class AvatarResponse(BaseModel):
    id: uuid.UUID
    name: str
    relationship: str
    consent_attested: bool
    portrait_image_url: str
    voice_sample_url: str
    audio_snr_score: Optional[float] = None
    created_at: datetime

# --- Story Job Schemas ---
class StoryGenerateRequest(BaseModel):
    avatar_id: uuid.UUID
    category: StoryCategory
    title: str = Field(..., example="The Starlight Journey")
    script_text: str = Field(..., min_length=10, max_length=2000, description="The text to be spoken by the avatar")

class StoryJobStatusResponse(BaseModel):
    job_id: uuid.UUID
    avatar_id: uuid.UUID
    title: str
    category: StoryCategory
    status: JobStatus
    progress_percentage: int
    error_message: Optional[str] = None
    synthesized_audio_url: Optional[str] = None
    final_video_url: Optional[str] = None
    approved_by_guardian: bool = False
    created_at: datetime
    updated_at: datetime

class GuardianApprovalRequest(BaseModel):
    guardian_pin: str = Field(..., min_length=4, max_length=6)
    approve: bool

# --- AI Script Co-Pilot Schemas ---
class ScriptAssistRequest(BaseModel):
    occasion: StoryCategory
    child_name: Optional[str] = Field(None, example="Leo")
    favorite_memory: Optional[str] = Field(None, example="Building Lego towers on Sunday mornings")
    custom_notes: Optional[str] = Field(None, example="Remind him to keep practicing his soccer kicks")

class ScriptAssistResponse(BaseModel):
    occasion: StoryCategory
    suggested_title: str
    script_text: str
    estimated_duration_seconds: int

# --- Pre-signed Media Upload Schemas ---
class PresignedUploadRequest(BaseModel):
    file_extension: str = Field(..., example=".m4a")
    content_type: str = Field(..., example="audio/mp4")

class PresignedUploadResponse(BaseModel):
    storage_key: str
    upload_url: str
    content_type: str
    expires_in_seconds: int

