from typing import Dict, Any, Callable, Optional
import asyncio
from src.orchestration.bus import MessageBus
from src.core.memory import Memory

class AgentRegistry:
    def __init__(self):
        self._agents: Dict[str, Any] = {}

    def register(self, name: str, agent: Any):
        self._agents[name] = agent

    def get(self, name: str) -> Optional[Any]:
        return self._agents.get(name)

class Runtime:
    def __init__(self):
        self.bus = MessageBus()
        self.memory = Memory()
        self.registry = AgentRegistry()
        self.config: Dict[str, Any] = {}

    def configure(self, config: Dict[str, Any]):
        self.config = config

    async def start(self):
        # Initialize all agents
        for name, agent in self.registry._agents.items():
            if hasattr(agent, 'initialize'):
                await agent.initialize(self)
        print("Runtime started.")

    async def stop(self):
        # Cleanup
        print("Runtime stopped.")
