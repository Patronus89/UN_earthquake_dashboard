import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster, HeatMap, Search
from streamlit_folium import st_folium

# --- Page Config ---
st.set_page_config(page_title="Myanmar Earthquake Dashboard", layout="wide")

# --- Add UN Logo and Title ---
st.image("undss-logo.jpg", width=100)
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
    df = pd
