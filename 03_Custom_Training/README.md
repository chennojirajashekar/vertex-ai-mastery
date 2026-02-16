# 03. Custom Training

## When to use Custom Training?
Use custom training when AutoML doesn't provide the level of control or the specific algorithm you need.

## Key Steps
1. **Prepare your script:** Write your training code in Python.
2. **Containerize:** Build a Docker image (optional but recommended for complex dependencies).
3. **Submit Job:** Use the Vertex AI SDK or CLI to start the training.

## Checkpointing
Always save checkpoints of your model during training. This allows you to resume if the job fails.

## Frameworks
- **TensorFlow:** Deep integration with Vertex AI.
- **PyTorch:** Fully supported with prebuilt containers.
- **XGBoost:** Great for tabular data.

---
**Next Step:** [AutoML](../04_AutoML/README.md)
