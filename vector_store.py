from typing import Dict
from langchain_community.vectorstores import FAISS

class VectorStoreManager:
    def __init__(self):
        self.store: Dict[str, FAISS] = {}

    def add(self, sid, vs):
        self.store[sid] = vs

    def retriever(self, sid):
        return self.store[sid].as_retriever(search_kwargs={"k": 5})

    def exists(self, sid):
        return sid in self.store

vector_store_manager = VectorStoreManager()
