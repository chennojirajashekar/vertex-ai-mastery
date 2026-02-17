# 10. Cost Optimization

## Overview
Vertex AI can be expensive if not managed correctly. This guide focuses on strategies to minimize costs while maintaining performance.

## Key Strategies
- **Spot Instances:** Using preemptible VMs for training pipelines.
- **Auto-scaling:** Configuring endpoints to scale to zero when idle (where supported).
- **Resource Monitoring:** Using Cloud Monitoring and Budgets to track AI spend.
- **Model Quantization:** Reducing model size to lower serving costs.

## Common Cost Traps
- **Idle Endpoints:** Forgetting to delete test endpoints.
- **Over-provisioning GPUs:** Using high-end GPUs for simple tasks.
- **Data Egress:** Transferring large datasets across regions.

---

**Next Step:** [Security & Governance](../13_Security_and_Governance/README.md)
