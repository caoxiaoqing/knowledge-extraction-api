# LangChain PDF Knowledge Extraction API

A comprehensive server application that extracts structured knowledge points from course PDF files using LangChain and large language models.

## Features

- **PDF Processing**: Extract text content from course PDFs with chapter segmentation
- **LangChain Integration**: Use advanced LLM capabilities for knowledge extraction  
- **Structured Output**: Extract knowledge points according to predefined JSON templates
- **Concurrent Processing**: Process multiple chapters simultaneously with rate limiting
- **File Validation**: Robust validation for uploaded PDF and JSON files
- **Error Handling**: Comprehensive error handling and logging
- **Scalable Architecture**: Modular design for easy extension and maintenance

## Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **LangChain**: Framework for developing applications with LLMs
- **PyPDF**: PDF text extraction
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server for production deployment

## Installation

1. Clone the repository and navigate to the project directory:
```bash
cd langchain-pdf-processor
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env file with your API keys and configuration
```

4. Start the development server:
```bash
uvicorn main:app --reload
```

## API Usage

### Process Files Endpoint

**POST** `/process`

Upload a course PDF and knowledge structure JSON to extract structured knowledge points.

**Request:**
- Content-Type: `multipart/form-data`
- `pdf_file`: Course content in PDF format
- `json_file`: Knowledge structure template in JSON format

**Response:**
```json
{
  "success": true,
  "message": "Knowledge points extracted successfully",
  "data": {
    // Structured knowledge points following input JSON format
  },
  "processed_at": "2025-01-11T10:30:00"
}
```

### Example JSON Structure

```json
{
  "course_title": "",
  "topics": [
    {
      "topic_name": "",
      "concepts": [
        {
          "concept_name": "",
          "definition": "",
          "examples": [],
          "key_points": []
        }
      ]
    }
  ],
  "learning_objectives": [],
  "summary": ""
}
```

## Configuration

Key environment variables:

- `OPENAI_API_KEY`: Your LLM API key (required)
- `OPENAI_API_BASE`: API base URL (default: DeepSeek API)
- `LLM_MODEL`: Model name (default: deepseek-chat)
- `MAX_CONCURRENT_CHAPTERS`: Concurrent processing limit (default: 3)

## Architecture

```
├── main.py                 # FastAPI application entry point
├── services/              # Business logic services
│   ├── pdf_processor.py   # PDF extraction and chapter splitting
│   ├── langchain_service.py # LLM interactions
│   └── knowledge_extractor.py # Main extraction orchestration
├── models/               # Pydantic models and schemas
│   └── schemas.py       
├── utils/               # Utility functions
│   ├── file_validator.py # File validation
│   └── json_processor.py # JSON operations
└── config/             # Configuration management
    └── settings.py     
```

## Development

The application is structured with clear separation of concerns:

- **Services**: Handle business logic and external integrations
- **Models**: Define data structures and validation rules
- **Utils**: Provide reusable utility functions
- **Config**: Manage application configuration and settings

## Error Handling

The application includes comprehensive error handling:

- File validation errors (format, size, content)
- LLM API errors and retries
- JSON parsing and structure validation errors
- Processing timeouts and resource limits

## Logging

All major operations are logged with appropriate log levels:
- INFO: Normal operation flow
- WARNING: Recoverable issues
- ERROR: Processing failures and exceptions

## Production Deployment

For production deployment:

1. Set appropriate environment variables
2. Use a production ASGI server like Gunicorn with Uvicorn workers
3. Configure proper logging and monitoring
4. Set up file storage for temporary uploads
5. Implement proper security measures (authentication, rate limiting)

## API Documentation

Once running, visit:
- **Interactive API docs**: http://localhost:8000/docs
- **Alternative docs**: http://localhost:8000/redoc