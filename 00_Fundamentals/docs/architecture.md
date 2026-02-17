# Vertex AI Architecture Overview

## Table of Contents
1. [Core Architecture](#core-architecture)
2. [Service Components](#service-components)
3. [ML Lifecycle on Vertex AI](#ml-lifecycle)
4. [Regional vs Global Services](#regional-vs-global)
5. [Integration Points](#integration-points)

## Core Architecture

### High-Level Architecture

Vertex AI is Google Cloud's unified ML platform that integrates multiple services:

```
┌─────────────────────────────────────────────────────────────────┐
│                      Vertex AI Platform                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Workbench  │  │   Pipelines  │  │  Feature     │         │
│  │              │  │              │  │  Store       │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Training   │  │    AutoML    │  │   Model      │         │
│  │              │  │              │  │   Registry   │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Prediction  │  │  Explainable │  │  Model       │         │
│  │  Endpoints   │  │     AI       │  │  Monitoring  │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│   GCS Storage   │  │  BigQuery Data  │  │  Cloud Build    │
│                 │  │                 │  │  /Artifact Reg  │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

### Architecture Layers

#### 1. **Data Layer**
- **Cloud Storage (GCS)**: Primary storage for training data, models, artifacts
- **BigQuery**: Structured data, feature engineering, batch predictions
- **Dataflow**: Stream and batch data processing
- **Data Labeling**: Annotation services for supervised learning

#### 2. **Training Layer**
- **Vertex AI Training**: Managed training with custom or pre-built containers
- **AutoML**: Automated model development
- **Hyperparameter Tuning**: Automated optimization
- **Distributed Training**: Multi-GPU/TPU training

#### 3. **Model Management Layer**
- **Model Registry**: Version control, metadata tracking
- **Model Garden**: Pre-trained models
- **Artifact Registry**: Container image storage

#### 4. **Serving Layer**
- **Prediction Endpoints**: Real-time inference
- **Batch Prediction**: Large-scale offline predictions
- **Private Endpoints**: VPC-secured serving

#### 5. **MLOps Layer**
- **Vertex AI Pipelines**: Workflow orchestration (Kubeflow)
- **Model Monitoring**: Drift detection, performance tracking
- **Explainable AI**: Model interpretability
- **Feature Store**: Feature management and serving

## Service Components

### 1. Vertex AI Workbench
**Purpose**: Managed Jupyter notebook environment

**Architecture**:
```
User → Workbench Instance → Compute Engine VM → GCS/BigQuery
```

**Key Features**:
- Pre-installed ML frameworks (TensorFlow, PyTorch, scikit-learn)
- Integration with Git, Cloud Source Repositories
- Scalable compute resources
- Built-in terminal access

### 2. Vertex AI Training
**Purpose**: Managed model training at scale

**Training Flow**:
```
1. Package Training Code → Docker Container
2. Upload to Artifact Registry
3. Submit Training Job → Vertex AI Training Service
4. Allocate Resources (CPU/GPU/TPU)
5. Execute Training
6. Save Model → GCS
7. Register Model → Model Registry
```

**Container Types**:
- **Pre-built containers**: TensorFlow, PyTorch, XGBoost, scikit-learn
- **Custom containers**: User-defined Docker images

### 3. AutoML
**Architecture**:
```
Raw Data → AutoML Pipeline → Neural Architecture Search → 
Hyperparameter Optimization → Model Selection → Deployed Model
```

**Supported Data Types**:
- Tabular (Classification, Regression)
- Image (Classification, Object Detection, Segmentation)
- Video (Classification, Object Tracking)
- Text (Classification, Entity Extraction, Sentiment Analysis)

### 4. Vertex AI Pipelines
**Based on**: Kubeflow Pipelines (KFP)

**Pipeline Architecture**:
```
Pipeline Definition (Python/YAML) → 
Compile → JSON/YAML Spec → 
Submit to Vertex AI → 
Kubeflow Backend → 
Execute Components → 
Store Artifacts
```

**Components**:
- **Pre-built components**: Google Cloud services
- **Custom components**: User-defined Python functions
- **Container components**: Docker-based components

### 5. Prediction Endpoints
**Online Prediction Architecture**:
```
Client Request → 
Load Balancer → 
Vertex AI Prediction Service → 
Model Container → 
Response
```

**Features**:
- Auto-scaling based on traffic
- Traffic splitting (A/B testing, canary deployments)
- Private endpoints (VPC-SC)
- Multi-model serving

## ML Lifecycle on Vertex AI

### End-to-End ML Workflow

```
1. DATA PREPARATION
   ├─ Ingest data (GCS, BigQuery)
   ├─ Explore in Workbench
   ├─ Feature engineering
   └─ Store features (Feature Store)

2. MODEL DEVELOPMENT
   ├─ Experiment in Workbench
   ├─ Train with AutoML OR Custom Training
   ├─ Hyperparameter tuning
   └─ Model evaluation

3. MODEL MANAGEMENT
   ├─ Register model (Model Registry)
   ├─ Version tracking
   └─ Model lineage

4. MODEL DEPLOYMENT
   ├─ Deploy to endpoint
   ├─ Configure serving resources
   └─ Set up monitoring

5. MONITORING & MAINTENANCE
   ├─ Monitor predictions
   ├─ Detect drift
   ├─ Retrain if needed
   └─ Update deployment
```

## Regional vs Global Services

### Regional Services
**Must specify region during creation**:
- Training Jobs
- Endpoints
- Batch Prediction Jobs
- Custom Jobs
- Hyperparameter Tuning Jobs

**Common Regions**:
- `us-central1`: Primary US region
- `europe-west4`: Primary EU region
- `asia-northeast1`: Primary Asia region

### Global Services
**No region specification needed**:
- Model Registry (metadata)
- Dataset metadata
- Feature Store schemas

### Multi-Regional Considerations
```
Scenario: Training in us-central1, Serving in europe-west4

1. Train model in us-central1
2. Save to GCS (multi-regional bucket)
3. Import model in europe-west4
4. Deploy endpoint in europe-west4
```

## Integration Points

### 1. Identity and Access Management (IAM)
```
Principal (User/Service Account) →
   IAM Policy →
      Vertex AI Resources

Key Roles:
- aiplatform.admin
- aiplatform.user
- aiplatform.viewer
- aiplatform.customCodeServiceAgent
```

### 2. Networking
```
Vertex AI Service →
   VPC Peering →
      Private Resources

Options:
- Public endpoints
- Private Service Connect
- VPC Service Controls
```

### 3. Security
```
Data Encryption:
├─ At rest: CMEK (Customer-Managed Encryption Keys)
├─ In transit: TLS 1.2+
└─ Model artifacts: Encrypted in GCS

Access Control:
├─ IAM policies
├─ VPC-SC perimeters
└─ Private endpoints
```

### 4. Monitoring and Logging
```
Vertex AI Operations →
   Cloud Logging →
      Log Explorer

Vertex AI Metrics →
   Cloud Monitoring →
      Dashboards & Alerts
```

## Best Practices

### Architecture Design Principles

1. **Separation of Concerns**
   - Separate projects for dev/staging/prod
   - Isolate data, training, and serving

2. **Resource Organization**
   ```
   Organization
   └── Folder: ML Platform
       ├── Project: ml-dev
       ├── Project: ml-staging
       └── Project: ml-prod
   ```

3. **Network Security**
   - Use VPC-SC for sensitive workloads
   - Private endpoints for production
   - Firewall rules for access control

4. **Cost Optimization**
   - Use preemptible VMs for training
   - Auto-scaling for endpoints
   - Committed use discounts

5. **Monitoring Strategy**
   - Model performance metrics
   - Prediction latency tracking
   - Feature drift detection
   - Resource utilization monitoring

## Common Architecture Patterns

### Pattern 1: Batch ML Pipeline
```
BigQuery → Feature Engineering → Training → Model Registry → Batch Prediction → BigQuery
```

### Pattern 2: Real-Time Serving
```
Client → API Gateway → Vertex Endpoint → Prediction → Client
```

### Pattern 3: Continuous Training
```
New Data → Trigger (Cloud Scheduler) → Pipeline → Training → 
Evaluation → Auto-Deploy (if better) → Endpoint
```

### Pattern 4: A/B Testing
```
Traffic → Load Balancer → 
   ├─ Model A (70%) → Response
   └─ Model B (30%) → Response
```

## References

- [Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)
- [Architecture Diagrams](https://cloud.google.com/architecture)
- [Best Practices Guide](https://cloud.google.com/vertex-ai/docs/start/best-practices)
