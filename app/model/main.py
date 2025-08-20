from fastapi import FastAPI
from app.endpoints import ingest_document_api, query_retrival_api

def create_app():
    app = FastAPI(
        title="AI Agent: Document Ingestion and Query Retrieval",
        description="API for uploading documents and querying using Cohere embeddings and Langchain.",
        version="1.0"
    )

    app.include_router(ingest_document_api.router, prefix="/api")
    app.include_router(query_retrival_api.router, prefix="/api")

    return app
# app/model/main.py
# This module initializes the FastAPI application and includes the API routers for document ingestion and query retrieval