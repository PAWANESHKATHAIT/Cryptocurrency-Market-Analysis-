# pipeline_orchestrator.py

# Import the main functions from your ETL and Segmentation scripts
from etl_crypto import run_etl_load
from segment_and_load import run_segmentation_update

if __name__ == "__main__":
    print("--- Starting Crypto Market Analytics Pipeline Orchestration ---")

    # Step 1: Run the ETL (Extract, Transform, Load) process
    run_etl_load()

    # Step 2: Run the Segmentation and Update process
    # This ensures segmentation happens AFTER the latest data is loaded
    run_segmentation_update()

    print("--- Crypto Market Analytics Pipeline Orchestration Finished ---")
