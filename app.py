import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import time

# =========================
# API KEY
# =========================
API_KEY = "a72e4993a2ea4af17fa7b2d7d89bcb98"
API_KEY = st.secrets["API_KEY"]
# =========================
# AUTO REFRESH EVERY 10 SEC
# =========================
st.set_page_config(page_title="India Weather Dashboard", layout="wide")

st.title("🌦 India State Capitals Live Weather")

st.caption("🔄 Auto updates every 10 seconds")

# =========================
# STATE CAPITALS
# =========================
cities = {
    "Delhi": [28.7041, 77.1025],
    "Mumbai": [19.0760, 72.8777],
    "Bengaluru": [12.9716, 77.5946],
    "Chennai": [13.0827, 80.2707],
    "Kolkata": [22.5726, 88.3639],
    "Hyderabad": [17.3850, 78.4867],
    "Jaipur": [26.9124, 75.7873],
    "Lucknow": [26.8467, 80.9462],
    "Bhopal": [23.2599, 77.4126],
    "Patna": [25.5941, 85.1376],
    "Raipur": [21.2514, 81.6296],
    "Ranchi": [23.3441, 85.3096],
    "Bhubaneswar": [20.2961, 85.8245],
    "Gandhinagar": [23.2156, 72.6369],
    "Dispur": [26.1445, 91.7362],
    "Shillong": [25.5788, 91.8933],
    "Imphal": [24.8170, 93.9368],
    "Aizawl": [23.7271, 92.7176],
    "Agartala": [23.8315, 91.2868],
    "Kohima": [25.6751, 94.1086],
    "Gangtok": [27.3389, 88.6065],
    "Dehradun": [30.3165, 78.0322],
    "Shimla": [31.1048, 77.1734],
    "Srinagar": [34.0837, 74.7973],
    "Panaji": [15.4909, 73.8278]
}

# =========================
# CREATE DARK MAP
# =========================
m = folium.Map(
    location=[22.5, 78.9],
    zoom_start=5,
    tiles="CartoDB dark_matter"
)

# =========================
# WEATHER LOOP
# =========================
for city, coords in cities.items():

    lat, lon = coords

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

    response = requests.get(url)

    data = response.json()

    if "main" in data:

        temp = data["main"]["temp"]
        weather = data["weather"][0]["description"]

        weather_lower = weather.lower()

        # Emojis
        if "cloud" in weather_lower:
            icon = "☁️"
        elif "rain" in weather_lower:
            icon = "🌧️"
        elif "clear" in weather_lower:
            icon = "☀️"
        elif "mist" in weather_lower:
            icon = "🌫️"
        elif "thunderstorm" in weather_lower:
            icon = "⛈️"
        else:
            icon = "🌤️"

        popup_html = f"""
        <div style="
            width:220px;
            font-size:16px;
            padding:10px;
        ">
            <h2>{icon} {city}</h2>
            <hr>
            <b>🌡 Temperature:</b> {temp}°C<br><br>
            <b>🌥 Weather:</b> {weather.title()}
        </div>
        """

        # Color based on temperature
        if temp > 35:
            color = "red"
        elif temp > 25:
            color = "orange"
        else:
            color = "lightblue"

        folium.CircleMarker(
            location=[lat, lon],
            radius=12,
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=f"{city}: {temp}°C",
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.8
        ).add_to(m)

# =========================
# SHOW MAP
# =========================
st_folium(m, width=1400, height=700)

# =========================
# AUTO REFRESH
# =========================
time.sleep(120)
st.rerun()
