import pandas as pd

# Load the dataset
df = pd.read_excel("../data/farmer_dataset_makueni.xlsx")

# ✅ Show missing values per column
print("\n🔍 Missing values:")
print(df.isnull().sum())

# ✅ Check data types
print("\n🔍 Data types:")
print(df.dtypes)

# ✅ Preview GPS format
print("\n🗺️ Sample GPS coordinates:")
print(df["GPS Coordinates"].head())
