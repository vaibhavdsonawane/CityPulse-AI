import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def create_project_structure() -> None:
    """Generates the production-grade folder architecture for CITYPULSE AI."""
    
    directories = [
        "app/routes",
        "app/models",
        "app/controllers",
        "app/templates",
        "app/static/css",
        "app/static/js",
        "app/static/uploads/images",
        "dataset/raw",
        "dataset/processed",
        "dataset/external",
        "dataset/synthetic",
        "ml_pipeline",
        "cv_pipeline",
        "saved_models/ml_models",
        "saved_models/cv_models",
        "scripts",
        "tests/unit",
        "tests/integration",
        "docs"
    ]
    
    files = [
        "app/__init__.py",
        "app/models.py",
        "config.py",
        "requirements.txt",
        "Dockerfile",
        ".env",
        "README.md",
        "dataset/README.md"
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        # Create __init__.py in Python packages
        if "app" in directory or "pipeline" in directory:
            with open(os.path.join(directory, "__init__.py"), 'a') as f:
                pass
        logging.info(f"Created directory: {directory}")

    for file in files:
        if not os.path.exists(file):
            with open(file, 'w') as f:
                pass
            logging.info(f"Created file: {file}")

if __name__ == "__main__":
    create_project_structure()
    logging.info("CITYPULSE AI folder structure initialized successfully.")