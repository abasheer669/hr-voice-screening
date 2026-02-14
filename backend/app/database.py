# backend/app/database.py

from supabase import create_client, Client
from app.config import settings
from typing import Dict
from datetime import datetime

class Database:
    def __init__(self):
        self.client: Client = create_client(
            settings.supabase_url,
            settings.supabase_service_key
        )
    
    def upload_resume_file(self, file_name: str, file_bytes: bytes) -> str:
        """Upload PDF to Supabase Storage"""
        
        # Upload to 'resumes' bucket
        self.client.storage.from_("resumes").upload(
            file_name,
            file_bytes,
            {"content-type": "application/pdf"}
        )
        
        # Get public URL
        url = self.client.storage.from_("resumes").get_public_url(file_name)
        return url
    
    def create_candidate(self, data: Dict) -> Dict:
        """Save candidate to database"""
        
        response = self.client.table("candidates").insert(data).execute()
        return response.data[0]

# Global instance
db = Database()