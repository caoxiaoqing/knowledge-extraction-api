"""
PDF Processing Service
Handles PDF file loading, text extraction, and chapter segmentation
"""

import logging
from typing import List, Dict
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import re

logger = logging.getLogger(__name__)

class PDFProcessor:
    """Service for processing PDF files and extracting content"""
    
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=4000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    async def extract_chapters(self, pdf_path: str) -> List[Dict[str, str]]:
        """
        Extract chapters from PDF file
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List of dictionaries containing chapter information
        """
        try:
            logger.info(f"Starting PDF extraction from: {pdf_path}")
            
            # Load PDF using LangChain PyPDFLoader
            loader = PyPDFLoader(pdf_path)
            documents = loader.load()
            
            logger.info(f"Loaded {len(documents)} pages from PDF")
            
            # Combine all pages content
            full_text = "\n".join([doc.page_content for doc in documents])
            
            # Split into chapters using common patterns
            chapters = self._split_into_chapters(full_text)
            
            # If no clear chapters found, split by text chunks
            if len(chapters) <= 1:
                chapters = self._split_by_chunks(full_text)
            
            logger.info(f"Successfully extracted {len(chapters)} chapters")
            return chapters
            
        except Exception as e:
            logger.error(f"Error extracting PDF chapters: {str(e)}")
            raise
    
    def _split_into_chapters(self, text: str) -> List[Dict[str, str]]:
        """
        Split text into chapters based on common patterns
        
        Args:
            text: Full text content
            
        Returns:
            List of chapter dictionaries
        """
        # Common chapter patterns
        chapter_patterns = [
            r'第[一二三四五六七八九十\d]+章.*?(?=第[一二三四五六七八九十\d]+章|$)',
            r'Chapter\s+\d+.*?(?=Chapter\s+\d+|$)',
            r'CHAPTER\s+\d+.*?(?=CHAPTER\s+\d+|$)',
            r'\n\d+\..*?(?=\n\d+\.|$)',
            r'\n[A-Z][^.]*\n.*?(?=\n[A-Z][^.]*\n|$)'
        ]
        
        chapters = []
        
        for pattern in chapter_patterns:
            matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)
            if matches and len(matches) > 1:
                for i, match in enumerate(matches):
                    chapter_title = self._extract_chapter_title(match)
                    chapters.append({
                        "chapter_number": i + 1,
                        "title": chapter_title,
                        "content": match.strip()
                    })
                break
        
        # If no patterns matched, return whole text as single chapter
        if not chapters:
            chapters = [{
                "chapter_number": 1,
                "title": "Complete Document",
                "content": text.strip()
            }]
        
        return chapters
    
    def _split_by_chunks(self, text: str) -> List[Dict[str, str]]:
        """
        Split text into manageable chunks when no clear chapter structure exists
        
        Args:
            text: Full text content
            
        Returns:
            List of chunk dictionaries
        """
        chunks = self.text_splitter.split_text(text)
        
        chapters = []
        for i, chunk in enumerate(chunks):
            chapters.append({
                "chapter_number": i + 1,
                "title": f"Section {i + 1}",
                "content": chunk.strip()
            })
        
        return chapters
    
    def _extract_chapter_title(self, chapter_text: str) -> str:
        """
        Extract chapter title from chapter text
        
        Args:
            chapter_text: Text content of the chapter
            
        Returns:
            Extracted chapter title
        """
        lines = chapter_text.strip().split('\n')
        
        # Try to find a clear title in the first few lines
        for line in lines[:3]:
            line = line.strip()
            if line and len(line) < 100:  # Reasonable title length
                return line
        
        # Fallback to first non-empty line
        for line in lines:
            line = line.strip()
            if line:
                return line[:100] + "..." if len(line) > 100 else line
        
        return "Untitled Chapter"