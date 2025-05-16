import torch
from core.tokenizer import SBCTokenizer
from core.model import SBCTransformer
from memory.cache import TokenCache
from memory.vectors import VectorMemory

class TinyLLM:
    def __init__(self):
        # Core components
        self.tokenizer = SBCTokenizer()
        self.model = SBCTransformer()
        self.cache = TokenCache(self.model)
        self.memory = VectorMemory()
        
        # Config
        self.max_seq_len = 32  # Tokens
        
        # Optimize for SBC
        self.model.eval()
        torch.set_grad_enabled(False)
    
    def process(self, text):
        # Tokenize
        tokens = self.tokenizer.encode(text)[-self.max_seq_len:]
        
        # Retrieve context
        context = self.cache.get_context()
        if context is not None:
            tokens = torch.cat([context, torch.tensor(tokens)])
        
        # Predict
        output = self.model(tokens[-self.max_seq_len:])
        predicted = output.argmax().item()
        
        # Update systems
        self.cache.add(tokens)
        self._update_memory(text, tokens)
        
        return self.tokenizer.id2word[predicted]
    
    def _update_memory(self, text, tokens):
        """Store important info in long-term memory"""
        if len(tokens) >= 4:  # Minimal meaningful length
            with torch.no_grad():
                vec = self.model.embed(torch.tensor(tokens)).mean(0)  # Average embedding
            self.memory.add(text, vec)
