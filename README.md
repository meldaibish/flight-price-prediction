# Flight Price Prediction ✈️

An end-to-end **machine learning portfolio project** predicting historical Indian domestic flight fares, based on airline, departure and arrival cities, journey date, time, duration and stops. Built with **Python, pandas, scikit-learn and Streamlit**.

> **Scope:** The underlying data covers 2019 flight listings. This is an educational demonstration, **not** a current booking tool or a promise of future ticket prices.

## Results

| Model evaluation on held-out 25% test set | Score |
| --- | ---: |
| **R²** | **0.8853** |
| **MAE** | **₹664.47** |
| **RMSE** | **₹1,530.60** |
| **MAPE** | **7.60%** |

Train/test split: 8,012 / 2,671 examples (seed 42). Model selected using training-only three-fold cross-validation. See [MODEL_REPORT.md](MODEL_REPORT.md) for details. An additional non-overlapping-input test check is documented there. Results reflect an in-distribution random split of the 2019 data, not prospective accuracy.

## How it works

1. Split the data *before* learning preprocessing statistics (avoiding target leakage).
2. Convert original date, departure/arrival time, stop count, and duration strings to numerical features.
3. Use scikit-learn `Pipeline` and `ColumnTransformer` for cross-validated imputation, scaling, and one-hot encoding.
4. Compare baseline, Ridge Regression and Random Forest; tune Random Forest with `RandomizedSearchCV` on training folds only.
5. Evaluate once on untouched test data using MAE, RMSE, R² and MAPE.
6. Save the entire fitted preprocessing/model pipeline as a `.joblib` file.
7. Offer inference via an interactive Streamlit app using the **same** deterministic feature function (`src/flight_features.py`).

## Repository

```text
flight-price-prediction/
├── flight_app.py                      # Streamlit UI
├── app_metadata.json                 # Historical routes and category options
├── src/
│   ├── __init__.py
│   └── flight_features.py            # Shared training/prediction feature logic
├── notebooks/
│   └── flight_prediction_improved.ipynb
├── models/
│   └── flight_price_model.joblib     # Trained scikit-learn pipeline
├── data/
│   └── .gitkeep                      # Dataset excluded
├── tests/
│   ├── test_features.py
│   └── test_model.py
├── MODEL_REPORT.md
├── evaluation_results.json
├── UPDATE_GITHUB.md
├── requirements.txt
├── requirements-dev.txt
└── .gitignore
```

## Run the Streamlit demo

Requires Python 3.11+; model artifact is produced with scikit-learn **1.8.0**.

```bash
python -m pip install -r requirements.txt
streamlit run flight_app.py
```

Select departure city and destination, airline, historical date, departure and arrival times, stops and flight details. The app displays an estimated **2019-style** fare in INR. Choices are restricted to routes/airlines observed in the original dataset where possible, but it is still possible to provide unusual combinations of inputs. The app is not connected to booking services.

## Reproduce training (data is not included)

1. Obtain the original `Data_Train.xlsx` dataset from an authorized source and place it at `data/Data_Train.xlsx`.
2. Install dependencies above, then open `notebooks/flight_prediction_improved.ipynb`.
3. Run all notebook cells in order. The notebook uses shared `make_features` from `src/flight_features.py` and saves the pipeline in `models/flight_price_model.joblib`.
4. Run tests: `python -m pip install -r requirements-dev.txt && python -m pytest tests -q`.

**Dataset provenance/licensing:** This repository does not redistribute the original Excel dataset. Add the dataset source and license once verified. Historical category names may include airlines that no longer operate.

## Interpretation and limitations

- Random splitting can overestimate performance for repeated or temporally related flights; see robustness check in the model report.
- The original dataset lacks booking lead time and real-time supply/demand factors; it cannot reliably forecast current fares.
- Large-price errors still occur; RMSE is higher than MAE.
- Feature preprocessing and inference inputs are centralized to avoid training-serving mismatch.
- `.joblib` uses Python pickle serialization. **Do not load model files from untrusted repositories.**

## Future improvements

Chronological validation, live authorized pricing data, automated checks for infeasible travel durations, a light API, and improved error analysis by route and fare tier.
