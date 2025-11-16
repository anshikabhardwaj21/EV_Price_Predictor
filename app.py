import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

# ---------------------------
# Load trained pipeline model
# ---------------------------
MODEL_PATH = Path("model/ev_price_model.pkl")

if not MODEL_PATH.exists():
    st.error("❌ Model file not found! Make sure ev_price_model.pkl exists inside the /model folder.")
    st.stop()

model = joblib.load(MODEL_PATH)

# ---------------------------
# Streamlit UI
# ---------------------------
st.set_page_config(page_title="EV Price Predictor", layout="centered")
st.title("🚗 Electric Vehicle Base MSRP Predictor")
st.write("Fill in the vehicle details to predict the estimated price.")

# ---------------------------
# Input form
# ---------------------------
col1, col2 = st.columns(2)

with col1:
    model_year = st.number_input("Model Year", min_value=1990, max_value=2035, value=2021)
    make = st.text_input("Make (e.g., TESLA, BMW)", value="TESLA")
    model_name = st.text_input("Model (e.g., MODEL 3)", value="MODEL 3")
    ev_type = st.selectbox("Electric Vehicle Type", [
        "Battery Electric Vehicle (BEV)",
        "Plug-in Hybrid Electric Vehicle (PHEV)"
    ])

with col2:
    ev_range = st.number_input("Electric Range (miles)", min_value=0, max_value=700, value=260)
    city = st.text_input("City", value="SEATTLE")
    county = st.text_input("County", value="KING")
    postal_code = st.text_input("Postal Code", value="98109")
    state = st.text_input("State", value="WA")

# Correct CAFV Categories (from your model encoder!)
cafv = st.selectbox("Clean Alternative Fuel Vehicle (CAFV) Eligibility", [
    "Clean Alternative Fuel Vehicle Eligible",
    "Eligibility unknown as battery range has not been researched",
    "Not eligible due to low battery range"
])

# ---------------------------
# Build input dataframe
# MODEL WAS TRAINED ON 10 FEATURES — INCLUDE ALL EXACT COLUMNS!
# ---------------------------

input_df = pd.DataFrame([{
    "County": county,
    "City": city,
    "State": state,
    "Postal Code": postal_code,
    "Model Year": model_year,
    "Make": make,
    "Model": model_name,
    "Electric Vehicle Type": ev_type,
    "Clean Alternative Fuel Vehicle (CAFV) Eligibility": cafv,
    "Electric Range": ev_range
}])

st.write("### 🔎 Input Data Preview")
st.dataframe(input_df)

# ---------------------------
# Prediction
# ---------------------------
if st.button("Predict Price"):
    try:
        prediction = model.predict(input_df)[0]
        st.success(f"💰 **Predicted EV Base MSRP:** ${prediction:,.2f}")
    except Exception as e:
        st.error("❌ Prediction failed. The model might not match expected inputs.")
        st.write(e)


