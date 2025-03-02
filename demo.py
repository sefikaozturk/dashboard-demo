import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px

# Must be the first Streamlit command
st.set_page_config(page_title="East Nashville Parks Dashboard", layout="wide")

# Enhanced Custom CSS for styling
st.markdown("""
    <style>
    .stApp {
        background-color: #E8F5E9;
        font-family: 'Arial', sans-serif;
    }
    .css-1d391kg {
        background: linear-gradient(to bottom, #4CAF50, #2E7D32);
        color: white;
        border-radius: 10px;
        padding: 10px;
    }
    .css-1d391kg .stRadio > label {
        color: white;
        font-weight: bold;
    }
    h1, h2, h3 {
        color: #4A2F1F;
        font-family: 'Georgia', serif;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
    }
    .stButton>button {
        background-color: #81C784;
        color: white;
        border: 2px solid #4CAF50;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #66BB6A;
        transform: scale(1.05);
    }
    .stMetric {
        background-color: rgba(241, 248, 233, 0.8);
        border: 1px solid #A5D6A7;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
    }
    .main .block-container {
        background-image: url('https://www.transparenttextures.com/patterns/green-leaves.png');
        background-size: 200px;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    /* Adjusted chart styling: background only for container, not SVG */
    .js-plotly-plot .plotly {
        background-color: #FFFFFF; /* White background for the chart container */
        border-radius: 15px;
        box-shadow: 0 0 10px rgba(232, 245, 233, 0.8); /* Soft green shadow for corner blending */
        padding: 10px; /* Padding to ensure content isn't cut off */
    }
    .js-plotly-plot .plotly .main-svg {
        background-color: transparent !important; /* Ensure SVG itself is transparent */
    }
    </style>
""", unsafe_allow_html=True)

# Set up multi-page app
PAGES = {
    "Volunteer Program": 1,
    "Invasive Plant Removal Data and Mapping": 2,
    "Surveys and Strategic Plan": 3
}

st.sidebar.title("🌿 Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]

# Sample volunteer data with increased numbers
volunteer_data = pd.DataFrame({
    'Volunteer': ['Alice', 'Bob', 'Charlie', 'Alice', 'Bob', 'Dana', 'Eve', 'Frank', 'Grace', 'Hank'] * 8 + ['Ian', 'Jill', 'Kate'],  # 88 entries
    'Event': (['Tree Planting', 'Litter Pickup', 'Tree Planting', 'Park Cleanup', 'Litter Pickup', 
              'Invasive Removal', 'Tree Planting', 'Park Cleanup', 'Litter Pickup', 'Trail Maintenance'] * 8) + ['Tree Planting', 'Litter Pickup', 'Park Cleanup'],
    'Date': ['2024-01-15', '2024-02-10', '2024-03-05', '2024-04-20', '2024-05-12', 
             '2024-06-01', '2024-07-10', '2024-08-15', '2024-09-20', '
