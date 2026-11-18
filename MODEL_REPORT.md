# Flight Price Prediction — Model Evaluation Report

## Executive summary

**Model:** Tuned Random Forest. **Test R²:** 0.8853.
**Test MAE:** 664.47. **Test RMSE:** 1,530.60.
**Test MAPE:** 7.60%.

The project predicts a flight fare from booking-related flight details such as
airline, destination, departure time, duration, journey date, and stop count.
It is an educational portfolio project, not a live flight pricing service.

## Dataset and validation

- **Rows:** 10,683; **training:** 8,012;
  **untouched test:** 2,671.
- **Split:** randomized 75% training / 25% test (`random_state=42`).
- **Model selection:** 3-fold training-only CV, minimizing mean absolute error.
- **Compared:** median prediction, Ridge regression, untuned Random Forest,
  and hyperparameter-tuned Random Forest.
- **Preprocessing:** deterministic feature engineering followed by fold-fitted
  missing-value imputation, scaling, and one-hot encoding in a single pipeline.
- **Leakage fix:** no category encoding based on the target price before splitting.

## Model comparison (training-only CV)

| Approach | CV MAE | CV R² |
| --- | ---: | ---: |
| Random Forest | 751.89 | 0.868 |
| Ridge regression | 1,801.70 | 0.647 |
| Median baseline | 3,627.95 | -0.025 |
| Tuned Random Forest | 747.58 | Not separately reported |

## Final test evaluation

| Metric | Score | What it means |
| --- | ---: | --- |
| MAE | 664.47 | Mean absolute prediction error in price units |
| RMSE | 1,530.60 | Penalizes particularly large errors |
| R² | 0.8853 | Variation explained relative to predicting the test-set mean |
| MAPE | 7.60% | Mean relative absolute error (prices here are positive) |

## Most important engineered features

Permutation importance, measured as the increase in MAE when one test feature
is shuffled (larger = more predictive contribution under the fitted model):

| Feature | Increase in MAE |
| --- | ---: |
| `Airline` | 1,824.09 |
| `duration_minutes` | 1,789.91 |
| `journey_month` | 861.97 |
| `Additional_Info` | 657.72 |
| `journey_day` | 497.28 |
| `total_stops` | 437.74 |

These are **interpretation diagnostics**, not causal effects. Feature
importance was not used to retune the model based on test data.

## Duplicate-overlap sensitivity check

Of the 2,671 random holdout examples,
157 share an **identical
raw feature row** with a training observation. A subset of the holdout can
therefore be easier to predict if the model memorizes repeated itineraries.
Restricting evaluation to the other 2,514
examples gives MAE = **653.03** and R² =
**0.8867**. This post-hoc diagnostic was not used to
tune the model and does not replace a group-based split at the outset.

## Limitations and next improvements

1. The dataset contains historical fares and lacks booking lead time, live
   demand, and competitor pricing information.
2. A random split may include similar itineraries in both sets; test a
   chronological or group-based holdout for stronger generalization evidence.
3. Some rare/high-price flights can be more difficult to predict. Inspect
   residuals before deciding whether a transformed target is appropriate.
4. Compare a gradient-boosting model in a **new** training-only experiment;
   preserve the present test set for final validation of the next iteration.
5. Add unit tests for date/time parsing and a Streamlit UI, then document the
   input schema and model-monitoring approach.

## Interview explanation (English, B1–B2)

> In my Flight Price Prediction project, I built a regression pipeline in
> Python with pandas and scikit-learn. I cleaned the data and created features
> such as flight duration, departure hour, and number of stops. I compared a
> baseline model, Ridge regression, and Random Forest using cross-validation.
> To avoid data leakage, I split the data first and fitted preprocessing only
> on the training data. The final model achieved an R² score of
> 0.89 and a mean absolute error of about 664 on
> the held-out test set. I also checked the biggest prediction errors and
> looked at feature importance to understand the model better.

The original training Excel file is deliberately omitted from the published
archive until its redistribution rights and attribution are confirmed.
