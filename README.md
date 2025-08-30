# Knowledge Extraction API

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
cd knowledge-point-extraction-system-backend
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

if everything goes well, you will see
```bash
INFO:     Will watch for changes in these directories: ['/path/to/your/knowledge-point-extraction-system-backend']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [PID]
INFO:     Started server process [PID]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

this means your FastAPI service is running on http://localhost:8000


## API Usage

你可以通过以下两种主要方式测试 `/process` 接口：

### a. 使用 FastAPI 自动生成的 Swagger UI (推荐)
1. 打开你的浏览器，访问：http://localhost:8000/docs
2. 你将看到 FastAPI 自动生成的交互式 API 文档 (Swagger UI)。
3. 找到 /process 端点，点击展开。
4. 点击 "Try it out" 按钮。
5. 你将看到 pdf_file 和 json_file 的文件上传字段。
6. 准备测试文件:
  - PDF 文件: 准备一个课程内容的 PDF 文件。你可以使用任何 PDF 文件进行测试。
  - JSON 文件: 使用项目根目录下的 examples/example_knowledge_structure.json 作为你的知识结构模板。你可以根据需要修改它。
7. 点击 pdf_file 和 json_file 字段旁边的 "Choose File" 按钮，上传你准备好的 PDF 和 JSON 文件。
8. 点击 "Execute" 按钮。
9. 你将在 "Responses" 部分看到 API 的响应，包括状态码、响应体 (JSON 格式的提取结果) 和响应头。

### b. 使用 curl 命令 (命令行测试)
如果你更喜欢在命令行中测试，可以使用 curl。你需要准备好 PDF 和 JSON 文件。

假设你的 PDF 文件名为 course.pdf，JSON 文件名为 structure.json，并且它们都在你运行 curl 命令的当前目录下。

```bash
curl -X POST "http://localhost:8000/process" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "pdf_file=@course.pdf;type=application/pdf" \
  -F "json_file=@structure.json;type=application/json"
```

- -X POST: 指定 HTTP 方法为 POST。
- "http://localhost:8000/process": API 端点 URL。
- -H "accept: application/json": 告诉服务器你期望 JSON 格式的响应。
- -H "Content-Type: multipart/form-data": 指定请求体类型为 multipart/form-data，因为是文件上传。
- -F "pdf_file=@course.pdf;type=application/pdf": 上传名为 course.pdf 的文件作为 pdf_file 字段，并指定其 MIME 类型。
- -F "json_file=@structure.json;type=application/json": 上传名为 structure.json 的文件作为 json_file 字段，并指定其 MIME 类型。

执行此命令后，你将在命令行中看到返回的 JSON 响应。

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

## Configuration

Key environment variables:

- `OPENAI_API_KEY`: Your LLM API key (required)
- `OPENAI_API_BASE`: API base URL (default: DeepSeek API)
- `LLM_MODEL`: Model name (default: deepseek-chat)
- `MAX_CONCURRENT_CHAPTERS`: Concurrent processing limit (default: 3)

## Architecture

```
├── config/                 # 应用程序配置
│   └── settings.py         # 配置设置，从环境变量加载
├── examples/               # 示例文件
│   └── example_knowledge_structure.json # 示例知识结构 JSON
├── models/                 # Pydantic 模型和数据模式
│   └── schemas.py          # 定义 API 请求和响应的数据结构
├── services/               # 核心业务逻辑服务
│   ├── knowledge_extractor.py # 知识提取的编排服务
│   ├── langchain_service.py # LangChain LLM 交互服务
│   └── pdf_processor.py    # PDF 处理和章节提取服务
├── utils/                  # 实用工具函数
│   ├── file_validator.py   # 文件上传验证工具
│   └── json_processor.py   # JSON 处理工具
├── .env.example            # 环境变量示例文件
├── main.py                 # FastAPI 主应用入口
├── requirements.txt        # Python 依赖库列表
├── README.md               # 项目说明文档
├── src/                    # 前端 React 应用代码 (与后端逻辑无关，但作为项目一部分)
│   ├── App.tsx
│   ├── index.css
│   ├── main.tsx
│   └── vite-env.d.ts
├── index.html              # 前端 HTML 入口
├── package.json            # 前端 Node.js 项目配置
├── postcss.config.js       # 前端 PostCSS 配置
├── tailwind.config.js      # 前端 Tailwind CSS 配置
├── tsconfig.app.json       # 前端 TypeScript 配置
├── tsconfig.json           # 前端 TypeScript 配置
├── tsconfig.node.json      # 前端 TypeScript 配置
└── vite.config.ts          # 前端 Vite 配置
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

