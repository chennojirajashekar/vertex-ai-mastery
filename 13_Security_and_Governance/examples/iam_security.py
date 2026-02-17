"""Security and Governance Example."""

from google.cloud import aiplatform
from google.cloud import resourcemanager_v3
from google.iam.v1 import iam_policy_pb2

# Initialize Vertex AI
aiplatform.init(
    project='YOUR_PROJECT_ID',
    location='us-central1'
)

# Set up IAM policies for security
from google.cloud import aiplatform_v1

client = aiplatform_v1.ModelServiceClient()
resource = 'projects/PROJECT_ID/locations/LOCATION/models/MODEL_ID'

# Get current IAM policy
policy = client.get_iam_policy(
    request={"resource": resource}
)

print(f"Current policy: {policy}")

# Add a new binding
from google.iam.v1.policy_pb2 import Binding

binding = Binding(
    role='roles/aiplatform.user',
    members=['user:user@example.com']
)

policy.bindings.append(binding)

# Update IAM policy
updated_policy = client.set_iam_policy(
    request={
        "resource": resource,
        "policy": policy
    }
)

print(f"Updated policy: {updated_policy}")

# Enable encryption with CMEK (Customer-Managed Encryption Keys)
model = aiplatform.Model.upload(
    display_name='secure-model',
    artifact_uri='gs://bucket/model',
    serving_container_image_uri='gcr.io/project/serving:latest',
    # Use customer-managed encryption key
    encryption_spec_key_name='projects/PROJECT/locations/LOCATION/keyRings/RING/cryptoKeys/KEY'
)

print(f"Model with CMEK: {model.resource_name}")

# Enable VPC-SC (VPC Service Controls)
print("VPC-SC should be configured at organization level")
