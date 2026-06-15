# -*- coding: utf-8 -*-
# load data 

import numpy as np
import pandas as pd
import pickle

test_data = pd.read_excel('data/Test_set.xlsx')

with open("data/rf_random.pkl", "rb") as file:
    model = pickle.load(file)

airlines = sorted(test_data["Airline"].dropna().unique())
sources = sorted(test_data["Source"].dropna().unique())
destinations = sorted(test_data["Destination"].dropna().unique())
stops = sorted(test_data["Total_Stops"].dropna().unique())

dict_airlines = {
    key: index for index, key in enumerate(airlines, 0)
}

dict_dest = {
    key: index for index, key in enumerate(destinations, 0)
}

stop_dict = {
    "non-stop": 0,
    "1 stop": 1,
    "2 stops": 2,
    "3 stops": 3,
    "4 stops": 4
}

import streamlit as st

st.set_page_config(page_title="Flight Price Prediction", layout='wide')
st.title("✈️ Flight Price Predictor")
st.write("This app estimates flight prices using airline, route, journey date and timings.")

# input
st.subheader("Flight Details")

col1, col2, col3, col4 = st.columns(4)

with col1:
    airline = st.selectbox(
        "Airline",
        airlines
    )

with col2:
    source = st.selectbox(
        "Source",
        sources
    )

with col3:
    destination = st.selectbox(
        "Destination",
        destinations
    )

with col4:
    total_stops = st.selectbox(
        "Total Stops",
        list(stop_dict.keys())
    )

st.subheader("Journey Date")

journey_date = st.date_input(
    "Date of Journey"
)

st.subheader("Flight Timings")

col5, col6 = st.columns(2)

with col5:
    dep_time = st.time_input(
        "Departure Time"
    )

with col6:
    arr_time = st.time_input(
        "Arrival Time"
    )
    
# duration calculate

dep_minutes = dep_time.hour * 60 + dep_time.minute
arr_minutes = arr_time.hour * 60 + arr_time.minute

duration = arr_minutes - dep_minutes

if duration < 0:
    duration += 24 * 60

duration_hour = duration // 60
duration_minute = duration % 60

if st.button("Predict Price"):

    airline_encoded = dict_airlines[airline]
    destination_encoded = dict_dest[destination]
    stops_encoded = stop_dict[total_stops]

    source_banglore = 1 if source == "Banglore" else 0
    source_kolkata = 1 if source == "Kolkata" else 0
    source_delhi = 1 if source == "Delhi" else 0
    source_chennai = 1 if source == "Chennai" else 0
    source_mumbai = 1 if source == "Mumbai" else 0

    input_df = pd.DataFrame([{
    "Airline": airline_encoded,
    "Destination": destination_encoded,
    "Total_Stops": stops_encoded,
    
    "Journey_day": journey_date.day,
    "Journey_month": journey_date.month,

    "Dep_Time_hour": dep_time.hour,
    "Dep_Time_minute": dep_time.minute,

    "Arrival_Time_hour": arr_time.hour,
    "Arrival_Time_minute": arr_time.minute,
    
    "Duration_hours": duration_hour,
    "Duration_mins": duration_minute,
    "Duration_hour": duration_hour,
    "Duration_minute": duration_minute,

    "Source_Banglore": source_banglore,
    "Source_Kolkata": source_kolkata,
    "Source_Delhi": source_delhi,
    "Source_Chennai": source_chennai,
    "Source_Mumbai": source_mumbai
}])

    prediction = model.predict(input_df)[0]

    st.success(
        f"💰 Estimated Flight Price: ₹ {prediction:,.2f}"
    )

    st.balloons()