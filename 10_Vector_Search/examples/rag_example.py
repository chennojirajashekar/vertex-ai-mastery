"""Vector Search and RAG Example."""

from google.cloud import aiplatform
from vertexai.language_models import TextEmbeddingModel
import vertexai

# Initialize Vertex AI
vertexai.init(
    project='YOUR_PROJECT_ID',
    location='us-central1'
)

# Create embeddings
model = TextEmbeddingModel.from_pretrained('textembedding-gecko@001')
texts = [
    "Machine learning is a subset of AI",
    "Deep learning uses neural networks",
    "Vertex AI is Google's ML platform"
]

embeddings = model.get_embeddings(texts)
for i, embedding in enumerate(embeddings):
    print(f"Text {i}: {len(embedding.values)} dimensions")

# Create Vector Search index
index = aiplatform.MatchingEngineIndex.create_tree_ah_index(
    display_name='my-index',
    dimensions=768,
    approximate_neighbors_count=10
)

print(f"Index created: {index.resource_name}")

# Deploy index to endpoint
endpoint = aiplatform.MatchingEngineIndexEndpoint.create(
    display_name='my-endpoint',
    public_endpoint_enabled=True
)

deployed_index = endpoint.deploy_index(
    index=index,
    deployed_index_id='deployed_index_id'
)

print(f"Index deployed to endpoint: {endpoint.resource_name}")

# Perform similarity search
query_embedding = model.get_embeddings(["What is AI?"])[0].values
response = endpoint.find_neighbors(
    deployed_index_id='deployed_index_id',
    queries=[query_embedding],
    num_neighbors=5
)

print(f"Similar items: {response}")
