"""PyTorch Custom Training on Vertex AI."""

import torch
import torch.nn as nn
from google.cloud import aiplatform

class SimpleModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(10, 1)
    
    def forward(self, x):
        return self.fc(x)

if __name__ == '__main__':
    model = SimpleModel()
    print('Training model...')
