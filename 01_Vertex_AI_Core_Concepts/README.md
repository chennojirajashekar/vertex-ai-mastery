# 01. Vertex AI Core Concepts

## IAM & Security
Before building, you need to set up permissions.
- **Service Accounts:** The "identities" that perform actions on your behalf.
- **Roles:** Permissions assigned to these accounts (e.g., `Vertex AI Admin`).

## Workbench (Notebooks)
- **Managed Notebooks:** Google handles the infrastructure.
- **User-managed Notebooks:** You have full control over the VM.

## Training vs. Serving
- **Training:** Building the model using data.
- **Serving:** Providing predictions once the model is built.

## Model Registry
The central place to store and version your models. It's like Git but for ML models.

---
**Next Step:** [Training Pipelines](../02_Training_Pipelines/README.md)
