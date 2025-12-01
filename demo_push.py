import asyncio
import os
import sys
import traceback
import logging
from dotenv import load_dotenv
from src.orchestration.orchestrator import Orchestrator

# Setup logging to file
logging.basicConfig(
    filename='demo.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w'
)

# Load environment variables
load_dotenv()

async def main():
    logging.info("Starting SPARKnSMART (SNS) Demo...")
    print("Starting SPARKnSMART (SNS) Demo...", flush=True)
    
    try:
        orchestrator = Orchestrator()
        await orchestrator.setup()
        
        appliances_file = "src/data/samples/appliances.json"
        tariff_file = "src/data/samples/tariff_telangana.json"
        
        if not os.path.exists(appliances_file) or not os.path.exists(tariff_file):
            logging.error(f"Error: Sample data files not found at {os.getcwd()}")
            return

        logging.info("Running scenario...")
        await orchestrator.run_scenario(appliances_file, tariff_file)
        
        logging.info("Scenario complete. Shutting down...")
        await orchestrator.shutdown()
        
    except Exception as e:
        logging.error(f"CRITICAL ERROR: {e}")
        logging.error(traceback.format_exc())
        print(f"CRITICAL ERROR: {e}", file=sys.stderr)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Stopped by user.")
    except Exception as e:
        logging.critical(f"Fatal error: {e}")
        logging.critical(traceback.format_exc())
