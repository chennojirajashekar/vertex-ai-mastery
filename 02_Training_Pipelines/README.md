# 02. Training Pipelines

## What is a Training Pipeline?
A training pipeline encapsulates the entire process of training a model: from data ingestion to model storage.

## Prebuilt vs. Custom Containers
- **Prebuilt Containers:** Provided by Google. Great for standard frameworks like TensorFlow or PyTorch.
- **Custom Containers:** You build a Docker image with your own dependencies. Necessary for niche libraries or complex setups.

## Distributed Training
Scaling your training across multiple GPUs or machines. Vertex AI handles the orchestration.

## Hyperparameter Tuning
Automatically finding the best "settings" (hyperparameters) for your model to get the highest accuracy.

---
**Next Step:** [Custom Training](../03_Custom_Training/README.md)
