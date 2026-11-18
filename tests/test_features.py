from datetime import date, time
import pandas as pd
import pytest
from src.flight_features import make_features, make_flight_input


def example_raw():
    return make_flight_input(
        airline="IndiGo", source="Banglore", destination="Delhi",
        additional_info="No info", journey_date=date(2019, 5, 20),
        departure=time(22, 30), arrival=time(1, 10),
        arrival_days_later=1, stops=0,
    )


def test_overnight_duration():
    features = make_features(example_raw())
    assert features.loc[0, "duration_minutes"] == 160
    assert features.loc[0, "total_stops"] == 0
    assert features.loc[0, "journey_month"] == 5
    assert features.loc[0, "departure_hour"] == 22
    assert features.loc[0, "arrival_hour"] == 1


def test_new_delhi_alias():
    raw = example_raw()
    raw["Destination"] = "New Delhi"
    assert make_features(raw).loc[0, "Destination"] == "Delhi"


def test_invalid_arrival_order():
    with pytest.raises(ValueError):
        make_flight_input(
            airline="IndiGo", source="Banglore", destination="Delhi",
            additional_info="No info", journey_date=date(2019, 5, 20),
            departure=time(22, 30), arrival=time(1, 10),
            arrival_days_later=0, stops=0,
        )


def test_no_target_leakage_columns():
    raw = example_raw()
    raw["Price"] = [999999]
    assert "Price" not in make_features(raw).columns
