from .attention import SBCAttention

class SBCTransformer(nn.Module):
    def __init__(self, vocab_size=2000, d_model=64):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, d_model)
        self.attn = SBCAttention(d_model)
        self.ff = nn.Sequential(
            nn.Linear(d_model, d_model//2),
            nn.ReLU(),
            nn.Linear(d_model//2, d_model)
        )
        self.lm_head = nn.Linear(d_model, vocab_size)
    
    def forward(self, x):
        # x: [seq_len]
        x = self.embed(x)  # [seq_len, d_model]
        x = x + self.attn(x)
        x = x + self.ff(x)
        return self.lm_head(x[-1:])  # Predict last token
