import streamlit as st
import pandas as pd
import numpy as np
from keras.models import load_model

# Load the model
model_path = 'C:/Users/USER/Downloads/patientprediction/blood_count_data_model (1).h5'

try:
    model = load_model(model_path)
except FileNotFoundError:
    raise FileNotFoundError(f"The model file was not found at: {model_path}")
except Exception as e:
    print(f"An error occurred while loading the model: {e}")

# Define the features used for training
# Ensure these match what you used when training the model
feature_columns = ['Age', 'Gender_male']  # Update this based on your actual feature columns

# Function to analyze health
def analyze_health(predicted_values):
    hemoglobin = predicted_values['hemoglobin']
    platelet_count = predicted_values['platelet_count']
    white_blood_cells = predicted_values['white_blood_cells']
    red_blood_cells = predicted_values['red_blood_cells']
    mcv = predicted_values['mcv']
    mch = predicted_values['mch']
    mchc = predicted_values['mchc']

    health_status = "Healthy"
    severity = 0
    suggestions = []

    if hemoglobin < 12 or hemoglobin > 16:
        health_status = "Unhealthy"
        severity += 2
        suggestions.append("Consult a doctor regarding hemoglobin levels.")
    
    if platelet_count < 150000 or platelet_count > 450000:
        health_status = "Unhealthy"
        severity += 1
        suggestions.append("Monitor your platelet count and consult a healthcare provider.")

    if white_blood_cells < 4000 or white_blood_cells > 10000:
        health_status = "Unhealthy"
        severity += 1
        suggestions.append("Consider lifestyle changes to boost immune health.")

    if red_blood_cells < 4.0 or red_blood_cells > 5.5:
        health_status = "Unhealthy"
        severity += 2
        suggestions.append("Discuss your RBC levels with a healthcare professional.")

    if mcv < 80 or mcv > 100:
        health_status = "Unhealthy"
        severity += 1
        suggestions.append("Consider dietary changes or supplements.")

    if mch < 27 or mch > 32:
        health_status = "Unhealthy"
        severity += 1
        suggestions.append("Consult a healthcare provider regarding MCH levels.")

    if mchc < 32 or mchc > 36:
        health_status = "Unhealthy"
        severity += 1
        suggestions.append("Monitor MCHC levels and consider dietary adjustments.")

    severity = min(severity, 5)

    return {
        'health_status': health_status,
        'severity': severity,
        'suggestions': suggestions
    }

# Function to prepare input for prediction
def prepare_input(age, gender):
    new_data = pd.DataFrame({'Age': [age], 'Gender_male': [1 if gender == 'male' else 0]})
    # Ensure all necessary columns are present
    for col in feature_columns:
        if col not in new_data.columns:
            new_data[col] = 0
    new_data = new_data[feature_columns]

    # Convert 'Age' column to int64
    new_data['Age'] = new_data['Age'].astype(np.int64)
    return new_data

# Streamlit UI
st.title("Blood Count Prediction App")
st.header("Enter your details")

age = st.number_input("Enter your age:", min_value=0, max_value=120)
gender = st.selectbox("Select your gender:", ["male", "female"])

if st.button("Predict"):
    input_data = prepare_input(age, gender)
    prediction = model.predict(input_data)

    # Display predictions
    st.subheader("Predicted Blood Count Values:")
    st.write(f"Hemoglobin: {prediction[0][0]:.2f}")
    st.write(f"Platelet Count: {prediction[0][1]:.2f}")
    st.write(f"White Blood Cells: {prediction[0][2]:.2f}")
    st.write(f"Red Blood Cells: {prediction[0][3]:.2f}")
    st.write(f"MCV: {prediction[0][4]:.2f}")
    st.write(f"MCH: {prediction[0][5]:.2f}")
    st.write(f"MCHC: {prediction[0][6]:.2f}")

    # Analyze health based on predictions
    health_analysis = analyze_health({
        'hemoglobin': prediction[0][0],
        'platelet_count': prediction[0][1],
        'white_blood_cells': prediction[0][2],
        'red_blood_cells': prediction[0][3],
        'mcv': prediction[0][4],
        'mch': prediction[0][5],
        'mchc': prediction[0][6]
    })

    st.subheader("Health Analysis:")
    st.write(f"Health Status: {health_analysis['health_status']}")
    st.write(f"Severity (out of 5): {health_analysis['severity']}")
    st.write("Suggestions for Improvement:")
    for suggestion in health_analysis['suggestions']:
        st.write(f"- {suggestion}")