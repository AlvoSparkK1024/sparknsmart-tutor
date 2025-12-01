try:
    import asyncio
    print("asyncio ok")
    import os
    print("os ok")
    from dotenv import load_dotenv
    print("dotenv ok")
    from src.orchestration.orchestrator import Orchestrator
    print("Orchestrator import ok")
except Exception as e:
    print(f"Import Error: {e}")
