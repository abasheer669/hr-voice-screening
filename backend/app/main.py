# backend/app/main.py

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.database import db
from app.services.resume_parser import parser
from datetime import datetime
import uuid

app = FastAPI(title="Resume Upload API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi import FastAPI, UploadFile, File, Form, HTTPException

@app.post("/api/upload-resume")
async def upload_resume(
    file: UploadFile = File(...),
    job_id: str = Form(...),
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...)
):
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(400, "Only PDF files are allowed")

    try:
        # Read file bytes
        file_bytes = await file.read()

        # Optional: Extract text if you want
        resume_text = parser.extract_text_from_bytes(file_bytes) if file_bytes else None

        # Upload PDF to Supabase Storage
        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        resume_url = db.upload_resume_file(unique_filename, file_bytes)

        # Create candidate record using form data
        candidate_data = {
            "name": name,
            "email": email,
            "phone": phone,
            "resume_url": resume_url,
            "resume_text": resume_text,
            "job_id": job_id,
            "status": "pending",
        }

        candidate = db.create_candidate(candidate_data)

        return {
            "success": True,
            "message": "Resume uploaded successfully",
            "candidate": candidate
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(500, f"Upload failed: {str(e)}")

    """
    Upload resume PDF and extract basic info
    
    Steps:
    1. Read PDF file
    2. Extract text
    3. Parse name, email, phone
    4. Upload PDF to Supabase Storage
    5. Save candidate to Supabase Database
    """
    
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(400, "Only PDF files are allowed")
    
    try:
        # Step 1: Read file bytes
        file_bytes = await file.read()
        
        # Step 2: Extract text from PDF
        resume_text = parser.extract_text_from_bytes(file_bytes)
        
        if not resume_text:
            raise HTTPException(400, "Could not extract text from PDF")
        
        # Step 3: Extract contact information
        contact_info = parser.extract_contact_info(resume_text)
        
        # Step 4: Upload PDF to Supabase Storage
        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        resume_url = db.upload_resume_file(unique_filename, file_bytes)
        
        # Step 5: Create candidate record in database
        candidate_data = {
            "name": contact_info.get("name") or "Unknown",
            "email": contact_info.get("email"),
            "phone": contact_info.get("phone"),
            "resume_url": resume_url,
            "resume_text": resume_text,
            "job_id": job_id,
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }
        
        candidate = db.create_candidate(candidate_data)
        
        # Return success response
        return {
            "success": True,
            "message": "Resume uploaded successfully",
            "candidate": {
                "id": candidate["id"],
                "name": candidate["name"],
                "email": candidate["email"],
                "phone": candidate["phone"],
                "resume_url": candidate["resume_url"]
            }
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(500, f"Upload failed: {str(e)}")

@app.get("/api/candidates/{candidate_id}")
async def get_candidate(candidate_id: str):
    """Get candidate by ID"""
    
    try:
        response = db.client.table("candidates").select("*").eq("id", candidate_id).execute()
        
        if not response.data:
            raise HTTPException(404, "Candidate not found")
        
        return response.data[0]
        
    except Exception as e:
        raise HTTPException(500, f"Failed to get candidate: {str(e)}")

@app.get("/")
async def root():
    return {
        "message": "Resume Upload API",
        "endpoints": {
            "upload": "POST /api/upload-resume",
            "get_candidate": "GET /api/candidates/{id}"
        }
    }