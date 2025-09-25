import pandas as pd

# Load the Excel file from the data folder
df = pd.read_excel("../data/farmer_dataset_makueni.xlsx")

# Show basic info
print("✅ Columns in the dataset:")
print(df.columns)

print("\n✅ First 5 rows of data:")
print(df.head())
