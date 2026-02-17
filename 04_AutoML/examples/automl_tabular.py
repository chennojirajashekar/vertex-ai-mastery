"""AutoML Tabular Training Example."""
from google.cloud import aiplatform
import os

aiplatform.init(project=os.getenv('GCP_PROJECT_ID'), location='us-central1')

dataset = aiplatform.TabularDataset.create(
    display_name='my-dataset',
    gcs_source='gs://bucket/data.csv'
)

job = aiplatform.AutoMLTabularTrainingJob(
    display_name='automl-training',
    optimization_prediction_type='classification'
)

model = job.run(
    dataset=dataset,
    target_column='label',
    budget_milli_node_hours=1000
)
