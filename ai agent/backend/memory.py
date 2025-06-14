import time
from typing import List, Dict, Any

class MemoryStore:
    def __init__(self):
        self.store: List[Dict[str, Any]] = []

    def log(self, entry: Dict[str, Any]):
        entry["timestamp"] = time.time()
        self.store.append(entry)

    def get_all(self):
        return self.store

memory = MemoryStore()
