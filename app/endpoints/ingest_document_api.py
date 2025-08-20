import os
import shutil
import logging
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.dependencies.text_processing import load_and_chunk
from app.dependencies.vector_store import save_vector_store
from app.model.schemas import IngestResponse
from app.core.config import settings # Import the settings object

# Initialize the router
router = APIRouter()

# Get the logger instance configured in your logging.yaml
logger = logging.getLogger("app")

@router.post("/ingest-document", response_model=IngestResponse)
async def ingest_document(
    file: UploadFile = File(...), 
    document_name: str = Form(...)
):
    """
    Handles the document ingestion process:
    1. Validates the uploaded file.
    2. Saves it to a temporary directory defined in the .env file.
    3. Extracts and chunks the text content.
    4. Generates embeddings and saves them to a vector store.
    5. Cleans up the temporary file.
    """
    temp_file_path = ""
    try:
        # Validate file type
        if file.content_type not in ["application/pdf", "text/csv", "application/vnd.ms-excel"]:
            logger.warning(
                f"Invalid file type uploaded: {file.filename} ({file.content_type}) "
                f"for document: {document_name}"
            )
            raise HTTPException(
                status_code=400, 
                detail="Invalid file type. Only PDF and CSV files are allowed."
            )

        # Use the configurable path from settings for the temporary file
        temp_file_path = os.path.join(settings.UPLOAD_TEMP_DIR, f"{document_name}_{file.filename}")

        # Save the uploaded file to the temporary location
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info(f"Temporarily saved uploaded file to: {temp_file_path}")

        # Process the file: load, chunk, and save to vector store
        file_extension = file.filename.split(".")[-1].lower()
        chunks = load_and_chunk(temp_file_path, file_extension)
        save_vector_store(document_name, chunks)

        logger.info(f"Document '{document_name}' ingested successfully.")
        return IngestResponse(
            message="Document ingested successfully", 
            document_name=document_name
        )

    except Exception as e:
        logger.error(
            f"Failed to ingest document '{document_name}': {str(e)}", 
            exc_info=True  # This includes the full stack trace in the log
        )
        # Raise a generic 500 error to avoid exposing internal details to the user
        raise HTTPException(status_code=500, detail="An unexpected error occurred during document ingestion.")
    
    finally:
        # Clean up the temporary file, ensuring it's always removed
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
                logger.info(f"Cleaned up temporary file: {temp_file_path}")
            except Exception as e:
                logger.error(f"Failed to clean up temporary file {temp_file_path}: {e}")

