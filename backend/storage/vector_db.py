try:
    import chromadb
    from chromadb.utils import embedding_functions
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False
    print("[VECTOR] ChromaDB not available. Using Mock Memory.")

import os
import datetime
import uuid

# We use the free HuggingFace model via Chroma's built-in utility or SentenceTransformers
# For simplicity/portability, we'll try to use the default all-MiniLM-L6-v2
# Check if we need to explicitly set it up.

class MockVectorDB:
    def __init__(self):
        self.collection = self
    
    def count(self):
        return 0
    
    def add(self, documents, metadatas, ids):
        pass
        
    def query(self, query_texts, n_results):
        return {"ids": [[]], "documents": [[]], "metadatas": [[]]}

class VectorDB:
    def __init__(self):
        # Persistent storage in /backend/storage/chroma_data
        base_path = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_path, "chroma_data")
        
        if CHROMA_AVAILABLE:
            self.client = chromadb.PersistentClient(path=db_path)
            
            # Use a high-quality free model
            self.ef = embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="all-MiniLM-L6-v2"
            )
            
            self.collection = self.client.get_or_create_collection(
                name="executive_narratives",
                embedding_function=self.ef
            )
        else:
            self.client = None
            self.collection = MockVectorDB()
        
    def store_narrative(self, agent: str, text: str, metadata: dict):
        """
        Stores an executive statement or summary into vector memory.
        """
        if not text or len(text) < 10:
            return # Skip empty/short texts
            
        # Add timestamps if missing
        if "timestamp" not in metadata:
            metadata["timestamp"] = datetime.datetime.now().isoformat()
            
        metadata["agent"] = agent
        
        doc_id = str(uuid.uuid4())
        
        if CHROMA_AVAILABLE:
            self.collection.add(
                documents=[text],
                metadatas=[metadata],
                ids=[doc_id]
            )
            print(f"[VECTOR] Stored {agent} narrative: '{text[:30]}...'")
        else:
            print(f"[VECTOR-MOCK] Stored {agent} narrative: '{text[:30]}...'")

    def find_similar_events(self, query_text: str, n=3):
        """
        Finds historical events semantically similar to the current situation.
        """
        if CHROMA_AVAILABLE:
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n
            )
            return results
        else:
            return {"ids": [[]], "documents": [[]], "metadatas": [[]]}

# Singleton instance
vector_memory = VectorDB()
