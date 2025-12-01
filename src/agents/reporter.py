import plotly.graph_objects as go
import os
from typing import Dict, Any
from src.orchestration.runtime import Runtime

class ReporterAgent:
    def __init__(self):
        self.runtime = None

    async def initialize(self, runtime: Runtime):
        self.runtime = runtime
        self.runtime.bus.subscribe("analysis_complete", self.create_chart)

    async def create_chart(self, data: Dict[str, Any]):
        results = data.get("results", [])
        if not results:
            return

        names = [r['appliance_name'] for r in results]
        costs = [r['monthly_cost'] for r in results]

        fig = go.Figure(data=[go.Bar(x=names, y=costs)])
        fig.update_layout(title_text='Monthly Cost per Appliance', xaxis_title='Appliance', yaxis_title='Cost')
        
        # Ensure output directory exists
        output_dir = "outputs"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        chart_path = os.path.join(output_dir, "cost_chart.png")
        # In a real headless env, we might need kaleido or similar. 
        # For this demo, we'll try to write it, or skip if dependencies are missing.
        try:
            fig.write_image(chart_path)
            await self.runtime.bus.publish("chart_ready", {"chart_path": chart_path})
        except Exception as e:
            print(f"Failed to generate chart image (missing kaleido?): {e}")
            # Proceed without chart
            await self.runtime.bus.publish("chart_ready", {"chart_path": None})
