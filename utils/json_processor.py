"""
JSON Processing Utilities
Handles JSON file operations and structure validation
"""

import json
import logging
from typing import Dict, Any
import aiofiles

logger = logging.getLogger(__name__)

class JSONProcessor:
    """Utility class for JSON file processing and validation"""
    
    async def parse_json_file(self, json_path: str) -> Dict[str, Any]:
        """
        Parse JSON file and return structure
        
        Args:
            json_path: Path to the JSON file
            
        Returns:
            Parsed JSON structure
            
        Raises:
            Exception: If JSON parsing fails
        """
        try:
            async with aiofiles.open(json_path, 'r', encoding='utf-8') as f:
                content = await f.read()
                json_structure = json.loads(content)
            
            logger.info("Successfully parsed JSON structure file")
            return json_structure
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {str(e)}")
            raise Exception(f"Invalid JSON format: {str(e)}")
        except Exception as e:
            logger.error(f"Error reading JSON file: {str(e)}")
            raise
    
    def validate_json_structure(self, json_data: Dict[str, Any]) -> bool:
        """
        Validate JSON structure for knowledge extraction
        
        Args:
            json_data: JSON data to validate
            
        Returns:
            True if structure is valid
        """
        try:
            # Basic structure validation
            if not isinstance(json_data, dict):
                return False
            
            # Check for common required fields (can be customized)
            required_structure_indicators = [
                'topics', 'concepts', 'knowledge_points', 
                'learning_objectives', 'content', 'sections'
            ]
            
            # Check if at least one structure indicator exists
            has_valid_structure = any(
                key in str(json_data).lower() 
                for key in required_structure_indicators
            )
            
            return has_valid_structure
            
        except Exception as e:
            logger.error(f"JSON structure validation error: {str(e)}")
            return False
    
    def ensure_json_serializable(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ensure data is JSON serializable
        
        Args:
            data: Data to check and clean
            
        Returns:
            JSON serializable data
        """
        try:
            # Test serialization
            json.dumps(data, ensure_ascii=False)
            return data
        except (TypeError, ValueError) as e:
            logger.warning(f"Data serialization issue: {str(e)}")
            
            # Clean non-serializable data
            return self._clean_non_serializable(data)
    
    def _clean_non_serializable(self, obj: Any) -> Any:
        """
        Recursively clean non-serializable objects
        
        Args:
            obj: Object to clean
            
        Returns:
            Cleaned object
        """
        if isinstance(obj, dict):
            return {k: self._clean_non_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._clean_non_serializable(item) for item in obj]
        elif isinstance(obj, (str, int, float, bool)) or obj is None:
            return obj
        else:
            # Convert non-serializable objects to string
            return str(obj)