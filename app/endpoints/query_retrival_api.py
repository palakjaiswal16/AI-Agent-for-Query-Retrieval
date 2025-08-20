from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.dependencies.vector_store import get_vector_store
from app.model.llm import get_llm

# Define the request and response models
class QueryRequest(BaseModel):
    document_name: str
    query: str

class QueryResponse(BaseModel):
    answer: str
    related_questions: list[str]

# Create the API router
router = APIRouter()

@router.post("/query", response_model=QueryResponse)
async def query_document(request: QueryRequest = Body(...)):
    """
    Accepts a query and a document name, retrieves relevant context,
    and generates an answer and related questions in parallel.
    """
    try:
        # 1. Load the vector store and create a retriever
        vector_store = get_vector_store(request.document_name)
        retriever = vector_store.as_retriever()

        # Get the language model
        llm = get_llm()

        # 2. Define the chain for answering the question
        answer_prompt = ChatPromptTemplate.from_template(
            "Answer the question based only on the following context:\n\n{context}\n\nQuestion: {question}"
        )
        
        retrieval_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | answer_prompt
            | llm
            | StrOutputParser()
        )

        # 3. Define the chain for generating related questions
        questions_prompt = ChatPromptTemplate.from_template(
            "Based on the following question, generate 3 related questions that a user might also ask. "
            "Return them as a comma-separated list:\n\nQuestion: {question}"
        )

        question_generation_chain = (
            questions_prompt
            | llm
            | StrOutputParser()
        )

        # 4. Create the RunnableParallel to run both chains at once
        parallel_chain = RunnableParallel(
            answer=retrieval_chain,
            questions=question_generation_chain
        )

        # 5. Invoke the parallel chain with the user's query
        result = await parallel_chain.ainvoke(request.query)

        # Process the results
        final_answer = result.get("answer", "Could not generate an answer.")
        related_questions_str = result.get("questions", "")
        related_questions = [q.strip() for q in related_questions_str.split(',') if q.strip()]

        return QueryResponse(answer=final_answer, related_questions=related_questions)

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Document not found.")
    except Exception as e:
        # In a real app, you'd log the error `e`
        raise HTTPException(status_code=500, detail="Failed to process the query.")

# Register the router in the main application
# This should be done in your main FastAPI app file, e.g., app/main.py