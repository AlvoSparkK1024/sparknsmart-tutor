import sys
import traceback

with open("runner_log.txt", "w") as f:
    f.write("Starting runner...\n")
    try:
        import src.orchestration.orchestrator
        f.write("Import src.orchestration.orchestrator success\n")
    except Exception as e:
        f.write(f"Import failed: {e}\n")
        f.write(traceback.format_exc())
    
    try:
        from src.orchestration.orchestrator import Orchestrator
        f.write("Import Orchestrator class success\n")
        o = Orchestrator()
        f.write("Orchestrator instantiated\n")
    except Exception as e:
        f.write(f"Orchestrator usage failed: {e}\n")
        f.write(traceback.format_exc())

    f.write("Runner finished.\n")