## 各模块功能和联系
1. main.py - FastAPI 主应用入口
- 功能: 这是整个 FastAPI 应用程序的入口点。它负责：
  - 初始化 FastAPI 应用实例。
  - 配置 CORS (跨域资源共享) 中间件，允许前端或其他客户端进行跨域请求。
  - 定义 API 路由 (/ 健康检查和 /process 核心处理接口)。
  - 实例化并协调各个服务 (PDFProcessor, LangChainService, KnowledgeExtractor, FileValidator, JSONProcessor)。
  - 处理文件上传 (pdf_file, json_file)，调用验证器进行初步检查。
  - 编排整个知识提取流程：文件验证 -> JSON 解析 -> PDF 章节提取 -> 知识点提取 -> 结果返回。
  - 实现全局异常处理，捕获未处理的错误并返回统一的错误响应。
  - 包含 uvicorn.run，用于在开发模式下启动服务。
- 联系: 它是所有其他后端模块的“指挥中心”。它调用 utils 中的验证器和处理器，并协调 services 中的核心业务逻辑。
  
2. config/settings.py - 应用程序配置
- 功能: 集中管理应用程序的所有配置设置，例如 API 标题、版本、LLM (大语言模型) 相关的配置 (API 密钥、模型名称、温度、最大 token 数)、文件大小限制、并发处理限制、日志级别等。
  - 它从 .env 文件（通过 dotenv 库加载）中读取环境变量，提供灵活的配置方式。
  - 包含一个 validate_settings 方法，用于在应用启动时检查必要的环境变量是否已设置（例如 OPENAI_API_KEY）。
- 联系: 几乎所有其他模块都需要访问这些配置，例如 langchain_service 需要 LLM 配置，file_validator 需要文件大小限制，knowledge_extractor 需要并发限制。通过一个集中的 settings 对象，避免了硬编码和重复配置。

3. models/schemas.py - Pydantic 模型和数据模式
- 功能: 使用 Pydantic 定义了 API 请求和响应的数据结构，确保数据的有效性和一致性。
  - ProcessResponse: 定义了 /process 接口成功响应的结构，包括 success 状态、message、提取的 data (知识点) 和 processed_at 时间戳。
  - ErrorResponse: 定义了错误响应的结构，包括 success 状态、message 和可选的 error 详情。
  - ChapterInfo, ProcessingConfig, KnowledgeStructure: 这些是内部或辅助模型，用于更清晰地定义数据类型和结构，尽管它们可能不直接作为 API 的输入/输出。
- 联系: main.py 使用这些模式来定义 API 接口的输入和输出，确保数据符合预期。services 模块在处理数据时也会遵循这些模式。
  
4. services/ 目录 - 核心业务逻辑
这个目录包含了应用程序的核心业务逻辑，每个文件负责一个特定的服务。

- services/pdf_processor.py - PDF 处理服务

  - 功能: 负责 PDF 文件的加载、文本内容的提取以及将 PDF 内容分割成逻辑章节。
    - 使用 langchain_community.document_loaders.PyPDFLoader 加载 PDF。
    - 使用 langchain_text_splitters.RecursiveCharacterTextSplitter 进行文本分割，以处理没有明确章节结构的 PDF。
    - 实现了基于正则表达式的章节识别逻辑 (_split_into_chapters)，尝试识别常见的章节标题模式。
    - 如果无法识别章节，则回退到固定大小的文本块分割 (_split_by_chunks)。
  - 联系: main.py 调用 pdf_processor.extract_chapters 来获取 PDF 的章节内容，这些章节内容随后会被传递给 knowledge_extractor 进行处理。
    
- services/langchain_service.py - LangChain LLM 交互服务

  - 功能: 封装了与大语言模型 (LLM) 的所有交互逻辑。
    - 初始化 ChatOpenAI (兼容 OpenAI API 的模型，默认配置为 DeepSeek)。
    - 定义了两个核心的 LangChain ChatPromptTemplate：
      - knowledge_prompt: 用于从单个章节内容中提取知识点，并按照给定的 JSON 结构填充。系统提示词强调了严格遵循 JSON 结构、只提取现有内容、保持有效 JSON 格式等关键指令。
      - merge_prompt: 用于将从不同章节提取的知识点合并成一个最终的、综合的 JSON 结构，处理去重和逻辑组织。
    - 使用 JsonOutputParser 确保 LLM 的输出是有效的 JSON 格式。
    - 提供了 extract_knowledge_from_chapter 方法，用于调用 LLM 处理单个章节。
    - 提供了 merge_knowledge_points 方法，用于调用 LLM 合并所有章节的提取结果。
  - 联系: knowledge_extractor 是 langchain_service 的主要消费者，它调用 extract_knowledge_from_chapter 逐章提取，并调用 merge_knowledge_points 进行最终整合。
    
- services/knowledge_extractor.py - 知识提取编排服务

  - 功能: 作为知识提取过程的“总指挥”，它编排了整个流程。
    - 接收 PDF 章节列表和目标知识结构 JSON。
    - 使用 asyncio.Semaphore 实现并发控制，限制同时向 LLM 发送的请求数量 (max_concurrent_requests)，以避免 API 速率限制或资源耗尽。
    - 异步地并行处理每个章节，调用 langchain_service.extract_knowledge_from_chapter。
    - 收集所有章节的提取结果，并过滤掉处理失败的章节。
    - 最后，调用 langchain_service.merge_knowledge_points 将所有章节的提取结果合并成一个最终的、完整的知识结构。
  - 联系: main.py 调用 knowledge_extractor.extract_knowledge_points 来启动整个知识提取流程。knowledge_extractor 内部则依赖于 langchain_service 来执行实际的 LLM 调用。

