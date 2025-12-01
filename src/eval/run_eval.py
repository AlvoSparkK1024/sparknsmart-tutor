import yaml
import asyncio
from src.orchestration.orchestrator import Orchestrator

async def run_eval():
    with open("src/eval/scenarios.yaml", "r") as f:
        config = yaml.safe_load(f)
    
    orchestrator = Orchestrator()
    await orchestrator.setup()
    
    for scenario in config["scenarios"]:
        print(f"Running scenario: {scenario['name']}")
        # In a real eval, we'd inject these specific files or mock data
        # For now, just triggering the main flow
        await orchestrator.run_scenario(scenario["appliances"], scenario["tariff"])
        
    await orchestrator.shutdown()

if __name__ == "__main__":
    asyncio.run(run_eval())
