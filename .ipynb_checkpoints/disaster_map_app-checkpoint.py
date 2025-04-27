import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster, HeatMap
from streamlit_folium import st_folium

# --- Title ---
st.title("Myanmar Earthquake Relief Dashboard")

# --- Sidebar Upload ---
uploaded_file = st.sidebar.file_uploader("Upload Disaster CSV", type=['csv'])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    # Default Data
    df = pd.DataFrame({
        'Location': ['Mandalay', 'Pyin Oo Lwin', 'Sagaing', 'Naypyidaw', 'Meiktila'],
        'Latitude': [21.9781, 22.0355, 21.8787, 19.7633, 20.8778],
        'Longitude': [96.0836, 96.4597, 95.9784, 96.0785, 95.8585],
        'Damage_Level': ['Severe', 'Moderate', 'Severe', 'Mild', 'Moderate'],
        'Needs': ['Medical, Shelter', 'Food, Water', 'Medical, Water', 'Temporary Shelter', 'Food, Medical'],
        'IDPs_Affected': [100000, 50000, 120000, 25000, 40000]
    })

# --- Filters ---
damage_filter = st.sidebar.selectbox('Filter by Damage Level', ['All', 'Mild', 'Moderate', 'Severe'])
location_query = st.sidebar.text_input('Search by Location')

# --- Map Building ---
m = folium.Map(location=[21.5, 96.0], zoom_start=6)
marker_cluster = MarkerCluster().add_to(m)

filtered_df = df.copy()

if damage_filter != 'All':
    filtered_df = filtered_df[filtered_df['Damage_Level'] == damage_filter]

if location_query:
    filtered_df = filtered_df[filtered_df['Location'].str.contains(location_query, case=False)]

color_dict = {'Severe': 'red', 'Moderate': 'orange', 'Mild': 'green'}

for idx, row in filtered_df.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=(f"<b>Location:</b> {row['Location']}<br>"
               f"<b>Damage:</b> {row['Damage_Level']}<br>"
               f"<b>Needs:</b> {row['Needs']}<br>"
               f"<b>IDPs Affected:</b> {row['IDPs_Affected']:,}"),
        icon=folium.Icon(color=color_dict.get(row['Damage_Level'], 'blue'))
    ).add_to(marker_cluster)

# Add Heatmap
heat_data = [
    [row['Latitude'], row['Longitude'], row['IDPs_Affected']] 
    for idx, row in filtered_df.iterrows()
]
HeatMap(heat_data, radius=20, blur=15, max_zoom=6).add_to(m)

# --- Streamlit Folium display ---
st_data = st_folium(m, width=1000, height=700)

# --- Download Map as HTML ---
st.download_button('Download Current Map as HTML', data=m._repr_html_(), file_name='myanmar_earthquake_map.html', mime='text/html')
