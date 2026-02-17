"""Setup and Initialize Google Cloud Vertex AI.

This script demonstrates how to set up authentication, initialize
the Vertex AI SDK, and configure your GCP project for Vertex AI.
"""

import os
from google.cloud import aiplatform
from google.auth import default
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VertexAISetup:
    """Class to handle Vertex AI initialization and setup."""
    
    def __init__(self, project_id: str, location: str = "us-central1"):
        """
        Initialize Vertex AI setup.
        
        Args:
            project_id: GCP Project ID
            location: GCP region for Vertex AI resources
        """
        self.project_id = project_id
        self.location = location
        self.credentials = None
        
    def authenticate(self):
        """Authenticate using Application Default Credentials."""
        try:
            credentials, project = default()
            self.credentials = credentials
            logger.info(f"Authenticated successfully for project: {project}")
            return True
        except Exception as e:
            logger.error(f"Authentication failed: {str(e)}")
            return False
    
    def initialize_vertex_ai(self):
        """Initialize Vertex AI SDK."""
        try:
            aiplatform.init(
                project=self.project_id,
                location=self.location,
                credentials=self.credentials
            )
            logger.info(f"Vertex AI initialized for project {self.project_id} in {self.location}")
            return True
        except Exception as e:
            logger.error(f"Initialization failed: {str(e)}")
            return False
    
    def verify_setup(self):
        """Verify Vertex AI setup by listing datasets."""
        try:
            datasets = aiplatform.TabularDataset.list()
            logger.info(f"Found {len(datasets)} datasets in the project")
            return True
        except Exception as e:
            logger.error(f"Verification failed: {str(e)}")
            return False


def main():
    """Main function to demonstrate Vertex AI setup."""
    # Set your project ID
    PROJECT_ID = os.getenv("GCP_PROJECT_ID", "your-project-id")
    LOCATION = "us-central1"
    
    # Initialize setup
    vertex_setup = VertexAISetup(PROJECT_ID, LOCATION)
    
    # Authenticate
    if not vertex_setup.authenticate():
        logger.error("Failed to authenticate. Exiting.")
        return
    
    # Initialize Vertex AI
    if not vertex_setup.initialize_vertex_ai():
        logger.error("Failed to initialize Vertex AI. Exiting.")
        return
    
    # Verify setup
    if vertex_setup.verify_setup():
        logger.info("Vertex AI setup completed successfully!")
    else:
        logger.warning("Setup verification encountered issues.")


if __name__ == "__main__":
    main()
