# US Wildfire Live Map 🔥

A real-time web application that visualizes active wildfire hotspots across the United States using NASA's FIRMS (Fire Information for Resource Management System) API data.

## Features

- Live map showing active fire locations across the USA
- Color-coded markers based on Fire Radiative Power (FRP) intensity
- Automatic data refresh every minute
- Interactive popups showing detailed information for each hotspot
- Key metrics dashboard showing total fires, average and maximum FRP

## Color Legend

- 🟡 Yellow: Low intensity (FRP < 1.64 MW)
- 🟠 Orange: Medium intensity (FRP 1.64-3.77 MW)
- 🟧 Red-Orange: High intensity (FRP 3.77-11.77 MW)
- 🔴 Red: Very high intensity (FRP > 11.77 MW)

## Setup

1. Clone this repository
2. Install requirements:
   ```bash
   pip install streamlit pandas folium streamlit-folium python-dotenv
   ```
3. Get a free FIRMS API key from [here](https://firms.modaps.eosdis.nasa.gov/api/map_key).
4. Create a `.env` file in the project root and add your FIRMS API key:
   ```bash
   FIRMS_API_KEY = "your_api_key_here"
   ```  
5. Run the application:
   ```bash
   streamlit run app.py
   ```

## Data Source

This application uses NASA's FIRMS API to fetch VIIRS (Visible Infrared Imaging Radiometer Suite) data from the NOAA-21 satellite. The FIRMS Fire Map is updated approximately every 5 minutes and global coverage updated roughly every 12 hours. More information can be found [here](https://www.earthdata.nasa.gov/data/tools/firms/faq).

## Technologies Used

- Streamlit: Web application framework
- Folium: Map visualization
- Pandas: Data processing
- NASA FIRMS API: Fire data source

## Note

The fire detection points shown on the map indicate areas of high temperature detection, which may include active fires, gas flares, volcanoes, or other sources of thermal anomalies. Always verify with local authorities for confirmed fire incidents.
