"""
LangChain Service
Handles LLM interactions and prompt management
"""

import logging
import os
from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import LangChainException
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class LangChainService:
    """Service for managing LangChain LLM interactions"""
    
    def __init__(self):
        """Initialize LangChain service with LLM configuration"""
        # Configure LLM - supports OpenAI API compatible endpoints
        self.llm = ChatOpenAI(
            model="deepseek-chat",  # Can be changed to gpt-4 or other models
            openai_api_base=os.getenv("OPENAI_API_BASE", "https://api.deepseek.com"),
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.1,  # Low temperature for consistent outputs
            max_tokens=4000
        )
        
        # JSON output parser for structured responses
        self.json_parser = JsonOutputParser()
        
        # Knowledge extraction prompt template
        self.knowledge_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert educational content analyzer. Your task is to extract knowledge points from course material and structure them according to a provided JSON template.

CRITICAL INSTRUCTIONS:
1. Extract ONLY knowledge points that are actually present in the provided text
2. Follow the EXACT structure of the provided JSON template
3. Fill in the template with relevant content from the text
4. If a section in the template has no corresponding content in the text, use null or empty values
5. Maintain the original JSON structure and field names
6. Ensure all output is valid JSON format

QUALITY REQUIREMENTS:
- Extract key concepts, definitions, examples, and important details
- Summarize complex topics clearly and concisely
- Preserve important technical terms and terminology
- Maintain logical connections between related concepts"""),
            
            ("human", """Please analyze the following course chapter and extract knowledge points according to the provided JSON structure.

CHAPTER CONTENT:
{chapter_content}

JSON STRUCTURE TEMPLATE:
{json_structure}

Extract the knowledge points from the chapter content and fill the JSON template accordingly. Return ONLY the filled JSON structure, no additional text or explanations.""")
        ])
        
        # Create the processing chain
        self.processing_chain = self.knowledge_prompt | self.llm | self.json_parser
    
    async def extract_knowledge_from_chapter(
        self, 
        chapter_content: str, 
        json_structure: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Extract knowledge points from a chapter using LangChain
        
        Args:
            chapter_content: Text content of the chapter
            json_structure: Target JSON structure for knowledge points
            
        Returns:
            Structured knowledge points in JSON format
        """
        try:
            logger.info("Starting knowledge extraction with LangChain")
            
            # Prepare inputs for the chain
            inputs = {
                "chapter_content": chapter_content,
                "json_structure": json.dumps(json_structure, indent=2, ensure_ascii=False)
            }
            
            # Process with LangChain
            result = await self.processing_chain.ainvoke(inputs)
            
            logger.info("Successfully extracted knowledge points")
            return result
            
        except LangChainException as e:
            logger.error(f"LangChain processing error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in knowledge extraction: {str(e)}")
            raise
    
    async def merge_knowledge_points(
        self, 
        extracted_points: List[Dict[str, Any]], 
        target_structure: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Merge multiple extracted knowledge points into final structure
        
        Args:
            extracted_points: List of extracted knowledge from different chapters
            target_structure: Target JSON structure
            
        Returns:
            Merged and structured knowledge points
        """
        try:
            logger.info("Starting knowledge points merge")
            
            merge_prompt = ChatPromptTemplate.from_messages([
                ("system", """You are an expert at consolidating educational content. Your task is to merge multiple knowledge point extractions into a single, comprehensive JSON structure.

INSTRUCTIONS:
1. Combine all knowledge points from different chapters
2. Eliminate duplicates while preserving unique information
3. Organize content logically within the target structure
4. Ensure comprehensive coverage of all topics
5. Maintain the exact JSON structure provided
6. Return ONLY the merged JSON, no additional text"""),
                
                ("human", """Please merge the following extracted knowledge points into the target JSON structure:

EXTRACTED KNOWLEDGE POINTS:
{extracted_points}

TARGET JSON STRUCTURE:
{target_structure}

Merge all knowledge points into a comprehensive, well-organized JSON structure.""")
            ])
            
            merge_chain = merge_prompt | self.llm | self.json_parser
            
            inputs = {
                "extracted_points": json.dumps(extracted_points, indent=2, ensure_ascii=False),
                "target_structure": json.dumps(target_structure, indent=2, ensure_ascii=False)
            }
            
            result = await merge_chain.ainvoke(inputs)
            
            logger.info("Successfully merged knowledge points")
            return result
            
        except Exception as e:
            logger.error(f"Error merging knowledge points: {str(e)}")
            raise