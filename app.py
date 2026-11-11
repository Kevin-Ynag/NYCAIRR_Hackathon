import streamlit as st # Website and user interface
import folium # Creates interactive map
from streamlit_folium import st_folium # Places the map inside the website
import requests # Retreives data from API

# Configure the apge
st.set_page_config(
    page_title = "ClearPath",
    page_icon = "🚶",
    layout = "wide"
)

# NYC DDC construction projects API
DDC_API_URL_ = "https://services.arcgis.com/v09SvJE7IY8GgvSx/ArcGIS/rest/services/DDC_Construction_Projects/FeatureServer/0/query"

# Retrieve construction project data from the NYC DDC API
@st.cache_data(ttl = 3600) # Tells streamlit to save the API response temporarily to improve load speed of the map.
def get_construction_data():
    print("Downloading construction data from NYC DDC...")
    params = {
        "where" : "1=1",
        "outFields": "ProjectID,Description,phase,division,client_agency,ProjectedConstrCompl",
        "returnGeometry": "true",
        "outSR": "4326",
        "f": "json"
    }
    response = requests.get(DDC_API_URL_, params = params)
    response.raise_for_status()
    return response.json()

# Convert coordinates from API[longitude, latitude] into Folium[latitude, longitude] format
def convert_coordinates(paths):
    folium_lines = []
    for path in paths:
        folium_line = []
        for array in path:
            folium_line.append([array[1], array[0]])
        folium_lines.append(folium_line)
    return folium_lines

# Retrieve construction data
construction_data = get_construction_data()

st.write("DDC API connection successful!")

# Homepage
st.title("ClearPath")
st.subheader("A clearer path throught NYC")

st.write(
    "Find walking routes that help you avoid construction-related "
    "noise and dust."
)

# Create map of NYC
nyc_map = folium.Map(
    location = [40.7128, -74.0060], # latitude(N) & longitude(W) of NYC
    zoom_start = 12
)

# Construction sites from DDC data
for record in construction_data["features"]:
    # Extract informations
    project_info = record["attributes"]
    geometry = record["geometry"]
    if not geometry or "paths" not in geometry:
        continue
    construction_lines = convert_coordinates(geometry["paths"])

    # Draw construction lines
    for line in construction_lines:
        if len(line) == 0:
            continue
        folium.PolyLine(
            locations = line,
            color = "red",
            weight = 5,
            tooltip = f"{project_info['Description']} - {project_info['phase']}",
            popup = f"Project ID: {project_info['ProjectID']}<br>"
                    f"Project: {project_info['Description']}<br>"
                    f"Phase: {project_info['phase']}"
        ).add_to(nyc_map)

        #Calculate midpoint for marker and creating it
        # middle_index = len(line) // 2
        # midpoint = line[middle_index]
        # folium.Marker(
        #     location = midpoint,
        #     tooltip = "Construction project midpoint",
        #     popup = f"Project: {project_info['Description']}",
        #     icon = folium.Icon(
        #         color = "red",
        #         icon = "wrench",
        #         prefix = "fa"   
        #     )
        # ).add_to(nyc_map)

# Display the map in steamlit
st_folium(nyc_map, use_container_width = True, height = 700)
st_folium(nyc_map, width = True, height = 700)