5. utils/ 目录 - 实用工具函数
- utils/file_validator.py - 文件上传验证工具

  - 功能: 提供了对上传文件进行安全和格式验证的功能。
    - validate_pdf: 检查 PDF 文件的扩展名、大小、以及文件内容是否以 %PDF 开头（基本魔术字节检查）。
    - validate_json: 检查 JSON 文件的扩展名、大小、以及内容是否是有效的 JSON 格式且为字典类型。
    - 在验证失败时抛出 HTTPException，FastAPI 会将其转换为 HTTP 错误响应。
  - 联系: main.py 在接收到文件上传后，会立即调用 file_validator 中的方法进行初步验证，确保只有合法的文件才能进入后续处理流程。

- utils/json_processor.py - JSON 处理工具

  - 功能: 提供了 JSON 文件的解析、结构验证和序列化处理功能。
    - parse_json_file: 异步读取并解析 JSON 文件内容。
    - validate_json_structure: 对解析后的 JSON 数据进行基本结构验证，检查是否包含常见的知识结构指示器（如 topics, concepts 等）。
    - ensure_json_serializable: 确保数据可以被 JSON 序列化，如果遇到不可序列化的对象，会尝试将其转换为字符串。
  - 联系: main.py 调用 json_processor.parse_json_file 来解析上传的知识结构 JSON 文件。langchain_service 在处理 LLM 输出时也可能用到 JSON 序列化相关的辅助功能。

6. requirements.txt - Python 依赖库列表
  - 功能: 列出了项目所需的所有 Python 库及其版本。这是 pip 包管理器用来安装项目依赖的清单。
  - 联系: 确保项目在任何环境中都能正确安装所有必要的库，是项目可运行的基础。

7. .env.example - 环境变量示例文件
  - 功能: 提供了一个 .env 文件的模板，用户可以复制此文件并填写自己的 API 密钥和其他配置值。
  - 联系: 与 config/settings.py 紧密相关，settings.py 会从实际的 .env 文件中加载这些变量。

8. README.md - 项目说明文档
  - 功能: 提供了项目的概述、功能、技术栈、安装指南、API 使用说明、配置选项、架构图、开发指南、错误处理和日志记录等信息。
  - 联系: 用户理解和使用项目的首要文档。

9. examples/example_knowledge_structure.json - 示例知识结构 JSON
  - 功能: 提供了一个预定义的 JSON 结构示例，用于指导用户如何构建自己的知识结构模板。
  - 联系: 用户在调用 /process 接口时，需要提供一个类似这样的 JSON 文件作为 json_file 参数。

## 模块间的工作流（以 /process 接口为例）
1. 请求接收: 用户向 /process 端点发送一个 POST 请求，包含 pdf_file 和 json_file。
2. 文件验证: main.py 首先调用 utils.file_validator 对上传的 PDF 和 JSON 文件进行类型、大小和基本格式的验证。如果验证失败，立即返回 HTTPException。
3. JSON 解析: main.py 调用 utils.json_processor.parse_json_file 解析上传的知识结构 JSON 文件，获取目标结构。
4. PDF 章节提取: main.py 调用 services.pdf_processor.extract_chapters 从 PDF 文件中提取文本内容，并将其分割成多个章节（或文本块）。
5. 知识提取编排: main.py 将提取的章节列表和目标 JSON 结构传递给 services.knowledge_extractor.extract_knowledge_points。
  - knowledge_extractor 使用 asyncio.Semaphore 控制并发，对每个章节：
    - 调用 services.langchain_service.extract_knowledge_from_chapter。
    - langchain_service 根据 knowledge_prompt 和章节内容、目标 JSON 结构，调用 LLM (DeepSeek) 进行知识点提取。
    - LLM 返回填充好的 JSON 片段。
6. 结果合并: knowledge_extractor 收集所有章节的提取结果，然后调用 services.langchain_service.merge_knowledge_points。
  - langchain_service 根据 merge_prompt 和所有章节的提取结果、原始目标 JSON 结构，再次调用 LLM 进行最终的合并和整合。
  - LLM 返回最终的、完整的知识结构 JSON。
7. 响应返回: main.py 接收到最终的知识结构 JSON 后，将其封装在 ProcessResponse 模型中，并作为 JSON 响应返回给客户端。

## 总结
main.py 负责路由和协调，config 负责配置，models 负责数据定义，utils 提供通用工具，而 services 目录是核心业务逻辑的所在地，每个服务都专注于一个特定任务（PDF 处理、LLM 交互、知识提取编排）。
