import asyncio
import json
from src.orchestration.runtime import Runtime
from src.agents.advisor import AdvisorAgent
from src.agents.analyzer import AnalyzerAgent
from src.agents.reporter import ReporterAgent
from src.agents.notifier import NotifierAgent
from src.agents.session import SessionAgent
from src.agents.notebooklm_agent import NotebookLMAgent


class Orchestrator:
    def __init__(self):
        self.runtime = Runtime()

    async def setup(self):
        # Register Agents
        self.runtime.registry.register("analyzer", AnalyzerAgent())
        self.runtime.registry.register("advisor", AdvisorAgent())
        self.runtime.registry.register("reporter", ReporterAgent())
        self.runtime.registry.register("notifier", NotifierAgent())
        self.runtime.registry.register("session", SessionAgent())
        self.runtime.registry.register("notebooklm", NotebookLMAgent())
        
        
        await self.runtime.start()

    async def run_scenario(self, input_text: str, input_type: str = "text"):
        # Trigger lecture generation
        await self.runtime.bus.publish("generate_lecture", {
            "text": input_text,
            "type": input_type
        })
        
        # Keep running for a bit to allow async processing
        await asyncio.sleep(15) 

    async def shutdown(self):
        await self.runtime.stop()
