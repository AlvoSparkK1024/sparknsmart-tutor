import os
import google.generativeai as genai
from typing import Dict, Any
from src.orchestration.runtime import Runtime
from src.core.schemas import Lesson

class AdvisorAgent:
    def __init__(self):
        self.runtime = None
        self.model = None

    async def initialize(self, runtime: Runtime):
        self.runtime = runtime
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
        self.runtime.bus.subscribe("analysis_complete", self.generate_lesson)

    async def generate_lesson(self, data: Dict[str, Any]):
        results = data.get("results", [])
        if not self.model:
            print("Gemini API Key not found. Skipping lesson generation.")
            return

        # Construct prompt
        prompt = f"""
        You are an energy efficiency expert. Analyze the following appliance data and create a short lesson.
        Data: {results}
        
        Output JSON format:
        {{
            "topic": "Topic Title",
            "content": "Short explanation of the main issue.",
            "actions": ["Action 1", "Action 2"],
            "estimated_savings": "Estimated savings text"
        }}
        """
        
        try:
            response = await self.model.generate_content_async(prompt)
            # In a real app, we'd parse the JSON strictly. For now, assuming valid JSON or handling text.
            # Simplified for demo: just taking the text if not JSON
            
            # Mocking parsed response for robustness in this scaffold
            lesson = Lesson(
                topic="Energy Optimization",
                content=response.text,
                actions=["Check power factor", "Reduce usage hours"],
                estimated_savings="10-15%"
            )
            
            await self.runtime.bus.publish("lesson_ready", lesson.dict())
            
        except Exception as e:
            print(f"Error generating lesson: {e}")
