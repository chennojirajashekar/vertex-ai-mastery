# 🚦 Common Mistakes & Failures in Vertex AI

Building production-grade AI systems is hard. This section highlights common pitfalls, architectural mistakes, and real-world failure patterns observed in enterprise Vertex AI deployments.

---

## 🛑 1. Costly Mistakes (The "Wallet Breakers")

### **GPU Under-utilization**
*   **The Mistake:** Provisioning high-end GPUs (A100/L4) for simple inference or pre-processing tasks.
*   **The Failure:** Paying $3+/hour for a workload that only uses 5% of the GPU capacity.
*   **Best Practice:** Profile workloads first; use CPUs or T4 GPUs where possible.

### **Idle Endpoints & Workbenches**
*   **The Mistake:** Leaving Online Endpoints or Workbench instances running over the weekend without traffic.
*   **The Failure:** Accidental bills reaching thousands of dollars.
*   **Best Practice:** Enable **Idle Shutdown** for Workbenches and use autoscaling (min nodes = 0) for serverless inference.

---

## 📉 2. Model Performance Failures

### **Ignoring Training-Serving Skew**
*   **The Mistake:** Using different data processing scripts for training (Python/Pandas) and serving (Go/Java).
*   **The Failure:** The model performs perfectly in training but fails miserably on live data.
*   **Best Practice:** Use **Vertex AI Pipelines** to encapsulate the preprocessing logic.

### **Data Leakage in Time-Series**
*   **The Mistake:** Using future data to predict the past during training.
*   **The Failure:** Over-optimistic validation scores that crash in production.
*   **Best Practice:** Always use strict chronological splitting for temporal datasets.

---

## 🏗 3. Architectural Anti-Patterns

### **Monolithic Containers**
*   **The Mistake:** Packing data processing, training, and evaluation into a single 10GB Docker image.
*   **The Failure:** Slow startup times and impossible debugging.
*   **Best Practice:** Break down tasks into modular components in a **KFP (Kubeflow Pipelines)** workflow.

### **Manual Model Deployments**
*   **The Mistake:** Deploying models via the Google Cloud Console instead of CI/CD.
*   **The Failure:** Inconsistency between Dev and Prod environments; no rollback capability.
*   **Best Practice:** Use **GitHub Actions** or **Cloud Build** with the Vertex AI SDK.

---

## 🧪 4. Case Studies: Production Horror Stories

1.  **The $50k Mistake:** A startup left a distributed training job running with a bug in the convergence criteria.
2.  **The Ghost Model:** An engineer deleted a Model Registry entry that was still being used by a production endpoint, causing a total system outage.
3.  **The Prompt Injection:** A GenAI chatbot without safety filters was manipulated into revealing internal system prompts.

---

**Next Steps:**
Learn how to avoid these by following our [Security & Governance](../13_Security_and_Governance/README.md) and [Cost Optimization](../12_Cost_Optimization/README.md) guides.
