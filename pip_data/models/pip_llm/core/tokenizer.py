class SBCTokenizer:
    def __init__(self):
        self.word2id = {"<UNK>": 0}
        self.id2word = ["<UNK>"]
    
    def build_from_file(self, path, max_vocab=2000):
        """Build vocab from a text file (saves RAM during training)"""
        word_counts = {}
        with open(path) as f:
            for line in f:
                for word in line.strip().split():
                    word_counts[word] = word_counts.get(word, 0) + 1
        
        # Top N words
        top_words = sorted(word_counts.items(), key=lambda x: -x[1])[:max_vocab-1]
        self.word2id.update({w: i+1 for i, (w, _) in enumerate(top_words)})
        self.id2word += [w for w, _ in top_words]
    
    def encode(self, text):
        return [self.word2id.get(word, 0) for word in text.split()]
