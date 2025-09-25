import streamlit as st
import pandas as pd
import pydeck as pdk
import altair as alt

# Load cleaned data
df = pd.read_csv("data/farmer_data_cleaned.csv")

st.set_page_config(page_title="Farmer Dashboard", layout="wide")
st.title("🌿 Makueni Farmer Dashboard")
st.markdown("""
<div style='background-color:#e0f7fa; padding:15px; border-radius:10px'>
    <h3 style='color:#00796b'>Welcome, steward of data 🌱</h3>
    <p>This dashboard is built to honor farmers, guide decisions, and uplift communities with clarity and dignity.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("Built by Austine Otieno — stewarding data for impact.")


# Sidebar filters
locations = st.sidebar.multiselect("📍 Filter by Location", options=df["Location"].unique())
methods = st.sidebar.multiselect("🌱 Filter by Farming Method", options=df["Farming Method"].unique())

# Apply filters
filtered_df = df.copy()
if locations:
    filtered_df = filtered_df[filtered_df["Location"].isin(locations)]
if methods:
    filtered_df = filtered_df[filtered_df["Farming Method"].isin(methods)]

# Show available columns for debugging
st.write("🧾 Available Columns:", filtered_df.columns.tolist())

# 🧩 Build dynamic blue borders around selected locations
polygon_data = []
for loc in locations:
    loc_df = df[df["Location"] == loc]
    if not loc_df.empty:
        lat = loc_df["Latitude"].mean()
        lon = loc_df["Longitude"].mean()
        box = [
            [lon - 0.01, lat + 0.01],
            [lon + 0.01, lat + 0.01],
            [lon + 0.01, lat - 0.01],
            [lon - 0.01, lat - 0.01],
            [lon - 0.01, lat + 0.01]
        ]
        polygon_data.append({"coordinates": [box]})

# 🎨 Create polygon layer
polygon_layer = pdk.Layer(
    "PolygonLayer",
    data=polygon_data,
    get_polygon="coordinates",
    get_fill_color=[0, 0, 255, 40],
    get_line_color=[0, 0, 255, 200],
    line_width_min_pixels=2,
    pickable=True,
    stroked=True,
    filled=True,
)

# 🗺️ Map view
st.subheader("🗺️ Farmer Locations")
st.pydeck_chart(pdk.Deck(
    initial_view_state=pdk.ViewState(
        latitude=filtered_df["Latitude"].mean(),
        longitude=filtered_df["Longitude"].mean(),
        zoom=8,
        pitch=0,
    ),
    layers=[
        polygon_layer,
        pdk.Layer(
            "ScatterplotLayer",
            data=filtered_df,
            get_position=["Longitude", "Latitude"],
            get_radius=100,
            get_color=[0, 128, 0],
            pickable=True,
        )
    ],
))

# 📊 Seasonal summary
st.subheader("📊 Seasonal Yield Summary")
season_cols = [col for col in df.columns if "Season" in col]
st.dataframe(filtered_df[season_cols].sum().sort_values(ascending=False).rename("Total Fruits"))

# 📈 Seasonal Yield Trends
season_cols = [col for col in filtered_df.columns if "Season" in col]
season_df = filtered_df[season_cols].sum().reset_index()
season_df.columns = ["Season", "Total Yield"]

chart = alt.Chart(season_df).mark_line(point=True).encode(
    x="Season",
    y="Total Yield",
    tooltip=["Season", "Total Yield"]
).properties(
    title="📈 Seasonal Yield Trends",
    width=700,
    height=400
)

st.subheader("📈 Seasonal Yield Trends")
st.altair_chart(chart, use_container_width=True)

# 🍍 Produce Insights Chart
fruit_totals = {
    "Mango": filtered_df[[c for c in season_cols if "Mango" in c]].sum().sum(),
    "Hass": filtered_df[[c for c in season_cols if "Hass" in c]].sum().sum(),
    "Fuerte": filtered_df[[c for c in season_cols if "Fuerte" in c]].sum().sum(),
    "Pixie": filtered_df[[c for c in season_cols if "Pixie" in c]].sum().sum(),
}

fruit_df = pd.DataFrame(list(fruit_totals.items()), columns=["Fruit", "Total Yield"])

chart = alt.Chart(fruit_df).mark_bar().encode(
    x=alt.X("Fruit", sort="-y"),
    y="Total Yield",
    tooltip=["Fruit", "Total Yield"],
    color=alt.Color("Fruit", legend=None)
).properties(
    title="🍍 Top Performing Fruits",
    width=600,
    height=400
)

st.subheader("🍍 Top Performing Fruits")
st.altair_chart(chart, use_container_width=True)

# 🍓 Fruit Drill-Down
selected_fruit = st.selectbox("🍓 Select a fruit to explore", options=["Mango", "Hass", "Fuerte", "Pixie"])
fruit_cols = [col for col in season_cols if selected_fruit in col]

if not fruit_cols:
    st.warning(f"⚠️ No seasonal columns found for {selected_fruit}. Please check your data.")
else:
    fruit_yield_df = filtered_df[["Farmer Name", "Location"] + fruit_cols].copy()
    fruit_yield_df["Total Yield"] = fruit_yield_df[fruit_cols].sum(axis=1)

    st.subheader(f"🧑‍🌾 {selected_fruit} Yield by Farmer")
    st.dataframe(fruit_yield_df[["Farmer Name", "Location", "Total Yield"]].sort_values(by="Total Yield", ascending=False))

# 👤 Farmer Profiles
profile_cols = ["Farmer Name", "Location", "Farming Method", "Irrigation Method"]
profile_df = filtered_df[profile_cols].drop_duplicates()

profile_df = profile_df.rename(columns={
    "Irrigation Method": "Irrigation Type"
})

# 👤 Farmer Profiles
# 🔍 Filter Summary Banner
selected_locations = ", ".join(locations) if locations else "All Locations"
selected_methods = ", ".join(methods) if methods else "All Methods"

st.markdown(f"**🔍 Showing farmers in `{selected_locations}` using `{selected_methods}` methods**")

st.markdown("### 👤 Farmer Profiles")

# Define background colors for farming methods
method_color = {
    "Organic": "#e8f5e9",        # Light green
    "Conventional": "#fce4ec"    # Soft pink
}

# Prepare profile data
profile_cols = ["Farmer Name", "Location", "Farming Method", "Irrigation Method"]
profile_df = filtered_df[profile_cols].drop_duplicates()
profile_df = profile_df.rename(columns={"Irrigation Method": "Irrigation Type"})

# Create 5-column layout
cols = st.columns(5)

# Display each farmer in a styled card
for i, (_, row) in enumerate(profile_df.iterrows()):
    bg_color = method_color.get(row["Farming Method"].split()[-1], "#f9f9f9")  # Default to light grey

    with cols[i % 5]:
        st.markdown(f"""
        <div style='border:1px solid #ccc; padding:10px; border-radius:8px; background:{bg_color}; margin-bottom:10px'>
            <strong>👤 {row['Farmer Name']}</strong><br>
            📍 Location: {row['Location']}<br>
            🌱 Farming Method: {row['Farming Method']}<br>
            💧 Irrigation Type: {row['Irrigation Type']}
        </div>
        """, unsafe_allow_html=True)




# 🏆 Fruit Ranking
st.subheader("🏆 Fruit Ranking")
ranked = pd.Series(fruit_totals).sort_values(ascending=False)
st.bar_chart(ranked)
