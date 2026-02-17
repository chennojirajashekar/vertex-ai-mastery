"""Generative AI with Gemini Example."""

import vertexai
from vertexai.generative_models import GenerativeModel

# Initialize Vertex AI
vertexai.init(
    project='YOUR_PROJECT_ID',
    location='us-central1'
)

# Initialize Gemini model
model = GenerativeModel('gemini-pro')

# Generate content
response = model.generate_content(
    "Explain machine learning in simple terms."
)
print(response.text)

# Chat conversation
chat = model.start_chat()
response = chat.send_message("What is Vertex AI?")
print(response.text)

response = chat.send_message("How does it compare to AWS SageMaker?")
print(response.text)

# Function calling example
functions = [
    {
        "name": "get_weather",
        "description": "Get weather information",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string"}
            }
        }
    }
]

response = model.generate_content(
    "What's the weather in San Francisco?",
    tools=functions
)
print(response)
