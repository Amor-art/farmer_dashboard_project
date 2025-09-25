import os
import pandas as pd

# Define paths
source_folder = "../data"
target_folder = "../data"

# Loop through all Excel files
for filename in os.listdir(source_folder):
    if filename.endswith(".xlsx") and filename.startswith("farmer_dataset_"):
        # Extract county name
        county_raw = filename.replace("farmer_dataset_", "").replace(".xlsx", "")
        county_clean = county_raw.lower().replace("-", "_").replace(" ", "_")

        # Read Excel file
        file_path = os.path.join(source_folder, filename)
        df = pd.read_excel(file_path)

        # Save as CSV
        csv_name = f"{county_clean}_farmers.csv"
        csv_path = os.path.join(target_folder, csv_name)
        df.to_csv(csv_path, index=False)

        print(f"✅ Converted: {filename} → {csv_name}")
