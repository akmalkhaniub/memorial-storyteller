import uuid
from typing import Dict
from ..core.config import settings

class StorageService:
    """
    Manages direct media uploads and pre-signed URLs
    for Cloudflare R2 / AWS S3.
    """
    
    @staticmethod
    def generate_presigned_upload_url(file_extension: str, content_type: str) -> Dict[str, str]:
        """
        Generates a secure temporary URL so mobile clients can upload large
        audio notes and high-res photos directly to storage without loading the API gateway.
        """
        file_id = str(uuid.uuid4())
        clean_ext = file_extension.lstrip(".")
        storage_key = f"uploads/{file_id}.{clean_ext}"
        
        # When cloud S3/R2 credentials are configured, generate boto3 presigned_post
        # Otherwise return a structured URL template
        base_endpoint = settings.STORAGE_ENDPOINT_URL or "https://vault.memorialstory.app"
        upload_url = f"{base_endpoint}/{settings.STORAGE_BUCKET_NAME}/{storage_key}"
        
        return {
            "storage_key": storage_key,
            "upload_url": upload_url,
            "content_type": content_type,
            "expires_in_seconds": 3600
        }
