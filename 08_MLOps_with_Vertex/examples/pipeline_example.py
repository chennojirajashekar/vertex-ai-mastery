"""MLOps Pipeline Example."""

from google.cloud import aiplatform
from kfp.v2 import dsl
from kfp.v2.dsl import component

# Initialize Vertex AI
aiplatform.init(
    project='YOUR_PROJECT_ID',
    location='us-central1'
)

@component(
    packages_to_install=['google-cloud-aiplatform']
)
def train_model(dataset_path: str) -> str:
    """Train a model component."""
    # Training logic here
    return 'gs://bucket/model'

@dsl.pipeline(
    name='mlops-pipeline',
    description='End-to-end MLOps pipeline'
)
def mlops_pipeline(dataset_path: str):
    """Define the pipeline."""
    model_path = train_model(dataset_path=dataset_path)
    return model_path

# Compile and run pipeline
from kfp.v2 import compiler
compiler.Compiler().compile(
    pipeline_func=mlops_pipeline,
    package_path='mlops_pipeline.json'
)

job = aiplatform.PipelineJob(
    display_name='mlops-pipeline-run',
    template_path='mlops_pipeline.json',
    parameter_values={'dataset_path': 'gs://bucket/data'}
)

job.run()
print(f"Pipeline job: {job.resource_name}")
