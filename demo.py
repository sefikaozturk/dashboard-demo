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
             '2024-06-01', '2024-07-10', '2024-08-15', '2024-09-20', '2024-10-05'] * 8 + ['2024-11-01', '2024-11-15', '2024-12-01'],
    'Satisfaction': [8, 7, 9, 6, 8, 9, 7, 8, 6, 9] * 8 + [7, 8, 9]
})

# Page 1: Volunteer Program
if page == 1:
    st.title("🌳 Volunteer Program Dashboard")
    
    option = st.selectbox("Choose view:", ["Overall Cumulative Data", "Individual Volunteer History", "Event-Specific Stats"])
    
    if option == "Overall Cumulative Data":
        st.subheader("🌱 Cumulative Volunteer Statistics")
        
        total_volunteers = 75  # Hardcoded as requested
        total_attended = len(volunteer_data)
        event_counts = volunteer_data['Event'].value_counts()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Volunteers Signed Up", total_volunteers)
            st.metric("Total Attendance", total_attended)
        with col2:
            fig = px.bar(event_counts, x=event_counts.index, y=event_counts.values, 
                         title="Events by Attendance", labels={'y': 'Number of Volunteers'},
                         color_discrete_sequence=['#4CAF50'])
            st.plotly_chart(fig)
            
    elif option == "Individual Volunteer History":
        st.subheader("🍃 Individual Volunteer History")
        
        volunteer = st.selectbox("Select Volunteer", set(volunteer_data['Volunteer']))
        vol_data = volunteer_data[volunteer_data['Volunteer'] == volunteer]
        
        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(vol_data, x='Event', y='Satisfaction', 
                         title=f"{volunteer}'s Event History and Satisfaction",
                         color_discrete_sequence=['#8BC34A'])
            st.plotly_chart(fig)
        with col2:
            st.write("Events Attended:")
            st.dataframe(vol_data[['Event', 'Date', 'Satisfaction']])
    
    elif option == "Event-Specific Stats":
        st.subheader("🌿 Event-Specific Statistics")
        
        event = st.selectbox("Select Event", sorted(set(volunteer_data['Event'])))
        event_data = volunteer_data[volunteer_data['Event'] == event]
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Attendance for Event", len(event_data))
            st.metric("Average Satisfaction", round(event_data['Satisfaction'].mean(), 1))
        with col2:
            fig = px.histogram(event_data, x='Satisfaction', title=f"Satisfaction Distribution for {event}",
                               color_discrete_sequence=['#66BB6A'], nbins=10)
            st.plotly_chart(fig)

# Page 2: Invasive Plant Removal Data and Mapping
elif page == 2:
    st.title("🌲 Invasive Plant Removal Data and Mapping")
    
    # Simplified data input
    st.subheader("🌿 Submit New Removal Event")
    with st.form(key='removal_form'):
        event_name = st.text_input("Event Name")
        acres_cleaned = st.number_input("Acres Cleaned", min_value=0.0, step=0.1)
        event_date = st.date_input("Event Date")
        submit_button = st.form_submit_button(label='Submit')
        
        if submit_button and event_name:
            st.success(f"Submitted: {event_name} - {acres_cleaned} acres cleaned on {event_date}")
    
    # Sample data for demo
    removal_data = pd.DataFrame({
        'lat': [36.1667, 36.1670, 36.1665],  
        'lon': [-86.7383, -86.7378, -86.7388],
        'acres': [5.0, 3.0, 7.0],
        'events': [1, 1, 1],
        'attendees': [10, 8, 15]
    })
    
    st.subheader("🍂 Removal Statistics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Acres Cleaned", removal_data['acres'].sum())
        st.metric("Number of Events", removal_data['events'].sum())
    with col2:
        st.metric("Total Attendees", removal_data['attendees'].sum())
    
    # Map with lines
    st.subheader("🌍 Map of Removal Events in Shelby Park")
    line_data = []
    for _, row in removal_data.iterrows():
        line_data.append({
            'start': [row['lon'], row['lat']],
            'end': [row['lon'] + row['acres'] * 0.001, row['lat']]
        })
    
    st.pydeck_chart(pdk.Deck(
        initial_view_state=pdk.ViewState(latitude=36.1667, longitude=-86.7383, zoom=14, pitch=50),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=removal_data,
                get_position='[lon, lat]',
                get_color='[139, 195, 74, 160]',
                get_radius=200,
            ),
            pdk.Layer(
                'LineLayer',
                data=pd.DataFrame([{'start': d['start'], 'end': d['end']} for d in line_data]),
                get_source_position='start',
                get_target_position='end',
                get_color='[76, 175, 80, 160]',
                get_width=5,
            )
        ]
    ))

# Page 3: Surveys and Strategic Plan
elif page == 3:
    st.title("🌴 Surveys and Strategic Plan Dashboard")
    
    survey_options = ["Support for Bike Lanes", "Support for More Trees", "Support for Park Expansion"]
    survey_data = {
        "Support for Bike Lanes": np.random.randint(0, 11, 100),
        "Support for More Trees": np.random.randint(0, 11, 100),
        "Support for Park Expansion": np.random.randint(0, 11, 100)
    }
    
    st.subheader("🌾 Survey Results")
    survey_choice = st.selectbox("Select Survey", survey_options)
    survey_results = pd.Series(survey_data[survey_choice]).value_counts().sort_index()
    
    fig = px.pie(
        names=survey_results.index,
        values=survey_results.values,
        title=f"Results: {survey_choice} (0-10 Scale)",
        color_discrete_sequence=px.colors.sequential.Greens
    )
    st.plotly_chart(fig)
    
    st.write("Raw Data Distribution:")
    st.bar_chart(survey_results, color="#A5D6A7")
