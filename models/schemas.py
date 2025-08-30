"""
Pydantic Models and Schemas
Data validation and response models
"""

from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime

class ProcessResponse(BaseModel):
    """Response model for successful processing"""
    success: bool = Field(True, description="Processing success status")
    message: str = Field(..., description="Response message")
    data: Dict[str, Any] = Field(..., description="Extracted knowledge points")
    processed_at: str = Field(..., description="Processing timestamp")

class ErrorResponse(BaseModel):
    """Response model for error cases"""
    success: bool = Field(False, description="Processing success status")
    message: str = Field(..., description="Error message")
    error: Optional[str] = Field(None, description="Detailed error information")

class ChapterInfo(BaseModel):
    """Model for chapter information"""
    chapter_number: int = Field(..., description="Chapter number")
    title: str = Field(..., description="Chapter title")
    content: str = Field(..., description="Chapter content")

class ProcessingConfig(BaseModel):
    """Configuration model for processing parameters"""
    max_concurrent_chapters: int = Field(3, description="Maximum concurrent chapter processing")
    chunk_size: int = Field(4000, description="Text chunk size for processing")
    chunk_overlap: int = Field(200, description="Overlap between text chunks")
    temperature: float = Field(0.1, description="LLM temperature for consistency")

class KnowledgeStructure(BaseModel):
    """Model for knowledge structure validation"""
    structure: Dict[str, Any] = Field(..., description="JSON structure template")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }