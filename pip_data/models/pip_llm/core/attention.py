import torch
import torch.nn as nn
import math

class SBCAttention(nn.Module):
    def __init__(self, d_model):
        super().__init__()
        self.d_model = d_model
        self.qkv = nn.Linear(d_model, 3*d_model)
        self.out = nn.Linear(d_model, d_model)
    
    def forward(self, x):
        q, k, v = self.qkv(x).chunk(3, dim=-1)
        scores = q @ k.T / math.sqrt(self.d_model)
        attn = torch.softmax(scores, dim=-1)
        return self.out(attn @ v)
