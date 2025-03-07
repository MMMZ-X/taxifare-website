import streamlit as st
import requests
import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim


st.write('Welcome to the monkeyhouse.....')

st.markdown('''
## Come let me know
''')

col1, col2 = st.columns(2)

with col1:
    pickup_datetime = st.text_input('When do you want to be picked up? (YYYY-MM-DD HH:MM:SS)', '2012-10-06 12:10:20')

    geolocator = Nominatim(user_agent="taxifare-app")

    def geocode_address(address):
        try:
            location = geolocator.geocode(address)
            if location:
                return location.latitude, location.longitude
            else:
                st.error("Address not found.")
                return None, None
        except Exception as e:
            st.error(f"Geocoding error: {e}")
            return None, None

    def create_map(pickup_lat, pickup_lon, dropoff_lat, dropoff_lon):
        if pickup_lat is not None and pickup_lon is not None and dropoff_lat is not None and dropoff_lon is not None:
            m = folium.Map(location=[(pickup_lat + dropoff_lat) / 2, (pickup_lon + dropoff_lon) / 2], zoom_start=12)
            folium.Marker([pickup_lat, pickup_lon], popup='Pickup').add_to(m)
            folium.Marker([dropoff_lat, dropoff_lon], popup='Dropoff').add_to(m)
            folium_static(m)
        else:
            st.write("Enter both pickup and dropoff locations to display the map.")

    st.subheader("Pick me up here")
    pickup_address = st.text_input("Enter Pickup Address")
    pickup_lat, pickup_lon = geocode_address(pickup_address)

    st.subheader("Drop me off there")
    dropoff_address = st.text_input("Enter Dropoff Address")
    dropoff_lat, dropoff_lon = geocode_address(dropoff_address)

    create_map(pickup_lat, pickup_lon, dropoff_lat, dropoff_lon)
with col2:

    st.image("Taxi.jpg", caption="My Image", use_column_width=True)

    passenger_count = st.slider('Passenger Count', 1, 8, 1)

    url = 'https://taxifare.lewagon.ai/predict'

    payload = {
        'pickup_datetime': pickup_datetime,
        'pickup_longitude': pickup_lon,
        'pickup_latitude': pickup_lat,
        'dropoff_longitude': dropoff_lon,
        'dropoff_latitude': dropoff_lat,
        'passenger_count': passenger_count
    }

    st.markdown('''
    Predicator, predicatoris, m
    ''')

    if st.button('Get Prediction'):
        if pickup_lat is not None and pickup_lon is not None and dropoff_lat is not None and dropoff_lon is not None:
            try:
                response = requests.get(url, params=payload)
                response.raise_for_status()
                prediction = response.json().get('fare')
                st.write(f'Predicted Fare: ${prediction:.2f}')
            except requests.exceptions.RequestException as e:
                st.error(f"Error calling API: {e}")
            except ValueError:
                st.error("Invalid JSON response from API.")
            except KeyError:
                st.error("Fare not found in API response.")
        else:
            st.error("Please enter valid pickup and dropoff addresses.")
