"""
LangChain PDF Knowledge Extraction Server
Main FastAPI application entry point
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
import logging
from typing import Dict, Any
import aiofiles
import os
from datetime import datetime

from services.pdf_processor import PDFProcessor
from services.langchain_service import LangChainService
from services.knowledge_extractor import KnowledgeExtractor
from models.schemas import ProcessResponse, ErrorResponse
from utils.file_validator import FileValidator
from utils.json_processor import JSONProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="LangChain PDF Knowledge Extraction API",
    description="Extract and structure knowledge points from course PDFs using LangChain",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
pdf_processor = PDFProcessor()
langchain_service = LangChainService()
knowledge_extractor = KnowledgeExtractor(langchain_service)
file_validator = FileValidator()
json_processor = JSONProcessor()

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "LangChain PDF Knowledge Extraction API", "status": "running"}

@app.post("/process", response_model=ProcessResponse)
async def process_files(
    pdf_file: UploadFile = File(..., description="Course PDF file"),
    json_file: UploadFile = File(..., description="Knowledge structure JSON file")
):
    """
    Process PDF and JSON files to extract structured knowledge points
    
    Args:
        pdf_file: Course content in PDF format
        json_file: Predefined knowledge structure in JSON format
    
    Returns:
        ProcessResponse: Structured knowledge points following input JSON format
    """
    try:
        # Validate uploaded files
        logger.info(f"Processing files - PDF: {pdf_file.filename}, JSON: {json_file.filename}")
        
        await file_validator.validate_pdf(pdf_file)
        await file_validator.validate_json(json_file)
        
        # Save uploaded files temporarily
        temp_dir = "temp_uploads"
        os.makedirs(temp_dir, exist_ok=True)
        
        pdf_path = f"{temp_dir}/{pdf_file.filename}"
        json_path = f"{temp_dir}/{json_file.filename}"
        
        # Save PDF file
        async with aiofiles.open(pdf_path, 'wb') as f:
            content = await pdf_file.read()
            await f.write(content)
        
        # Save and parse JSON file
        async with aiofiles.open(json_path, 'wb') as f:
            json_content = await json_file.read()
            await f.write(json_content)
        
        # Parse JSON structure
        knowledge_structure = await json_processor.parse_json_file(json_path)
        logger.info("Successfully parsed knowledge structure JSON")
        
        # Extract PDF content by chapters
        pdf_chapters = await pdf_processor.extract_chapters(pdf_path)
        logger.info(f"Extracted {len(pdf_chapters)} chapters from PDF")
        
        # Process each chapter with LangChain
        structured_knowledge = await knowledge_extractor.extract_knowledge_points(
            pdf_chapters, knowledge_structure
        )
        
        # Cleanup temporary files
        os.remove(pdf_path)
        os.remove(json_path)
        
        logger.info("Successfully processed files and extracted knowledge points")
        
        return ProcessResponse(
            success=True,
            message="Knowledge points extracted successfully",
            data=structured_knowledge,
            processed_at=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Error processing files: {str(e)}")
        
        # Cleanup on error
        for file_path in [pdf_path, json_path]:
            if 'file_path' in locals() and os.path.exists(file_path):
                os.remove(file_path)
        
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process files: {str(e)}"
        )

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unexpected errors"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            success=False,
            message="Internal server error",
            error=str(exc)
        ).dict()
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)