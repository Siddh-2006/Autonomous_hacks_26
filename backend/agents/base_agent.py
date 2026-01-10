# Shared agent logic
import time

class BaseAgent:
    def __init__(self, name):
        self.name = name
    
    def fetch_data(self):
        raise NotImplementedError
    
    def analyze(self, data):
        raise NotImplementedError
    
    def emit_signal(self, result):
        return {
            "agent": self.name,
            "signal": result,
            "timestamp": time.time()
        }