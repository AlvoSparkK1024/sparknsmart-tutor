import asyncio
import os
import sys
import traceback
import logging
from dotenv import load_dotenv

# Manual logging setup
def log(msg):
    with open("debug_demo.log", "a") as f:
        f.write(msg + "\n")

log("Starting debug_demo.py")

try:
    log("Importing Orchestrator...")
    from src.orchestration.orchestrator import Orchestrator
    log("Orchestrator imported.")
except Exception as e:
    log(f"Error importing Orchestrator: {e}")
    log(traceback.format_exc())
    sys.exit(1)

# Load environment variables
log("Loading dotenv...")
load_dotenv()
log("Dotenv loaded.")

async def main():
    log("Entering main()")
    
    try:
        log("Instantiating Orchestrator...")
        orchestrator = Orchestrator()
        log("Orchestrator instantiated.")
        
        log("Calling orchestrator.setup()...")
        await orchestrator.setup()
        log("orchestrator.setup() complete.")
        
        appliances_file = "src/data/samples/appliances.json"
        tariff_file = "src/data/samples/tariff_telangana.json"
        
        if not os.path.exists(appliances_file) or not os.path.exists(tariff_file):
            log(f"Error: Sample data files not found at {os.getcwd()}")
            return

        log("Running scenario...")
        await orchestrator.run_scenario(appliances_file, tariff_file)
        log("Scenario run initiated.")
        
        log("Shutting down...")
        await orchestrator.shutdown()
        log("Shutdown complete.")
        
    except Exception as e:
        log(f"CRITICAL ERROR in main: {e}")
        log(traceback.format_exc())

if __name__ == "__main__":
    try:
        log("Calling asyncio.run(main())")
        asyncio.run(main())
        log("asyncio.run(main()) finished")
    except KeyboardInterrupt:
        log("Stopped by user.")
    except Exception as e:
        log(f"Fatal error: {e}")
        log(traceback.format_exc())
