##AI Agent for Document Ingestion and Query Retrieval

A powerful, standalone backend microservice built with FastAPI and LangChain that allows users to upload documents (PDFs and CSVs) and ask questions about their content using natural language. The system leverages state-of-the-art AI embedding models to provide fast and accurate semantic search capabilities.

## ✨ Features

- *Document Ingestion*: Upload PDF and CSV files via a RESTful API endpoint.
- *Intelligent Text Processing*: Automatically extracts text, splits it into semantically meaningful chunks, and generates vector embeddings.
- *State-of-the-Art Embeddings*: Uses Cohere's powerful embedding models to convert text into high-dimensional vectors.
- *Vector Storage*: Stores and indexes vectors efficiently using FAISS for fast retrieval.
- *Natural Language Queries*: A dedicated API endpoint to ask questions about an ingested document and receive relevant answers.
- *Parallel Processing*: Utilizes LangChain's RunnableParallel to enhance query responses by generating related questions alongside the primary answer.
- *Configurable \& Scalable*: Key parameters (API keys, file paths, etc.) are managed via a .env file, and the application is designed to be scalable.
- *Structured Logging*: Centralized logging configured via a logging.yaml file for easy monitoring and debugging.


## 🛠️ Tech Stack

- *Backend Framework*: FastAPI
- *AI/ML Orchestration*: LangChain
- *Embedding Models*: Cohere (embed-english-v3.0 or similar)
- *Vector Database*: FAISS (Facebook AI Similarity Search)
- *Configuration*: Pydantic
- *Language*: Python 3.12+
- *Dependency Management*: uv


## 🚀 Getting Started

Follow these steps to set up and run the project locally.

### 1. Prerequisites

- Python 3.12 or higher
- uv (or pip) for package installation. uv is recommended for its speed.
- A Cohere API key for generating embeddings.


### 2. Clone the Repository

bash
git clone <your-repository-url>
cd AI_AGENT



### 3. Set Up the Environment

First, create a virtual environment.

*Using uv:*

bash
# This will also create the virtual environment (.venv)
uv init


*Using standard venv:*

bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`



### 4. Configure Environment Variables

Create a .env file in the root of the project directory by copying the example file:

bash
cp .env.example .env


Now, open the .env file and add your credentials and desired configurations:

env
# .env file

# Your Cohere API Key
COHERE_API_KEY="your_cohere_api_key_here"

# Path to store the FAISS vector databases
VECTOR_DB_PATH="vector_store"

# Directory for temporary file uploads
UPLOAD_TEMP_DIR="tmp_uploads"

# API prefix for all endpoints
API_PREFIX="/api"



### 5. Install Dependencies

Install all the required Python packages.

*Using uv:*

bash
uv pip install -e .


*Using pip:*

bash
pip install -e .



### 6. Run the Application

Start the FastAPI server using uvicorn.

bash
uvicorn app.main:app --reload


The server will start, and the application will be available at http://127.0.0.1:8000.

## 📖 API Usage

Once the server is running, you can access the interactive API documentation (Swagger UI) at:

*[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)*

From there, you can test the API endpoints directly.

### Endpoints

#### 1. Ingest a Document

- *URL*: /api/ingest-document
- *Method*: POST
- *Body*: multipart/form-data
    - document_name (string): A unique name to identify the document (e.g., "financial_report_q3").
    - file (file): The PDF or CSV file to be ingested.

*Example using curl:*

bash
curl -X POST "http://127.0.0.1:8000/api/ingest-document" \
     -H "Content-Type: multipart/form-data" \
     -F "document_name=my_first_doc" \
     -F "file=@/path/to/your/document.pdf"



#### 2. Query a Document

- *URL*: /api/query
- *Method*: POST
- *Body*: JSON
    - document_name (string): The name of the ingested document you want to query.
    - query (string): Your question about the document's content.

*Example using curl:*

bash
curl -X POST "http://127.0.0.1:8000/api/query" \
     -H "Content-Type: application/json" \
     -d '{
           "document_name": "my_first_doc",
           "query": "What were the total revenues last quarter?"
         }'



## 📁 Project Structure


AI_AGENT/
├── .env                  # Environment variables
├── .venv/                # Virtual environment
├── app/                  # Main application package
│   ├── __init__.py
│   ├── core/             # Configuration and core settings
│   ├── dependencies/     # Reusable logic (text processing, vector store)
│   ├── endpoints/        # API route definitions
│   ├── model/            # Pydantic schemas and AI model wrappers
│   └── main.py           # FastAPI application entry point
├── logging.yaml          # Logging configuration
├── pyproject.toml        # Project metadata and dependencies
└── README.md             # This file
