from pydantic import BaseModel

class IngestResponse(BaseModel):
    message: str
    document_name: str

class QueryRequest(BaseModel):
    query: str
    document_name: str

class QueryResponse(BaseModel):
    answer: str
    