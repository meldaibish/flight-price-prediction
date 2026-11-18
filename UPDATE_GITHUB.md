# Updating your existing GitHub repository

Target: <https://github.com/meldaibish/flight-price-prediction>

**Do not upload** `Data_Train.xlsx`, tokens, credentials, or training files that do not have redistribution permission.

## Option A: Git (recommended for a clean replacement)

1. Clone your current repository, if it is not already on your machine:

   ```bash
   git clone https://github.com/meldaibish/flight-price-prediction.git
   cd flight-price-prediction
   ```

2. Make a backup or commit your previous work. Extract the ZIP provided with this update and **copy its contents** into the cloned folder. Do **not** delete the `.git` directory.

3. Remove the old single notebook if it is still present:

   ```bash
   git rm flight_prediction.ipynb
   ```

   If Git says that file does not exist, skip the command.

4. Verify the new `flight_app.py`, `src/`, `models/flight_price_model.joblib`, `notebooks/`, `tests/`, `README.md`, and `requirements.txt` are present. Do not add `data/Data_Train.xlsx`.

5. Review differences, then commit and push:

   ```bash
   git status
   git add -A
   git commit -m "Refactor flight price ML pipeline and Streamlit app"
   git push origin main
   ```

## Option B: GitHub website

1. Open the existing repository on GitHub (not a new one).
2. Upload new files and folders from this archive with **Add file → Upload files**. Files with the same path will be replaced after the commit.
3. Delete the old `flight_prediction.ipynb` separately, so visitors see the corrected notebook in `notebooks/`.
4. Review the new GitHub file tree and ensure `Data_Train.xlsx` was not published.

## After uploading

- For a live demo, create a Streamlit Community Cloud app with the repository, branch `main`, and main file `flight_app.py`.
- For local testing: `pip install -r requirements.txt` followed by `streamlit run flight_app.py`.
- The bundled `.joblib` is a Python pickle-family artifact: only load it from a source you trust, and retrain for different scikit-learn versions if required.
