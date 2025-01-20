import os
import time
import pandas as pd
import streamlit as st
import folium
# pip install streamlit-folium
from streamlit_folium import st_folium
from dotenv import load_dotenv

# Load environment variables and setup
load_dotenv()
API_KEY = os.getenv('FIRMS_API_KEY')
FIRMS_URL = f"https://firms.modaps.eosdis.nasa.gov/api/country/csv/{API_KEY}/VIIRS_NOAA21_NRT/USA/2"

# Page config
st.set_page_config(
    page_title="US Wildfire Live Map",
    page_icon="🔥",
    layout="wide"
)

def get_color(frp):
    """Returns a color based on the Fire Radiative Power (FRP) value"""
    if frp < 1.64:
        return '#ffff00'  # Yellow
    elif frp < 3.77:
        return '#ffa500'  # Orange
    elif frp < 11.77:
        return '#ff4500'  # Red-Orange
    else:
        return '#ff0000'  # Red

def fetch_and_process_fire_data():
    """Fetch and process fire data from the FIRMS API"""
    try:
        df = pd.read_csv(FIRMS_URL)
        df_subset = df[['latitude', 'longitude', 'bright_ti4', 'acq_date', 'acq_time', 'confidence', 'frp']]
        
        # Filter out low confidence data
        filtered_df = df_subset[df_subset['confidence'] != 'l'].copy()
        
        # Filter out rows with NaN values in critical columns
        filtered_df = filtered_df.dropna(subset=['latitude', 'longitude', 'frp'])

        # Add color column based on FRP
        filtered_df.loc[:, 'color'] = filtered_df['frp'].apply(get_color)
        
        return filtered_df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

def create_map(data):
    """Create a folium map with wildfire data"""
    # Create a map centered around the USA
    m = folium.Map(location=[37.0902, -95.7129], zoom_start=4)
    
    # Add markers for each fire
    for _, row in data.iterrows():
        iframe = folium.IFrame(f"""
            <b>FRP:</b> {row['frp']:.2f}<br>
            <b>Date:</b> {row['acq_date']}<br>
            <b>Time:</b> {row['acq_time']}
        """)
        popup = folium.Popup(iframe, min_width=200, max_width=200, min_height=100)
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=8,
            color=row['color'],
            fill=True,
            fillColor=row['color'],
            fillOpacity=0.7,
            popup=popup
        ).add_to(m)
    
    return m

def main():
    # Initialize session state for data caching
    if 'last_fetch_time' not in st.session_state:
        st.session_state.last_fetch_time = time.time()
    if 'fire_data' not in st.session_state:
        with st.spinner("Fetching data..."):
            st.session_state.fire_data = fetch_and_process_fire_data()

    # Title and description
    st.title("🔥 US Wildfire Live Map")
    st.markdown("""
    This map shows active wildfire hotspots in the United States using data from NASA's FIRMS API.
    The map updates automatically every minute. The color is based on the fire radiative power (FRP),
    measured in megawatts (MW) per pixel.
    
    **Color Legend:**
    - 🟡 Yellow: Low intensity (FRP < 1.64)
    - 🟠 Orange: Medium intensity (FRP 1.64-3.77)
    - 🟧 Red-Orange: High intensity (FRP 3.77-11.77)
    - 🔴 Red: Very high intensity (FRP > 11.77)
    """)   

    with st.container():
        col1, col2, col3 = st.columns(3, border=True)
        with col1:
            st.metric("Total Active Fires/Hotspots", len(st.session_state.fire_data))
        with col2:
            st.metric("Average FRP", f"{st.session_state.fire_data['frp'].mean():.2f}")
        with col3:
            st.metric("Max FRP", f"{st.session_state.fire_data['frp'].max():.2f}")

        m = create_map(st.session_state.fire_data)
        st_data = st_folium(m, width="100%", height=600, key="fire_map")
    
    st.write(f"Time since last data refresh: {time.time() - st.session_state.last_fetch_time:.1f} seconds")
    if time.time() - st.session_state.last_fetch_time >= 60:
        st.toast("Refreshing data...")
        st.session_state.fire_data = fetch_and_process_fire_data()
        st.session_state.last_fetch_time = time.time()
        

if __name__ == "__main__":
    main()