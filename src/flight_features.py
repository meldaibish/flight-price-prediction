"""Stateless feature engineering shared by notebook and Streamlit app.

Only row-level operations: no fitted statistics and no access to the target Price.
"""
from __future__ import annotations

from datetime import date, time
import pandas as pd

CATEGORICAL = ["Airline", "Source", "Destination", "Additional_Info"]
NUMERIC = [
    "journey_day", "journey_month", "journey_weekday",
    "departure_hour", "departure_minute", "arrival_hour", "arrival_minute",
    "duration_minutes", "total_stops",
]


def make_features(df: pd.DataFrame) -> pd.DataFrame:
    """Convert original raw flight rows to columns expected by the fitted model."""
    required = CATEGORICAL + ["Date_of_Journey", "Dep_Time", "Arrival_Time", "Duration", "Total_Stops"]
    missing = sorted(set(required).difference(df.columns))
    if missing:
        raise ValueError(f"Missing required flight columns: {missing}")
    out = pd.DataFrame(index=df.index)
    for col in CATEGORICAL:
        out[col] = df[col].astype("string").str.strip().astype(object)
    out["Destination"] = out["Destination"].replace({"New Delhi": "Delhi"})

    journey = pd.to_datetime(
        df["Date_of_Journey"].astype("string"), format="%d/%m/%Y", errors="coerce"
    )
    out["journey_day"] = journey.dt.day
    out["journey_month"] = journey.dt.month
    out["journey_weekday"] = journey.dt.weekday

    for source, prefix in [("Dep_Time", "departure"), ("Arrival_Time", "arrival")]:
        clock = df[source].astype("string").str.extract(r"^(\d{1,2}:\d{2})", expand=False)
        parsed = pd.to_datetime(clock, format="%H:%M", errors="coerce")
        out[f"{prefix}_hour"] = parsed.dt.hour
        out[f"{prefix}_minute"] = parsed.dt.minute

    duration_text = df["Duration"].astype("string")
    hours = pd.to_numeric(duration_text.str.extract(r"(\d+)\s*h", expand=False), errors="coerce")
    mins = pd.to_numeric(duration_text.str.extract(r"(\d+)\s*m", expand=False), errors="coerce")
    out["duration_minutes"] = (hours.fillna(0) * 60 + mins.fillna(0)).mask(
        hours.isna() & mins.isna()
    )

    stops_text = df["Total_Stops"].astype("string").str.lower().str.strip()
    out["total_stops"] = pd.to_numeric(
        stops_text.str.extract(r"(\d+)", expand=False), errors="coerce"
    ).mask(stops_text.fillna("").eq("non-stop"), 0)
    return out[CATEGORICAL + NUMERIC]


def make_flight_input(*, airline: str, source: str, destination: str,
                      additional_info: str, journey_date: date,
                      departure: time, arrival: time,
                      arrival_days_later: int, stops: int) -> pd.DataFrame:
    """Prepare one plausible raw row from the web form, for make_features()."""
    if source == destination:
        raise ValueError("Departure and destination cities must be different.")
    if arrival_days_later not in (0, 1, 2):
        raise ValueError("Arrival day offset must be 0, 1, or 2.")
    if stops not in (0, 1, 2, 3, 4):
        raise ValueError("Stops must be between 0 and 4.")
    departure_min = departure.hour * 60 + departure.minute
    arrival_min = arrival.hour * 60 + arrival.minute
    duration_min = arrival_min - departure_min + arrival_days_later * 1440
    if duration_min <= 0:
        raise ValueError("Arrival must occur after departure. Select next day if necessary.")
    duration_text = f"{duration_min // 60}h {duration_min % 60}m"
    return pd.DataFrame([{
        "Airline": airline,
        "Source": source,
        "Destination": destination,
        "Additional_Info": additional_info,
        "Date_of_Journey": journey_date.strftime("%d/%m/%Y"),
        "Dep_Time": departure.strftime("%H:%M"),
        "Arrival_Time": arrival.strftime("%H:%M"),
        "Duration": duration_text,
        "Total_Stops": "non-stop" if stops == 0 else f"{stops} {'stop' if stops == 1 else 'stops'}",
    }])


def predict_price(model, raw_flight: pd.DataFrame) -> float:
    """Predict one fare using exactly the notebook feature engineering."""
    predictions = model.predict(make_features(raw_flight))
    return float(predictions[0])
