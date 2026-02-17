"""Model Registry Example."""

from google.cloud import aiplatform

# Initialize Vertex AI
aiplatform.init(
    project='YOUR_PROJECT_ID',
    location='us-central1'
)

# Upload a model to the registry
model = aiplatform.Model.upload(
    display_name='my-model',
    artifact_uri='gs://your-bucket/model',
    serving_container_image_uri='gcr.io/cloud-aiplatform/prediction/tf2-cpu.2-8:latest'
)

print(f"Model uploaded: {model.resource_name}")

# List all models
models = aiplatform.Model.list()
for model in models:
    print(f"Model: {model.display_name}, Version: {model.version_id}")

# Get a specific model
model = aiplatform.Model('projects/PROJECT_ID/locations/LOCATION/models/MODEL_ID')
print(f"Retrieved model: {model.display_name}")
