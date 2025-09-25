import pandas as pd

# Load the dataset
df = pd.read_excel("../data/farmer_dataset_makueni.xlsx")

# Define seasonal columns for each fruit
seasonal_columns = {
    "Mango": ["Mango Season 1", "Mango Season 2", "Mango Season 3"],
    "Hass": ["Hass Season 1", "Hass Season 2", "Hass Season 3"],
    "Fuerte": ["Fuerte Season 1", "Fuerte Season 2", "Fuerte Season 3"],
    "Pixie": ["Pixie Season 1", "Pixie Season 2", "Pixie Season 3"]
}

# Analyze total yield per season
print("\n🍊 Total yield per fruit per season:")
for fruit, cols in seasonal_columns.items():
    totals = df[cols].sum()
    print(f"\n{fruit}:")
    print(totals)

# Identify best season per fruit
print("\n🏆 Best season per fruit:")
for fruit, cols in seasonal_columns.items():
    totals = df[cols].sum()
    best_season = totals.idxmax()
    print(f"{fruit}: Best in {best_season} with {totals.max()} fruits")

# Rank fruits by total yield
print("\n📊 Fruit ranking by total yield:")
fruit_totals = {fruit: df[cols].sum().sum() for fruit, cols in seasonal_columns.items()}
sorted_fruits = sorted(fruit_totals.items(), key=lambda x: x[1], reverse=True)
for fruit, total in sorted_fruits:
    print(f"{fruit}: {total} fruits harvested")
