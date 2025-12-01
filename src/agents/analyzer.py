from typing import List, Dict, Any
from src.core.schemas import Appliance, Tariff, AnalysisResult
from src.orchestration.runtime import Runtime

class AnalyzerAgent:
    def __init__(self):
        self.runtime = None

    async def initialize(self, runtime: Runtime):
        self.runtime = runtime
        self.runtime.bus.subscribe("analyze_appliances", self.analyze)

    async def analyze(self, data: Dict[str, Any]):
        appliances_data = data.get("appliances", [])
        tariff_data = data.get("tariff", {})
        
        appliances = [Appliance(**a) for a in appliances_data]
        tariff = Tariff(**tariff_data)
        
        results = []
        for app in appliances:
            monthly_kwh = (app.power_watts * app.daily_usage_hours * 30) / 1000
            
            # Simple tiered calculation (simplified)
            rate = tariff.tiers[0]["rate"] # Default to first tier for simplicity in this demo
            for tier in tariff.tiers:
                if monthly_kwh > tier.get("limit", float('inf')):
                    rate = tier["rate"]
            
            monthly_cost = monthly_kwh * rate
            
            suggestions = []
            if app.power_factor < 0.9:
                suggestions.append(f"Low Power Factor ({app.power_factor}). Consider a capacitor bank.")
            if app.harmonics_thd > 5.0:
                suggestions.append(f"High Harmonics ({app.harmonics_thd}%). Check for non-linear loads.")
                
            results.append(AnalysisResult(
                appliance_name=app.name,
                monthly_kwh=monthly_kwh,
                monthly_cost=monthly_cost,
                pf_penalty=0.0, # Placeholder
                suggestions=suggestions
            ))
            
        # Publish results
        await self.runtime.bus.publish("analysis_complete", {"results": [r.dict() for r in results]})
