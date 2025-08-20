
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    # Your existing settings
    COHERE_API_KEY: str
    VECTOR_DB_PATH: str

    # Add the new setting for the upload directory
    UPLOAD_TEMP_DIR: str = "tmp_uploads"  # Default value if not found in .env

    # Configure Pydantic to load from the .env file
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

# Create a single, reusable instance of the settings
settings = Settings()

# --- Best Practice: Create the directory if it doesn't exist ---
# This ensures that the application doesn't fail if the folder is missing
os.makedirs(settings.UPLOAD_TEMP_DIR, exist_ok=True)

# This file contains the configuration settings for the application.    