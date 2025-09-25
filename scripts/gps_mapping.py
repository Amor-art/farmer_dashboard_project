import pandas as pd

# Load the dataset
df = pd.read_excel("data/farmer_dataset_makueni.xlsx")

# Split GPS Coordinates into Latitude and Longitude
df[["Latitude", "Longitude"]] = df["GPS Coordinates"].str.split(",", expand=True)
df["Latitude"] = df["Latitude"].astype(float)
df["Longitude"] = df["Longitude"].astype(float)

# ✅ Show sample coordinates
print("\n🗺️ Sample mapped coordinates:")
print(df[["Farmer Name", "Location", "Latitude", "Longitude"]].head())

# ✅ Save cleaned version for dashboard use
df.to_csv("data/farmer_data_cleaned.csv", index=False)
print("\n✅ Cleaned data with GPS saved to 'farmer_data_cleaned.csv'")
