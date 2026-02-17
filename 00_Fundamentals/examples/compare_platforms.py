"""Comprehensive comparison: Vertex AI vs AWS SageMaker vs Azure ML.

This module provides detailed comparisons, feature matrices,
and decision-making guidelines for choosing the right platform.
"""

from dataclasses import dataclass
from typing import List, Dict
from enum import Enum


class PlatformFeature(Enum):
    """Enumeration of key ML platform features."""
    AUTOML = "AutoML Capabilities"
    CUSTOM_TRAINING = "Custom Training"
    MODEL_REGISTRY = "Model Registry"
    DEPLOYMENT = "Model Deployment"
    PIPELINES = "ML Pipelines"
    EXPLAINABILITY = "Model Explainability"
    MONITORING = "Model Monitoring"
    FEATURE_STORE = "Feature Store"
    PRICING = "Cost Efficiency"
    INTEGRATION = "Cloud Integration"


@dataclass
class PlatformComparison:
    """Data class for platform comparison metrics."""
    name: str
    automl_support: str
    custom_training: str
    managed_notebooks: str
    model_registry: str
    deployment_options: List[str]
    pricing_model: str
    best_for: List[str]
    limitations: List[str]
    

class MLPlatformComparator:
    """Compare major ML platforms across multiple dimensions."""
    
    def __init__(self):
        self.platforms = self._initialize_platforms()
    
    def _initialize_platforms(self) -> Dict[str, PlatformComparison]:
        """Initialize platform comparison data."""
        return {
            "vertex_ai": PlatformComparison(
                name="Google Cloud Vertex AI",
                automl_support="Excellent (Tables, Vision, NLP, Video)",
                custom_training="Full support with pre-built containers",
                managed_notebooks="Vertex AI Workbench",
                model_registry="Native with versioning & lineage",
                deployment_options=[
                    "Online prediction (real-time)",
                    "Batch prediction",
                    "Private endpoints",
                    "Autoscaling"
                ],
                pricing_model="Pay-per-use, committed use discounts",
                best_for=[
                    "Google Cloud native projects",
                    "Unified ML workflow",
                    "AutoML requirements",
                    "TensorFlow/JAX workloads"
                ],
                limitations=[
                    "Younger than AWS SageMaker",
                    "Smaller community",
                    "Less 3rd-party integrations"
                ]
            ),
            "sagemaker": PlatformComparison(
                name="AWS SageMaker",
                automl_support="Good (AutoPilot)",
                custom_training="Extensive framework support",
                managed_notebooks="SageMaker Studio",
                model_registry="SageMaker Model Registry",
                deployment_options=[
                    "Real-time endpoints",
                    "Batch transform",
                    "Multi-model endpoints",
                    "Serverless inference"
                ],
                pricing_model="Pay-per-use, savings plans",
                best_for=[
                    "AWS ecosystem",
                    "Mature ML workflows",
                    "Large model zoo",
                    "Extensive algorithm library"
                ],
                limitations=[
                    "Complex pricing",
                    "Steeper learning curve",
                    "Can be expensive at scale"
                ]
            ),
            "azure_ml": PlatformComparison(
                name="Azure Machine Learning",
                automl_support="Good (Automated ML)",
                custom_training="Strong PyTorch/ONNX support",
                managed_notebooks="Azure ML Studio",
                model_registry="Azure ML Model Registry",
                deployment_options=[
                    "Azure Kubernetes Service",
                    "Azure Container Instances",
                    "Azure Functions",
                    "IoT Edge"
                ],
                pricing_model="Pay-per-use, reserved instances",
                best_for=[
                    "Microsoft ecosystem",
                    "Enterprise integrations",
                    "MLOps with Azure DevOps",
                    ".NET applications"
                ],
                limitations=[
                    "Less mature than SageMaker",
                    "UI can be complex",
                    "Documentation gaps"
                ]
            )
        }
    
    def print_comparison_table(self):
        """Print a formatted comparison table."""
        print("\n" + "="*80)
        print(" " * 20 + "ML PLATFORM COMPARISON")
        print("="*80 + "\n")
        
        for platform_key, platform in self.platforms.items():
            print(f"\n{'='*60}")
            print(f"Platform: {platform.name}")
            print(f"{'='*60}")
            print(f"AutoML Support: {platform.automl_support}")
            print(f"Custom Training: {platform.custom_training}")
            print(f"Notebooks: {platform.managed_notebooks}")
            print(f"Model Registry: {platform.model_registry}")
            print(f"\nDeployment Options:")
            for option in platform.deployment_options:
                print(f"  • {option}")
            print(f"\nPricing: {platform.pricing_model}")
            print(f"\nBest For:")
            for use_case in platform.best_for:
                print(f"  ✓ {use_case}")
            print(f"\nLimitations:")
            for limitation in platform.limitations:
                print(f"  ✗ {limitation}")
            print()
    
    def get_recommendation(self, requirements: Dict[str, str]) -> str:
        """Get platform recommendation based on requirements."""
        cloud_provider = requirements.get("cloud_provider", "")
        
        if "google" in cloud_provider.lower() or "gcp" in cloud_provider.lower():
            return "vertex_ai"
        elif "aws" in cloud_provider.lower():
            return "sagemaker"
        elif "azure" in cloud_provider.lower() or "microsoft" in cloud_provider.lower():
            return "azure_ml"
        
        # Default recommendation
        return "vertex_ai"  # Unified experience and modern architecture


def main():
    """Main function to demonstrate platform comparison."""
    comparator = MLPlatformComparator()
    
    print("\nWelcome to ML Platform Comparison Tool")
    print("This tool helps you compare Vertex AI, SageMaker, and Azure ML\n")
    
    # Print detailed comparison
    comparator.print_comparison_table()
    
    # Example recommendation
    requirements = {"cloud_provider": "Google Cloud"}
    recommended = comparator.get_recommendation(requirements)
    platform_name = comparator.platforms[recommended].name
    
    print("\n" + "="*80)
    print(f"Based on your requirements, we recommend: {platform_name}")
    print("="*80)


if __name__ == "__main__":
    main()
