import streamlit as st # Website and user interface
import folium # Creates interactive map
from streamlit_folium import st_folium # Places the map inside the website

# Configure the apge
st.set_page_config(
    page_title = "ClearPath",
    page_icon = "",
    layout = "wide"
)

# Homepage
st.title("ClearPath")
st.subheader("A clearer path throught NYC")

st.write(
    "Find walking routes that help you avoid construction-related "
    "noise and dust."
)

# Create map of NYC
nyc_map = folium.Map(
    location = [40.7128, -74.0060],
    zoom_start = 12
)

# Fake construction sites
folium.Marker(
    location = [40.7484, -73.9857],
    popup = "Fake construction site 1",
    tooltip = "Click for construction details",
    icon = folium.Icon(color = "red", icon = "wrench", prefix = "fa")
).add_to(nyc_map)

folium.Marker(
    location = [40.7580, -73.9855],
    popup = "Fake construction site 2",
    tooltip = "Click for construction details",
    icon = folium.Icon(color = "red", icon = "wrench", prefix = "fa")
).add_to(nyc_map)

# Display the map in steamlit
st_folium(nyc_map, width = True, height = 700)