from typing import Dict, Any
from src.orchestration.runtime import Runtime

class SessionAgent:
    def __init__(self):
        self.runtime = None

    async def initialize(self, runtime: Runtime):
        self.runtime = runtime
        # Could subscribe to user messages to update state
        # For now, just a placeholder for session tracking
        pass
