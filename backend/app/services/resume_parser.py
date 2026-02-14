# backend/app/services/resume_parser.py

import PyPDF2
import io
import re
from typing import Dict

class ResumeParser:
    
    def extract_text_from_bytes(self, file_bytes: bytes) -> str:
        """Extract text from PDF bytes"""
        
        pdf_file = io.BytesIO(file_bytes)
        reader = PyPDF2.PdfReader(pdf_file)
        
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        
        return text.strip()
    
    def extract_contact_info(self, text: str) -> Dict[str, str]:
        """Extract name, email, phone from text"""
        
        result = {
            "name": None,
            "email": None,
            "phone": None
        }
        
        # Extract email
        email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
        emails = re.findall(email_pattern, text)
        if emails:
            result["email"] = emails[0]
        
        # Extract phone
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phones = re.findall(phone_pattern, text)
        if phones:
            # Clean up phone number
            phone = ''.join(phones[0]) if isinstance(phones[0], tuple) else phones[0]
            result["phone"] = phone.strip()
        
        # Extract name (usually first bold/large text or first line)
        # Try to find name pattern: FirstName LastName
        name_pattern = r'^([A-Z][a-z]+\s+[A-Z][a-z]+)'
        lines = text.split('\n')
        for line in lines[:5]:  # Check first 5 lines
            line = line.strip()
            if len(line) > 0:
                name_match = re.match(name_pattern, line)
                if name_match:
                    result["name"] = name_match.group(1)
                    break
        
        # If still no name, use first non-empty line
        if not result["name"]:
            for line in lines[:3]:
                line = line.strip()
                if len(line) > 0 and len(line) < 50:
                    result["name"] = line
                    break
        
        return result

# Global instance
parser = ResumeParser()