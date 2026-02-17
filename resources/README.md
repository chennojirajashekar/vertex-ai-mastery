# 📚 Resources & Cheat Sheets

Your quick reference guide for Vertex AI mastery.

---

## 🚀 Quick Start Commands

### gcloud CLI Essentials

```bash
# Set project
gcloud config set project PROJECT_ID

# Create custom training job
gcloud ai custom-jobs create \
  --region=us-central1 \
  --display-name=my-training-job \
  --worker-pool-spec=machine-type=n1-standard-4,replica-count=1,container-image-uri=gcr.io/PROJECT_ID/trainer:latest

# Deploy model to endpoint
gcloud ai endpoints deploy-model ENDPOINT_ID \
  --region=us-central1 \
  --model=MODEL_ID \
  --display-name=deployment-name \
  --traffic-split=0=100

# Batch prediction
gcloud ai batch-prediction-jobs create \
  --region=us-central1 \
  --model=projects/PROJECT_ID/locations/us-central1/models/MODEL_ID \
  --input-path=gs://BUCKET/input.jsonl \
  --output-path=gs://BUCKET/output/
```

---

## 🐍 Python SDK Quick Reference

### Training Pipeline

```python
from google.cloud import aiplatform

aiplatform.init(project='PROJECT_ID', location='us-central1')

# Custom training job
job = aiplatform.CustomTrainingJob(
    display_name="my-training-job",
    container_uri="gcr.io/PROJECT_ID/trainer:latest",
    requirements=["pandas", "scikit-learn"]
)

model = job.run(
    dataset=my_dataset,
    model_display_name="my-model",
    training_fraction_split=0.8,
    validation_fraction_split=0.1,
    test_fraction_split=0.1,
    machine_type="n1-standard-4",
)
```

### Model Deployment

```python
# Create endpoint
endpoint = aiplatform.Endpoint.create(
    display_name="my-endpoint",
    encryption_spec_key_name=CMEK_KEY
)

# Deploy model
endpoint.deploy(
    model=model,
    deployed_model_display_name="v1",
    machine_type="n1-standard-4",
    min_replica_count=1,
    max_replica_count=3,
    traffic_percentage=100,
)

# Prediction
predictions = endpoint.predict(instances=[...])
```

### AutoML Training

```python
dataset = aiplatform.TabularDataset.create(
    display_name="my-dataset",
    gcs_source="gs://BUCKET/data.csv"
)

job = aiplatform.AutoMLTabularTrainingJob(
    display_name="automl-training",
    optimization_prediction_type="classification",
    optimization_objective="maximize-au-prc"
)

model = job.run(
    dataset=dataset,
    target_column="label",
    budget_milli_node_hours=1000,
)
```

---

## 🔑 IAM Roles Cheat Sheet

| Role | Purpose | Permissions |
|------|---------|-------------|
| `roles/aiplatform.user` | Full access to all Vertex AI resources | Create, update, delete all resources |
| `roles/aiplatform.viewer` | Read-only access | View all resources, no modifications |
| `roles/aiplatform.modelUser` | Deploy and predict | Deploy models, make predictions |
| `roles/aiplatform.customCodeServiceAgent` | Custom training execution | Run custom training jobs |

---

## 💰 Cost Optimization Checklist

- [ ] Use preemptible instances for training
- [ ] Enable autoscaling for endpoints (min=0)
- [ ] Delete idle endpoints and notebooks
- [ ] Use batch prediction for non-realtime needs
- [ ] Monitor with cost alerts
- [ ] Use appropriate machine types (don't over-provision GPUs)
- [ ] Enable request-response logging selectively
- [ ] Use caching for repeated predictions
- [ ] Compress large model artifacts
- [ ] Set budget limits on training jobs

---

## 🔒 Security Best Practices

1. **Always use service accounts** (never personal credentials)
2. **Enable VPC-SC** for sensitive workloads
3. **Encrypt data at rest** (CMEK for enterprise)
4. **Use private endpoints** for production
5. **Implement least privilege** IAM policies
6. **Enable audit logging** for compliance
7. **Scan containers** for vulnerabilities
8. **Rotate credentials** regularly
9. **Use Cloud Armor** for endpoint protection
10. **Implement model versioning** for rollbacks

---

## 🏗 Architecture Patterns

### Multi-Environment Setup

```
Dev Environment (Project: dev-ml)
  ├── Workbench instances
  ├── Experimental models
  └── Low-cost resources

Staging (Project: staging-ml)
  ├── Integration testing
  ├── Model validation
  └── Performance benchmarks

Production (Project: prod-ml)
  ├── High-availability endpoints
  ├── Monitoring & alerting
  ├── Autoscaling enabled
  └── Private networking
```

### CI/CD Pipeline Pattern

```
Code Push → Cloud Build Trigger
  ↓
Build Training Container
  ↓
Run Training Job (Vertex AI)
  ↓
Model Validation Tests
  ↓
Register Model (Model Registry)
  ↓
Deploy to Staging Endpoint
  ↓
Integration Tests
  ↓
Manual Approval
  ↓
Gradual Rollout to Production
  ↓
Monitor Metrics
```

---

## 📊 Performance Benchmarks

### Machine Type Recommendations

| Workload | Machine Type | GPU | Use Case |
|----------|--------------|-----|----------|
| Small tabular | n1-standard-4 | None | <10K rows |
| Medium tabular | n1-highmem-8 | None | 10K-1M rows |
| Large tabular | n1-highmem-32 | None | >1M rows |
| Computer Vision | n1-standard-8 | 1x T4 | Image classification |
| NLP (small models) | n1-highmem-16 | 1x T4 | BERT-base |
| LLM Fine-tuning | a2-highgpu-1g | 1x A100 | GPT-style models |
| Inference (light) | n1-standard-2 | None | <100 QPS |
| Inference (heavy) | n1-standard-8 | 1x T4 | >100 QPS |

---

## 🧪 Testing Checklist

### Pre-Deployment

- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Model performance meets SLA
- [ ] Latency < target threshold
- [ ] Cost within budget
- [ ] Security scan complete
- [ ] Monitoring configured
- [ ] Rollback plan tested
- [ ] Documentation updated
- [ ] Stakeholder approval

---

## 🔗 Useful Links

- [Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)
- [Python SDK Reference](https://cloud.google.com/python/docs/reference/aiplatform/latest)
- [Pricing Calculator](https://cloud.google.com/products/calculator)
- [Vertex AI Samples](https://github.com/GoogleCloudPlatform/vertex-ai-samples)
- [Community Forums](https://www.googlecloudcommunity.com/gc/AI-ML/bd-p/ai-ml)

---

## 🆘 Troubleshooting Guide

### Common Issues

**Training Job Fails**
- Check logs in Cloud Logging
- Verify IAM permissions
- Ensure container image exists
- Check resource quotas

**High Latency**
- Increase replica count
- Use GPU for inference
- Enable prediction caching
- Check network configuration

**Cost Overruns**
- Review Cloud Billing reports
- Delete unused resources
- Enable autoscaling
- Use preemptible instances

**Model Drift Detected**
- Retrain with recent data
- Review feature distributions
- Check for data quality issues
- Update preprocessing logic

---

**Ready to build?** Start with [00_Fundamentals](../00_Fundamentals/README.md)
