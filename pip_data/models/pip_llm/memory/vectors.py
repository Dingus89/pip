import sqlite3
import numpy as np

class VectorMemory:
    """Disk-based long-term memory"""
    def __init__(self, path=":memory:"):
        self.conn = sqlite3.connect(path)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY,
                text TEXT,
                vector BLOB
            )""")
    
    def add(self, text, vector):
        self.conn.execute("INSERT INTO memories (text, vector) VALUES (?, ?)",
                          (text, vector.numpy().tobytes()))
        self.conn.commit()
    
    def search(self, query_vec, k=3):
        cur = self.conn.execute("SELECT text, vector FROM memories")
        results = []
        for text, vec_bytes in cur:
            vec = np.frombuffer(vec_bytes, dtype=np.float32)
            sim = np.dot(query_vec, vec) / (np.linalg.norm(query_vec) * np.linalg.norm(vec))
            results.append((sim, text))
        return [text for _, text in sorted(results, reverse=True)[:k]]
