"""
Knowledge Extraction Service
Orchestrates the complete knowledge extraction process
"""

import logging
from typing import List, Dict, Any
from services.langchain_service import LangChainService
import asyncio

logger = logging.getLogger(__name__)

class KnowledgeExtractor:
    """Main service for orchestrating knowledge extraction process"""
    
    def __init__(self, langchain_service: LangChainService):
        self.langchain_service = langchain_service
        self.max_concurrent_requests = 3  # Limit concurrent API calls
    
    async def extract_knowledge_points(
        self, 
        chapters: List[Dict[str, str]], 
        knowledge_structure: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Extract knowledge points from all chapters and structure them
        
        Args:
            chapters: List of chapter dictionaries with content
            knowledge_structure: Target JSON structure for knowledge points
            
        Returns:
            Complete structured knowledge points
        """
        try:
            logger.info(f"Starting knowledge extraction for {len(chapters)} chapters")
            
            # Create semaphore to limit concurrent requests
            semaphore = asyncio.Semaphore(self.max_concurrent_requests)
            
            # Process chapters concurrently with rate limiting
            tasks = []
            for chapter in chapters:
                task = self._process_chapter_with_semaphore(
                    semaphore, chapter, knowledge_structure
                )
                tasks.append(task)
            
            # Execute all chapter processing tasks
            chapter_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Filter successful results and log errors
            successful_results = []
            for i, result in enumerate(chapter_results):
                if isinstance(result, Exception):
                    logger.error(f"Failed to process chapter {i + 1}: {str(result)}")
                else:
                    successful_results.append(result)
            
            if not successful_results:
                raise Exception("Failed to process any chapters successfully")
            
            logger.info(f"Successfully processed {len(successful_results)} chapters")
            
            # Merge all chapter results into final structure
            final_knowledge = await self.langchain_service.merge_knowledge_points(
                successful_results, knowledge_structure
            )
            
            return final_knowledge
            
        except Exception as e:
            logger.error(f"Error in knowledge extraction process: {str(e)}")
            raise
    
    async def _process_chapter_with_semaphore(
        self, 
        semaphore: asyncio.Semaphore, 
        chapter: Dict[str, str], 
        knowledge_structure: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process a single chapter with concurrency control
        
        Args:
            semaphore: Asyncio semaphore for rate limiting
            chapter: Chapter dictionary with content
            knowledge_structure: Target JSON structure
            
        Returns:
            Extracted knowledge points for the chapter
        """
        async with semaphore:
            try:
                logger.info(f"Processing chapter: {chapter['title']}")
                
                result = await self.langchain_service.extract_knowledge_from_chapter(
                    chapter['content'], knowledge_structure
                )
                
                # Add chapter metadata to result
                result['_chapter_info'] = {
                    "chapter_number": chapter['chapter_number'],
                    "title": chapter['title']
                }
                
                logger.info(f"Completed processing chapter: {chapter['title']}")
                return result
                
            except Exception as e:
                logger.error(f"Error processing chapter {chapter['title']}: {str(e)}")
                raise