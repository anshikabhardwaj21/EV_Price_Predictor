import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

# Load model
MODEL_PATH = Path("model/ev_price_model.pkl")
if not MODEL_PATH.exists():
    st.error("Model not found. Train the notebook first.")
    st.stop()

model = joblib.load(MODEL_PATH)

st.set_page_config(page_title="EV Price Predictor", layout="centered")
st.title("Electric Vehicle Price Predictor")
st.write("Enter vehicle features to predict the Base MSRP (price)")

# Input fields
col1, col2 = st.columns(2)
with col1:
    model_year = st.number_input("Model Year", min_value=1990, max_value=2030, value=2020)
    make = st.text_input("Make (e.g., TESLA, BMW)", value="TESLA")
    model_name = st.text_input("Model (e.g., MODEL 3)", value="MODEL 3")
    ev_type = st.selectbox("Electric Vehicle Type", options=["Battery Electric Vehicle (BEV)", "Plug-in Hybrid Electric Vehicle (PHEV)"])

with col2:
    ev_range = st.number_input("Electric Range (miles)", min_value=0, max_value=1000, value=250)
    city = st.text_input("City", value="SEATTLE")
    county = st.text_input("County", value="KING")
    postal_code = st.text_input("Postal Code", value="98109")
    state = st.text_input("State", value="WA")

cafv = st.selectbox("Clean Alternative Fuel Vehicle (CAFV) Eligibility", options=[
    "Clean Alternative Fuel Vehicle Eligible",
    "Not eligible due to low battery range",
    "Unknown"
], index=2)

# Predict button
if st.button("Predict Price"):
    input_df = pd.DataFrame([{
        'Make': make,
        'Model': model_name,
        'Model Year': model_year,
        'Electric Vehicle Type': ev_type,
        'Electric Range': ev_range,
        'City': city,
        'State': state,
        'Postal Code': postal_code,
        'County': county,
        'Clean Alternative Fuel Vehicle (CAFV) Eligibility': cafv
    }])

    st.write("### Input Data Preview:")
    st.dataframe(input_df)

    try:
        pred = model.predict(input_df)[0]
        st.success(f"Predicted EV Base MSRP: ${pred:,.2f}")
    except Exception as e:
        st.error("Error making prediction. Check column names and preprocessing.")
        st.write(e)
