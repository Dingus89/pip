from collections import deque

class TokenCache:
    """Stores recent tokens as embeddings"""
    def __init__(self, model, maxlen=32):
        self.model = model
        self.cache = deque(maxlen=maxlen)
    
    def add(self, tokens):
        with torch.no_grad():
            embeds = self.model.embed(torch.tensor(tokens))
            self.cache.extend(embeds.unbind(0))
    
    def get_context(self):
        return torch.stack(list(self.cache)) if self.cache else None
