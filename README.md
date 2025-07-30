# Edu Chat RAG

A **Retrieval-Augmented Generation (RAG)** application designed for educational purposes, enabling users to upload PDF documents and ask questions that are answered using AI-powered context retrieval.

## 🚀 Features

- **PDF Document Processing**: Upload and process PDF files with automatic text extraction
- **Vector Database**: Semantic search using OpenAI embeddings for context retrieval
- **AI-Powered Q&A**: Get intelligent answers based on document content using GPT-4o-mini
- **RESTful API**: FastAPI-based endpoints for easy integration
- **User Session Management**: Multi-user support with isolated document contexts
- **Streaming Responses**: Real-time AI response streaming
- **Frontend Interface**: Web-based UI coming soon for easy document upload and Q&A

## 🏗️ Architecture

The application follows a modular architecture with the following components:

- **API Layer**: FastAPI routes for document upload and question handling
- **Document Processing**: PDF text extraction and chunking
- **Vector Database**: In-memory vector storage with cosine similarity search
- **Embedding Service**: OpenAI text-embedding-3-small for semantic encoding
- **Chat Model**: GPT-4o-mini for generating contextual responses
- **Prompt Management**: Structured prompt templates for consistent AI interactions

## 📋 Prerequisites

- Python 3.10-3.11
- OpenAI API key
- Docker (optional)

## 🛠️ Installation

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd edu-chat-rag/backend
   ```

2. **Install dependencies**
   ```bash
   pip install -e .
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your OpenAI API key and server configuration
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

### Docker

#### Using Docker Compose (Recommended)

1. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your OpenAI API key
   ```

2. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

3. **Run in background**
   ```bash
   docker-compose up -d --build
   ```

#### Using Docker directly

1. **Build the image**
   ```bash
   docker build -t edu-chat-rag .
   ```

2. **Run the container**
   ```bash
   docker run -p 8000:8000 \
     -e OPENAI_API_KEY=your_openai_api_key_here \
     -e HOST=0.0.0.0 \
     -e PORT=8000 \
     edu-chat-rag
   ```

3. **Run with environment file**
   ```bash
   docker run -p 8000:8000 --env-file .env edu-chat-rag
   ```

## 🔧 Configuration

Create a `.env` file with the following variables:

```env
OPENAI_API_KEY=your_openai_api_key_here
HOST=0.0.0.0
PORT=8000
```

## 📚 API Documentation

> **Note**: A web frontend is coming soon to provide a user-friendly interface for document upload and Q&A interactions.

### Health Check
```http
GET /ping
```

### Upload PDF Document
```http
POST /api/v1/upload/pdf
Content-Type: multipart/form-data
X-User-Id: your_user_id

file: [PDF file]
```

**Response:**
```json
{
  "message": "PDF processed and indexed",
  "chunks": 15
}
```

### Ask Question
```http
POST /api/v1/ask
Content-Type: application/x-www-form-urlencoded
X-User-Id: your_user_id

question: What is the main topic of the document?
```

**Response:**
```json
{
  "answer": "Based on the document content, the main topic is..."
}
```

## 🔍 How It Works

1. **Document Upload**: PDF files are processed and text is extracted
2. **Text Chunking**: Documents are split into manageable chunks (1000 chars with 200 char overlap)
3. **Vector Embedding**: Each chunk is converted to embeddings using OpenAI's text-embedding-3-small
4. **Vector Storage**: Embeddings are stored in an in-memory vector database
5. **Question Processing**: User questions are embedded and used to find relevant document chunks
6. **Context Retrieval**: Top-k most similar chunks are retrieved using cosine similarity
7. **AI Response**: Retrieved context is combined with the question and sent to GPT-4o-mini for answer generation

## 🏛️ Project Structure

```
backend/
├── api/
│   └── v1/
│       ├── __init__.py
│       └── upload_routes.py      # API endpoints
├── data/                         # Sample documents
│   ├── attention.pdf
│   └── protein.txt
├── models/
│   ├── __init__.py
│   └── schemas.py               # Pydantic models
├── services/
│   ├── __init__.py
│   ├── chatmodel.py             # OpenAI chat integration
│   ├── embedding.py             # Text embedding service
│   ├── pdf_utils.py             # PDF processing utilities
│   ├── prompts.py               # Prompt template management
│   ├── text_utils.py            # Text file processing
│   ├── utilits.py               # Utility functions
│   └── vectordatabase.py        # Vector database implementation
├── main.py                      # FastAPI application entry point
├── pyproject.toml               # Project dependencies
└── README.md
```

## 🧪 Usage Examples

> **Coming Soon**: A web-based frontend will provide an intuitive interface for uploading documents and asking questions without needing to use the API directly.

### Python Client Example

```python
import requests

# Upload a PDF document
with open('document.pdf', 'rb') as f:
    files = {'file': f}
    headers = {'X-User-Id': 'user123'}
    response = requests.post('http://localhost:8000/api/v1/upload/pdf', 
                           files=files, headers=headers)
    print(response.json())

# Ask a question
data = {'question': 'What are the key findings in this document?'}
headers = {'X-User-Id': 'user123'}
response = requests.post('http://localhost:8000/api/v1/ask', 
                        data=data, headers=headers)
print(response.json()['answer'])
```

### cURL Examples

```bash
# Upload PDF
curl -X POST "http://localhost:8000/api/v1/upload/pdf" \
  -H "X-User-Id: user123" \
  -F "file=@document.pdf"

# Ask question
curl -X POST "http://localhost:8000/api/v1/ask" \
  -H "X-User-Id: user123" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "question=What is the main topic of this document?"
```

## 🔒 Security Considerations

- **API Key Management**: Store OpenAI API keys securely in environment variables
- **User Isolation**: Each user's documents are isolated using user IDs
- **Input Validation**: All inputs are validated before processing
- **Error Handling**: Comprehensive error handling with appropriate HTTP status codes

## 🚧 Limitations

- **In-Memory Storage**: Vector database is stored in memory (not persistent)
- **Single Document**: Currently supports one document per user session
- **PDF Only**: Currently supports PDF files only
- **No Authentication**: Basic user ID-based isolation (not production-ready)

## 🔮 Future Enhancements

- [ ] **Web Frontend**: User-friendly web interface for document upload and Q&A
- [ ] Persistent vector database (Redis/PostgreSQL)
- [ ] Multiple document support per user
- [ ] Text file support (.txt, .docx)
- [ ] User authentication and authorization
- [ ] Document versioning and management
- [ ] Advanced chunking strategies
- [ ] Response caching
- [ ] Rate limiting
- [ ] Docker containerization
- [ ] Kubernetes deployment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Zubair Farahi**
- Email: farahi.zubair121@gmail.com
- GitHub: [@zubairfarahi](https://github.com/zubairfarahi)

## 🙏 Acknowledgments

- OpenAI for providing the embedding and chat models
- FastAPI for the excellent web framework
- The open-source community for various utility libraries

---

**Note**: This is an educational project. For production use, consider implementing proper authentication, persistent storage, and additional security measures.
