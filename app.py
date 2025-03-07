import streamlit as st
import requests
import pandas as pd
import numpy as np


st.write('Welcome to the monkeyhouse')

st.markdown('''
## Come let me know
''')

pickup_datetime = st.text_input('Pickup Datetime (YYYY-MM-DD HH:MM:SS)', '2012-10-06 12:10:20')
pickup_longitude = st.number_input('Pickup Longitude', format="%0.4f")
pickup_latitude = st.number_input('Pickup Latitude', format="%0.4f")
dropoff_longitude = st.number_input('Dropoff Longitude', format="%0.4f")
dropoff_latitude = st.number_input('Dropoff Latitude', format="%0.4f")
passenger_count = st.slider('Passenger Count', 1, 8, 1)

url = 'https://taxifare.lewagon.ai/predict'

payload = {
    'pickup_datetime': pickup_datetime,
    'pickup_longitude': pickup_longitude,
    'pickup_latitude': pickup_latitude,
    'dropoff_longitude': dropoff_longitude,
    'dropoff_latitude': dropoff_latitude,
    'passenger_count': passenger_count
}

st.markdown('''
Predicator, predicatoris, m
''')

if st.button('Get Prediction'):  # Add a button to trigger the API call
    try:
        response = requests.get(url, params=payload)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        prediction = response.json().get('fare')

        st.write(f'Predicted Fare: ${prediction:.2f}')  # Display the prediction
    except requests.exceptions.RequestException as e:
        st.error(f"Error calling API: {e}")
    except ValueError:
        st.error("Invalid JSON response from API.")
    except KeyError:
        st.error("Fare not found in API response.")


# col1, col2 = st.columns(2)
# with col1:
