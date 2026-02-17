"""IAM and Service Account Management for Vertex AI.

This module demonstrates how to manage IAM permissions, service accounts,
and role bindings for Vertex AI resources.
"""

import os
from typing import List, Dict, Optional
from google.cloud import resourcemanager_v3
from google.iam.v1 import iam_policy_pb2
from google.iam.v1 import policy_pb2
from google.cloud import iam_credentials_v1
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VertexAIIAMManager:
    """Manage IAM permissions and service accounts for Vertex AI."""
    
    # Common Vertex AI IAM roles
    VERTEX_AI_ROLES = {
        "admin": "roles/aiplatform.admin",
        "user": "roles/aiplatform.user",
        "viewer": "roles/aiplatform.viewer",
        "custom_code_service_agent": "roles/aiplatform.customCodeServiceAgent",
        "service_agent": "roles/aiplatform.serviceAgent",
    }
    
    def __init__(self, project_id: str):
        """Initialize IAM manager.
        
        Args:
            project_id: GCP Project ID
        """
        self.project_id = project_id
        self.project_name = f"projects/{project_id}"
        
    def create_service_account(self, 
                               account_id: str, 
                               display_name: str,
                               description: str = "") -> Dict:
        """Create a service account for Vertex AI.
        
        Args:
            account_id: Service account ID (e.g., 'vertex-ai-sa')
            display_name: Human-readable name
            description: Service account description
            
        Returns:
            Service account details
        """
        try:
            from google.cloud import iam_admin_v1
            
            client = iam_admin_v1.IAMClient()
            
            service_account = iam_admin_v1.ServiceAccount(
                display_name=display_name,
                description=description or f"Service account for Vertex AI {account_id}"
            )
            
            request = iam_admin_v1.CreateServiceAccountRequest(
                name=self.project_name,
                account_id=account_id,
                service_account=service_account
            )
            
            sa = client.create_service_account(request=request)
            logger.info(f"Created service account: {sa.email}")
            
            return {
                "email": sa.email,
                "name": sa.name,
                "unique_id": sa.unique_id
            }
            
        except Exception as e:
            logger.error(f"Failed to create service account: {str(e)}")
            raise
    
    def grant_vertex_ai_role(self, 
                            service_account_email: str,
                            role: str = "user") -> bool:
        """Grant Vertex AI role to a service account.
        
        Args:
            service_account_email: Service account email
            role: Role key from VERTEX_AI_ROLES (default: 'user')
            
        Returns:
            True if successful
        """
        try:
            from google.cloud import resourcemanager_v3
            
            client = resourcemanager_v3.ProjectsClient()
            
            # Get current IAM policy
            policy = client.get_iam_policy(
                request={"resource": self.project_name}
            )
            
            # Add new binding
            role_name = self.VERTEX_AI_ROLES.get(role, role)
            member = f"serviceAccount:{service_account_email}"
            
            binding = next(
                (b for b in policy.bindings if b.role == role_name),
                None
            )
            
            if binding:
                if member not in binding.members:
                    binding.members.append(member)
            else:
                new_binding = policy_pb2.Binding(
                    role=role_name,
                    members=[member]
                )
                policy.bindings.append(new_binding)
            
            # Set updated policy
            client.set_iam_policy(
                request={
                    "resource": self.project_name,
                    "policy": policy
                }
            )
            
            logger.info(f"Granted {role_name} to {service_account_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to grant role: {str(e)}")
            return False
    
    def create_service_account_key(self, 
                                   service_account_email: str,
                                   key_file_path: str = "./key.json") -> str:
        """Create and download service account key.
        
        Args:
            service_account_email: Service account email
            key_file_path: Path to save the key file
            
        Returns:
            Path to the downloaded key file
        """
        try:
            from google.cloud import iam_admin_v1
            
            client = iam_admin_v1.IAMClient()
            
            name = f"projects/{self.project_id}/serviceAccounts/{service_account_email}"
            
            key = client.create_service_account_key(
                request={
                    "name": name,
                    "private_key_type": iam_admin_v1.ServiceAccountPrivateKeyType.TYPE_GOOGLE_CREDENTIALS_FILE
                }
            )
            
            # Save key to file
            with open(key_file_path, 'wb') as f:
                f.write(key.private_key_data)
            
            logger.info(f"Service account key saved to {key_file_path}")
            logger.warning("IMPORTANT: Keep this key file secure!")
            
            return key_file_path
            
        except Exception as e:
            logger.error(f"Failed to create key: {str(e)}")
            raise
    
    def list_service_accounts(self) -> List[Dict]:
        """List all service accounts in the project.
        
        Returns:
            List of service account details
        """
        try:
            from google.cloud import iam_admin_v1
            
            client = iam_admin_v1.IAMClient()
            
            service_accounts = []
            for sa in client.list_service_accounts(request={"name": self.project_name}):
                service_accounts.append({
                    "email": sa.email,
                    "display_name": sa.display_name,
                    "unique_id": sa.unique_id,
                    "description": sa.description
                })
            
            logger.info(f"Found {len(service_accounts)} service accounts")
            return service_accounts
            
        except Exception as e:
            logger.error(f"Failed to list service accounts: {str(e)}")
            return []
    
    def get_iam_policy(self) -> Dict:
        """Get current IAM policy for the project.
        
        Returns:
            IAM policy as dictionary
        """
        try:
            from google.cloud import resourcemanager_v3
            
            client = resourcemanager_v3.ProjectsClient()
            policy = client.get_iam_policy(
                request={"resource": self.project_name}
            )
            
            policy_dict = {
                "bindings": [],
                "etag": policy.etag,
                "version": policy.version
            }
            
            for binding in policy.bindings:
                policy_dict["bindings"].append({
                    "role": binding.role,
                    "members": list(binding.members)
                })
            
            return policy_dict
            
        except Exception as e:
            logger.error(f"Failed to get IAM policy: {str(e)}")
            return {}
    
    def setup_vertex_ai_service_account(self, 
                                       account_id: str = "vertex-ai-sa",
                                       create_key: bool = False) -> Dict:
        """Complete setup of a Vertex AI service account.
        
        Args:
            account_id: Service account ID
            create_key: Whether to create and download a key
            
        Returns:
            Service account details
        """
        logger.info(f"Setting up Vertex AI service account: {account_id}")
        
        # Create service account
        sa = self.create_service_account(
            account_id=account_id,
            display_name=f"Vertex AI {account_id}",
            description="Service account for Vertex AI operations"
        )
        
        # Grant necessary roles
        roles_to_grant = ["user", "custom_code_service_agent"]
        for role in roles_to_grant:
            self.grant_vertex_ai_role(sa["email"], role)
        
        # Optionally create key
        if create_key:
            key_path = f"./credentials/{account_id}-key.json"
            os.makedirs("./credentials", exist_ok=True)
            sa["key_path"] = self.create_service_account_key(
                sa["email"], 
                key_path
            )
        
        logger.info("Service account setup complete!")
        return sa


def main():
    """Main function to demonstrate IAM management."""
    PROJECT_ID = os.getenv("GCP_PROJECT_ID", "your-project-id")
    
    iam_manager = VertexAIIAMManager(PROJECT_ID)
    
    print("\n=" * 60)
    print("Vertex AI IAM Management Demo")
    print("=" * 60)
    
    # List existing service accounts
    print("\n1. Listing existing service accounts...")
    accounts = iam_manager.list_service_accounts()
    for sa in accounts:
        print(f"  - {sa['email']} ({sa['display_name']})")
    
    # Display current IAM policy
    print("\n2. Current IAM Policy (Vertex AI roles only)...")
    policy = iam_manager.get_iam_policy()
    for binding in policy.get("bindings", []):
        if "aiplatform" in binding["role"]:
            print(f"  Role: {binding['role']}")
            for member in binding["members"][:3]:  # Show first 3
                print(f"    - {member}")
    
    # Example: Create new service account (commented out)
    # print("\n3. Creating new service account...")
    # new_sa = iam_manager.setup_vertex_ai_service_account(
    #     account_id="vertex-ai-demo",
    #     create_key=False  # Set to True to create key
    # )
    # print(f"  Created: {new_sa['email']}")
    
    print("\n" + "=" * 60)
    print("Demo complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
