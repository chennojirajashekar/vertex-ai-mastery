"""Cost Optimization Example."""

from google.cloud import aiplatform
import google.cloud.monitoring_v3 as monitoring

# Initialize Vertex AI
aiplatform.init(
    project='YOUR_PROJECT_ID',
    location='us-central1'
)

# Deploy with cost optimization
model = aiplatform.Model('projects/PROJECT_ID/locations/LOCATION/models/MODEL_ID')

# Use Spot instances for training
job = aiplatform.CustomTrainingJob(
    display_name='cost-optimized-training',
    container_uri='gcr.io/my-project/training:latest',
    model_serving_container_image_uri='gcr.io/my-project/serving:latest'
)

# Use preemptible instances to save costs
job.run(
    replica_count=1,
    machine_type='n1-standard-4',
    accelerator_type='NVIDIA_TESLA_T4',
    accelerator_count=1,
    # Use spot/preemptible instances
    base_output_dir='gs://bucket/output',
    service_account='sa@project.iam.gserviceaccount.com'
)

# Autoscaling configuration for deployment
endpoint = model.deploy(
    deployed_model_display_name='cost-optimized-model',
    machine_type='n1-standard-2',
    min_replica_count=1,  # Minimum replicas
    max_replica_count=5,  # Scale up when needed
    traffic_percentage=100,
    # Enable autoscaling
    autoscaling_target_cpu_utilization=60
)

print(f"Model deployed with autoscaling: {endpoint.resource_name}")

# Monitor costs using Cloud Monitoring
client = monitoring.MetricServiceClient()
project_name = f"projects/{aiplatform.initializer.global_config.project}"

query = f'''
fetch consumed_api
| metric 'serviceruntime.googleapis.com/api/request_count'
| filter resource.service == 'aiplatform.googleapis.com'
'''

print("Query for cost monitoring configured")
