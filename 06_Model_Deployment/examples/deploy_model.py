"""Model Deployment Example."""

from google.cloud import aiplatform

# Initialize Vertex AI
aiplatform.init(
    project='YOUR_PROJECT_ID',
    location='us-central1'
)

# Get the model
model = aiplatform.Model('projects/PROJECT_ID/locations/LOCATION/models/MODEL_ID')

# Deploy model to endpoint
endpoint = model.deploy(
    deployed_model_display_name='my-deployed-model',
    machine_type='n1-standard-4',
    min_replica_count=1,
    max_replica_count=3,
    traffic_percentage=100
)

print(f"Model deployed to endpoint: {endpoint.resource_name}")

# Make a prediction
instances = [[1.0, 2.0, 3.0]]
prediction = endpoint.predict(instances=instances)
print(f"Prediction: {prediction}")

# Undeploy model
endpoint.undeploy_all()
print("Model undeployed from endpoint")
