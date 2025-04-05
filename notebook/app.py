import streamlit as st
import pickle
import pandas as pd

# Load model + column structure
model = pickle.load(open("electrification_model.pkl", "rb"))
model_columns = pickle.load(open("model_columns.pkl", "rb"))

st.title("🔌 Electrification Candidate Predictor")

# Input fields
floor_area = st.number_input("Floor Area (sqft)", value=1500)
hdd = st.number_input("Annual Heating Degree Days (HDD)", value=3000)
income = st.number_input("Estimated Household Income (in $1000s)", value=60)

fuel_type = st.selectbox(
    "Current Heating Fuel",
    ["Electricity", "Fuel Oil", "Natural Gas", "Wood", "Other"]
)

# Create input DataFrame with one-hot encoding
input_dict = {
    'floor_area': floor_area,
    'HDD': hdd,
    'estimated_income': income,
    'heating_fuel_Fuel Oil': 0,
    'heating_fuel_Natural Gas': 0,
    'heating_fuel_Wood': 0,
    'heating_fuel_Other': 0,
}

if fuel_type != 'Electricity':
    key = f'heating_fuel_{fuel_type}'
    input_dict[key] = 1

# Ensure all required columns are in the input
for col in model_columns:
    if col not in input_dict:
        input_dict[col] = 0  # Add missing columns as 0

# Align with training column order
input_df = pd.DataFrame([input_dict])[model_columns]

# Predict
proba = model.predict_proba(input_df)[0][1]  # probability of class 1
threshold = st.slider("Minimum probability to recommend electrification:", 0.0, 1.0, 0.5)
prediction = int(proba >= threshold)

st.write(f"🔍 Model score: {proba:.3f} (Threshold: {threshold})")



# Output
if prediction == 1:
    st.success("✅ This home is a strong electrification candidate!")
else:
    st.warning("❌ This home may not be a strong candidate for electrification.")

