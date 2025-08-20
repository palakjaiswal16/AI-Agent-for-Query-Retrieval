import os
from langchain_community.vectorstores import FAISS
from app.core.config import settings
from app.model.llm import EmbeddingGenerator

def get_vector_store(doc_name: str):
    path = os.path.join(settings.VECTOR_DB_PATH, f"{doc_name}.faiss")
    if not os.path.exists(path):
        raise FileNotFoundError("Document not found in vector store")

    # Get the actual embedding model from your wrapper class
    embedding_model = EmbeddingGenerator().model
    # Pass the model directly to FAISS
    # The 'allow_dangerous_deserialization' is required for loading local FAISS indexes
    return FAISS.load_local(path, embedding_model, allow_dangerous_deserialization=True)

def save_vector_store(doc_name: str, docs):
    # Get the actual embedding model from your wrapper class
    embedding_model = EmbeddingGenerator().model
    # Pass the model directly to FAISS
    vector_store = FAISS.from_documents(docs, embedding_model)
    os.makedirs(settings.VECTOR_DB_PATH, exist_ok=True)
    path = os.path.join(settings.VECTOR_DB_PATH, f"{doc_name}.faiss")
    vector_store.save_local(path)
    return vector_store
# app/dependencies/vector_store.py
# This module provides functions to interact with the vector store, including loading and saving documents.