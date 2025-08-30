"""
File Validation Utilities
Validates uploaded files for security and format compliance
"""

import logging
from fastapi import UploadFile, HTTPException
import json
import magic
import os

logger = logging.getLogger(__name__)

class FileValidator:
    """Utility class for validating uploaded files"""
    
    def __init__(self):
        self.max_file_size = 50 * 1024 * 1024  # 50MB max file size
        self.allowed_pdf_types = ["application/pdf"]
        self.allowed_json_types = ["application/json", "text/plain"]
    
    async def validate_pdf(self, pdf_file: UploadFile) -> None:
        """
        Validate PDF file upload
        
        Args:
            pdf_file: Uploaded PDF file
            
        Raises:
            HTTPException: If validation fails
        """
        # Check file extension
        if not pdf_file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=400,
                detail="File must have .pdf extension"
            )
        
        # Check file size
        file_content = await pdf_file.read()
        if len(file_content) > self.max_file_size:
            raise HTTPException(
                status_code=400,
                detail=f"PDF file too large. Maximum size: {self.max_file_size // (1024*1024)}MB"
            )
        
        # Reset file pointer
        await pdf_file.seek(0)
        
        # Validate PDF content type (basic check)
        if not file_content.startswith(b'%PDF'):
            raise HTTPException(
                status_code=400,
                detail="Invalid PDF file format"
            )
        
        logger.info(f"PDF file validation successful: {pdf_file.filename}")
    
    async def validate_json(self, json_file: UploadFile) -> None:
        """
        Validate JSON file upload
        
        Args:
            json_file: Uploaded JSON file
            
        Raises:
            HTTPException: If validation fails
        """
        # Check file extension
        if not json_file.filename.lower().endswith('.json'):
            raise HTTPException(
                status_code=400,
                detail="File must have .json extension"
            )
        
        # Check file size
        file_content = await json_file.read()
        if len(file_content) > 10 * 1024 * 1024:  # 10MB for JSON
            raise HTTPException(
                status_code=400,
                detail="JSON file too large. Maximum size: 10MB"
            )
        
        # Validate JSON format
        try:
            json_content = json.loads(file_content.decode('utf-8'))
            if not isinstance(json_content, dict):
                raise HTTPException(
                    status_code=400,
                    detail="JSON file must contain a valid object structure"
                )
        except json.JSONDecodeError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid JSON format: {str(e)}"
            )
        except UnicodeDecodeError:
            raise HTTPException(
                status_code=400,
                detail="JSON file must be UTF-8 encoded"
            )
        
        # Reset file pointer
        await json_file.seek(0)
        
        logger.info(f"JSON file validation successful: {json_file.filename}")
    
    def validate_file_size(self, file_path: str, max_size: int) -> bool:
        """
        Validate file size
        
        Args:
            file_path: Path to the file
            max_size: Maximum allowed size in bytes
            
        Returns:
            True if file size is valid
        """
        if not os.path.exists(file_path):
            return False
        
        file_size = os.path.getsize(file_path)
        return file_size <= max_size