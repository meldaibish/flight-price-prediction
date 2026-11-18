"""Streamlit historical flight fare demo for a fitted sklearn Pipeline."""
from datetime import date, time
import json
from pathlib import Path

import joblib
import streamlit as st

from src.flight_features import make_flight_input, predict_price

ROOT = Path(__file__).resolve().parent
MODEL_PATH = ROOT / "models" / "flight_price_model.joblib"
METADATA_PATH = ROOT / "app_metadata.json"

st.set_page_config(page_title="Flight Price Prediction", page_icon="✈️", layout="centered")
st.title("✈️ Flight Price Prediction")
st.write("Estimate a historical-style ticket fare using a Random Forest model.")
st.warning(
    "Educational demo trained on flight data from **2019**. Predictions are **not live fares** "
    "and should not be used for booking or present-day price decisions."
)

@st.cache_resource
def load_model():
    # Serialized sklearn models must come from a trusted local training source.
    return joblib.load(MODEL_PATH)

@st.cache_data
def load_metadata():
    return json.loads(METADATA_PATH.read_text(encoding="utf-8"))

if not MODEL_PATH.exists() or not METADATA_PATH.exists():
    st.error("Required trained model or metadata is missing. See README for setup.")
    st.stop()

try:
    model = load_model()
    metadata = load_metadata()
except Exception as exc:
    st.error(f"Unable to load model: {exc}")
    st.stop()

# Route selectors must stay OUTSIDE the form, so destination and airline
# options refresh immediately when the departure city changes.
source = st.selectbox("Departure city", metadata["sources"])
destinations = metadata["routes"].get(source, metadata["destinations"])
destination = st.selectbox("Destination city", destinations)
airline_options = metadata["airlines_by_route"].get(
    f"{source}|||{destination}", metadata["airlines"]
)

with st.form("predict_fare"):
    airline = st.selectbox("Airline", airline_options)
    journey_date = st.date_input(
        "Historical journey date (2019)", value=date(2019, 5, 20),
        min_value=date(2019, 3, 1), max_value=date(2019, 6, 30)
    )
    a,b = st.columns(2)
    with a:
        departure = st.time_input("Departure time", value=time(9, 0))
        stops = st.selectbox("Number of stops", [0, 1, 2, 3, 4])
    with b:
        arrival = st.time_input("Arrival time", value=time(11, 30))
        arrival_days_later = st.selectbox(
            "Arrival day", [0, 1, 2],
            format_func=lambda i: ["Same day", "Next day", "Two days later"][i]
        )
    info_options = metadata["additional_info"]
    default_info = info_options.index("No info") if "No info" in info_options else 0
    info = st.selectbox("Additional flight information", info_options, index=default_info)
    submitted = st.form_submit_button("Predict historical-style fare", type="primary")

if submitted:
    try:
        raw_flight = make_flight_input(
            airline=airline, source=source, destination=destination,
            additional_info=info, journey_date=journey_date,
            departure=departure, arrival=arrival,
            arrival_days_later=arrival_days_later, stops=stops,
        )
        pred = predict_price(model, raw_flight)
        st.metric("Estimated fare", f"₹{pred:,.0f}")
        st.caption("Indicative 2019 Indian domestic flight price. Not a quote or future forecast.")
        with st.expander("Processed input features"):
            from src.flight_features import make_features
            st.dataframe(make_features(raw_flight))
    except ValueError as exc:
        st.error(str(exc))
    except Exception as exc:
        st.error(f"Prediction could not be completed: {exc}")

st.divider()
st.caption("Portfolio demo | Python · pandas · scikit-learn · Streamlit")
