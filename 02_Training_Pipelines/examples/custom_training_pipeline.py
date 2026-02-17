"""Custom Training Pipeline Example for Vertex AI."""

from google.cloud import aiplatform
import os

PROJECT_ID = os.getenv('GCP_PROJECT_ID')
LOCATION = 'us-central1'

aiplatform.init(project=PROJECT_ID, location=LOCATION)

# Create custom training job
job = aiplatform.CustomTrainingJob(
    display_name='custom-training-job',
    container_uri='gcr.io/cloud-aiplatform/training/tf-cpu.2-8:latest',
    model_serving_container_image_uri='gcr.io/cloud-aiplatform/prediction/tf2-cpu.2-8:latest'
)

job.run(
    dataset=None,
    model_display_name='my-model',
    machine_type='n1-standard-4'
)
