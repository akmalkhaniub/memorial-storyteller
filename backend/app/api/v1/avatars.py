from fastapi import APIRouter, HTTPException, status
import uuid
from datetime import datetime
from ...models.schemas import AvatarCreateRequest, AvatarResponse

router = APIRouter(prefix="/avatars", tags=["Avatars"])

# In-memory store for rapid prototyping / testing
AVATARS_DB = {}

@router.post("", response_model=AvatarResponse, status_code=status.HTTP_201_CREATED)
async def create_avatar(request: AvatarCreateRequest):
    if not request.consent_attested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Posthumous consent and guardianship attestation must be accepted."
        )

    avatar_id = uuid.uuid4()
    avatar_record = {
        "id": avatar_id,
        "name": request.name,
        "relationship": request.relationship,
        "consent_attested": request.consent_attested,
        "portrait_image_url": f"https://cdn.memorialstory.app/{request.portrait_storage_key}",
        "voice_sample_url": f"https://cdn.memorialstory.app/{request.voice_storage_key}",
        "audio_snr_score": 24.5,
        "created_at": datetime.utcnow()
    }
    AVATARS_DB[str(avatar_id)] = avatar_record
    return avatar_record

@router.get("/{avatar_id}", response_model=AvatarResponse)
async def get_avatar(avatar_id: uuid.UUID):
    record = AVATARS_DB.get(str(avatar_id))
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Avatar profile not found.")
    return record
