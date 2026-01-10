# Optional vector store for memory
import time
import json
import os

class SimpleVectorStore:
    """Simple in-memory vector store replacement for ChromaDB"""
    
    def __init__(self):
        self.documents = []
        self.storage_file = "storage/vector_memory.json"
        self.load_from_file()
    
    def add(self, documents, ids):
        """Add documents to store"""
        for doc, doc_id in zip(documents, ids):
            self.documents.append({
                "id": doc_id,
                "document": doc,
                "timestamp": time.time()
            })
        self.save_to_file()
    
    def query(self, query_texts, n_results=3):
        """Simple text matching query"""
        results = []
        query_text = query_texts[0].lower()
        
        # Simple keyword matching
        matches = []
        for doc in self.documents:
            if any(word in doc["document"].lower() for word in query_text.split()):
                matches.append(doc)
        
        # Return most recent matches
        matches.sort(key=lambda x: x["timestamp"], reverse=True)
        return {"documents": [matches[:n_results]]}
    
    def save_to_file(self):
        """Save to JSON file"""
        try:
            os.makedirs(os.path.dirname(self.storage_file), exist_ok=True)
            with open(self.storage_file, "w") as f:
                json.dump(self.documents, f, indent=2)
        except Exception as e:
            print(f"Error saving vector store: {e}")
    
    def load_from_file(self):
        """Load from JSON file"""
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, "r") as f:
                    self.documents = json.load(f)
        except Exception as e:
            print(f"Error loading vector store: {e}")
            self.documents = []

# Initialize simple vector store
vector_store = SimpleVectorStore()

def store_event(text):
    """Store event in vector database"""
    vector_store.add([text], [str(time.time())])

def search_similar(text):
    """Search for similar events"""
    return vector_store.query([text], n_results=3)