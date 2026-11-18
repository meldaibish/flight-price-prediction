from datetime import date, time
from pathlib import Path
import joblib
import pytest
from src.flight_features import make_flight_input, predict_price

MODEL = Path(__file__).resolve().parents[1] / "models" / "flight_price_model.joblib"

@pytest.mark.skipif(not MODEL.exists(), reason="Model file missing; train the notebook first")
def test_model_inference_uses_shared_features():
    model = joblib.load(MODEL)
    row = make_flight_input(
        airline="IndiGo", source="Banglore", destination="Delhi",
        additional_info="No info", journey_date=date(2019, 5, 20),
        departure=time(22, 30), arrival=time(1, 10),
        arrival_days_later=1, stops=0,
    )
    estimate = predict_price(model, row)
    assert 0 < estimate < 1_000_000
