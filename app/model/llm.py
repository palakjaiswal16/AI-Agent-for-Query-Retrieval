from langchain_cohere import CohereEmbeddings, ChatCohere
from app.core.config import settings


class EmbeddingGenerator:
    def __init__(self):
        self.model = CohereEmbeddings(cohere_api_key=settings.COHERE_API_KEY, model="embed-v4.0")


    def embed(self, texts):
        return self.model.embed_documents(texts)


def get_llm():
    return ChatCohere(cohere_api_key=settings.COHERE_API_KEY)
# app/model/llm.py
# This module provides the LLM and embedding generator using Cohere API for text embeddings and responses