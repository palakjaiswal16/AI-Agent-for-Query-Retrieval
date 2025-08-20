import logging.config
import yaml
from app.model.main import create_app

# --- Add this new section to set up logging ---
def setup_logging():
    """Loads logging configuration from the logging.yaml file."""
    try:
        # This assumes 'logging.yaml' is in the same root directory as this main.py
        with open('logging.yaml', 'r') as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
        
        # Get the logger named 'app' from your yaml and log a success message
        logging.getLogger("app").info("Logging configured successfully from logging.yaml.")

    except FileNotFoundError:
        print("Warning: logging.yaml not found. Falling back to basic logging.")
        logging.basicConfig(level=logging.INFO)
    except Exception as e:
        print(f"Warning: Error loading logging configuration: {e}. Falling back to basic logging.")
        logging.basicConfig(level=logging.INFO)

# Call the setup function to configure logging right when the application starts
setup_logging()
# --- End of logging setup section ---


# The rest of your file remains the same
app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
