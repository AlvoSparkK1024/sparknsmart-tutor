from typing import Dict, Any
from src.orchestration.runtime import Runtime
from src.core.schemas import Message

class NotifierAgent:
    def __init__(self):
        self.runtime = None
        self.pending_lesson = None
        self.pending_chart = None

    async def initialize(self, runtime: Runtime):
        self.runtime = runtime
        self.runtime.bus.subscribe("lesson_ready", self.on_lesson)
        self.runtime.bus.subscribe("chart_ready", self.on_chart)

    async def on_lesson(self, data: Dict[str, Any]):
        self.pending_lesson = data
        await self.check_and_send()

    async def on_chart(self, data: Dict[str, Any]):
        self.pending_chart = data.get("chart_path")
        await self.check_and_send()

    async def check_and_send(self):
        if self.pending_lesson: # Chart is optional or might arrive later/earlier. 
            # For simplicity, if we have a lesson, we try to send. 
            # In a real system, we'd wait for a specific signal or timeout.
            
            content = f"**{self.pending_lesson['topic']}**\n\n"
            content += f"{self.pending_lesson['content']}\n\n"
            content += "**Actions:**\n" + "\n".join([f"- {a}" for a in self.pending_lesson['actions']])
            
            msg = Message(content=content, image_path=self.pending_chart)
            
            await self.runtime.bus.publish("send_message", msg.dict())
            
            # Reset
            self.pending_lesson = None
            self.pending_chart = None
