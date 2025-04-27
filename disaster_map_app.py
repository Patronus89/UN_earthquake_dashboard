import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster, HeatMap, Search
from streamlit_folium import st_folium

# --- Page Config ---
st.set_page_config(page_title="Myanmar Earthquake Dashboard", layout="wide")

# --- Add UN Logo and Title ---
st.image("undss-logo.png", width=100)
st.title("Myanmar Earthquake Emergency Dashboard")
st.markdown("**Date:** 28 March 2025  \n"
            "**Magnitude:** 7.7  \n"
            "**Epicenter:** Near Mandalay")

# --- Add Brief Context ---
st.markdown("""
On 28 March 2025, a massive 7.7-magnitude earthquake struck central Myanmar, resulting in widespread loss of life and destruction of infrastructure.  
Over 15 million people have been affected, including 1.6 million internally displaced persons (IDPs) who were already vulnerable due to ongoing conflicts.  

This dashboard allows responders and coordinators to **visualize the damage**, **identify urgent needs**, and **support relief operations** based on real-time information.
""")

st.markdown("---")

# --- Sidebar Upload CSV ---
uploaded_file = st.sidebar.file_uploader("Upload Disaster CSV (optional)", type=['csv'])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    # Default Example Data
    df = pd.DataFrame({
        'Location': ['Mandalay', 'Pyin Oo Lwin', 'Sagaing', 'Naypyidaw', 'Meiktila'],
        'Latitude': [21.9781, 22.0355, 21.8787, 19.7633, 20.8778],
        'Longitude': [96.0836, 96.4597, 95.9784, 96.0785, 95.8585],
        'Damage_Level': ['Severe', 'Moderate', 'Severe', 'Mild', 'Moderate'],
        'Needs': ['Medical, Shelter', 'Food, Water', 'Medical, Water', 'Temporary Shelter', 'Food, Medical'],
        'IDPs_Affected': [100000, 50000, 120000, 25000, 40000]
    })

# --- Sidebar Filters ---
st.sidebar.header("Map Filters")
damage_filter = st.sidebar.selectbox('Filter by Damage Level', ['All', 'Mild', 'Moderate', 'Severe'])
location_query = st.sidebar.text_input('Search by Location')

# --- Build Map ---
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

# Add HeatMap
heat_data = [
    [row['Latitude'], row['Longitude'], row['IDPs_Affected']] 
    for idx, row in filtered_df.iterrows()
]
HeatMap(heat_data, radius=20, blur=15, max_zoom=6).add_to(m)

# Add Search Bar
search = Search(
    layer=marker_cluster,
    search_label='Location',
    placeholder='Search for a city',
    collapsed=False
)
search.add_to(m)

# --- Display Map ---
st_folium(m, width=1100, height=700)

