# flight-price-prediction
Flight price prediction using Machine Learning and Streamlit for UI
## Project Overview

This project predicts airline ticket prices using Machine Learning. The model estimates the expected flight price based on airline, route, travel date, departure and arrival times, and number of stops.

The project includes both model development and a Streamlit web application for real-time predictions.

---

## Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Streamlit
- Matplotlib
- Seaborn

---

## Dataset

The dataset contains information about flights, including:

- Airline
- Source
- Destination
- Date of Journey
- Departure Time
- Arrival Time
- Duration
- Total Stops
- Ticket Price

---

## Project Workflow

### 1. Data Preprocessing

- Cleaned and prepared the dataset
- Extracted date and time features
- Encoded categorical variables
- Created duration-related features

### 2. Exploratory Data Analysis (EDA)

- Analyzed price distributions
- Investigated relationships between features and ticket prices
- Identified important predictors

### 3. Model Training

Several machine learning models were tested and compared.

Final model:

- Random Forest Regressor

### 4. Model Evaluation

Performance was evaluated using:

- R² Score
- Mean Absolute Error (MAE)

---

## Feature Importance

The most influential features include:

- Destination
- Airline
- Total Stops
- Flight Duration
- Source Airport
- Departure and Arrival Time

---

## Streamlit Application

The project includes a Streamlit web application that allows users to:

- Select airline
- Choose source and destination
- Select journey date
- Enter departure and arrival times
- Choose number of stops
- Receive a predicted flight price

---

## Repository Structure

```text
flight-price-prediction/
│
├── flight_app.py
├── Flight_Price_Prediction.ipynb
├── requirements.txt
└── README.md
```

---

## How to Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit application:

```bash
streamlit run flight_app.py
```

---

## Future Improvements

- Hyperparameter optimization
- Cloud deployment
- Pipeline-based preprocessing
- Model monitoring
- Additional feature engineering
