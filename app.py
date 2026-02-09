import streamlit as st
import pickle
import os
from streamlit_option_menu import option_menu

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="Multiple Disease Prediction",
    layout="wide",
    page_icon="🏥"
)

# --------------------------------------------------
# Load Models
# --------------------------------------------------
working_dir = os.path.dirname(os.path.abspath(__file__))

diabetes_model = pickle.load(open(os.path.join(working_dir, "saved_models/diabetes.pkl"), "rb"))
heart_disease_model = pickle.load(open(os.path.join(working_dir, "saved_models/heart.pkl"), "rb"))
kidney_disease_model = pickle.load(open(os.path.join(working_dir, "saved_models/kidney.pkl"), "rb"))

# --------------------------------------------------
# Sidebar Menu
# --------------------------------------------------
with st.sidebar:
    selected = option_menu(
        "Multiple Disease Prediction",
        ["Diabetes Prediction", "Heart Disease Prediction", "Kidney Disease Prediction"],
        icons=["activity", "heart", "person"],
        menu_icon="hospital-fill",
        default_index=0
    )

# ==================================================
# DIABETES PREDICTION
# ==================================================
if selected == "Diabetes Prediction":

    st.title("🩸 Diabetes Prediction")

    col1, col2, col3 = st.columns(3)

    with col1:
        Pregnancies = st.number_input("Pregnancies", min_value=0, step=1)
    with col2:
        Glucose = st.number_input("Glucose Level", min_value=0.0)
    with col3:
        BloodPressure = st.number_input("Blood Pressure", min_value=0.0)

    with col1:
        SkinThickness = st.number_input("Skin Thickness", min_value=0.0)
    with col2:
        Insulin = st.number_input("Insulin", min_value=0.0)
    with col3:
        BMI = st.number_input("BMI", min_value=0.0)

    with col1:
        DiabetesPedigreeFunction = st.number_input("Diabetes Pedigree Function", min_value=0.0)
    with col2:
        Age = st.number_input("Age", min_value=0, step=1)

    diabetes_result = ""

    if st.button("Diabetes Test Result"):

        # Reset derived features
        NewBMI_Underweight = NewBMI_Overweight = 0
        NewBMI_Obesity_1 = NewBMI_Obesity_2 = NewBMI_Obesity_3 = 0
        NewInsulinScore_Normal = 0
        NewGlucose_Low = NewGlucose_Normal = 0
        NewGlucose_Overweight = NewGlucose_Secret = 0

        # BMI Categories
        if BMI <= 18.5:
            NewBMI_Underweight = 1
        elif 24.9 < BMI <= 29.9:
            NewBMI_Overweight = 1
        elif 29.9 < BMI <= 34.9:
            NewBMI_Obesity_1 = 1
        elif 34.9 < BMI <= 39.9:
            NewBMI_Obesity_2 = 1
        elif BMI > 39.9:
            NewBMI_Obesity_3 = 1

        # Insulin
        if 16 <= Insulin <= 166:
            NewInsulinScore_Normal = 1

        # Glucose
        if Glucose <= 70:
            NewGlucose_Low = 1
        elif 70 < Glucose <= 99:
            NewGlucose_Normal = 1
        elif 99 < Glucose <= 126:
            NewGlucose_Overweight = 1
        else:
            NewGlucose_Secret = 1

        user_input = [
            Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin,
            BMI, DiabetesPedigreeFunction, Age,
            NewBMI_Underweight, NewBMI_Overweight,
            NewBMI_Obesity_1, NewBMI_Obesity_2, NewBMI_Obesity_3,
            NewInsulinScore_Normal,
            NewGlucose_Low, NewGlucose_Normal,
            NewGlucose_Overweight, NewGlucose_Secret
        ]

        prediction = diabetes_model.predict([user_input])

        diabetes_result = (
            "🔴 The person is diabetic"
            if prediction[0] == 1
            else "🟢 The person is not diabetic"
        )

    st.success(diabetes_result)

# ==================================================
# HEART DISEASE PREDICTION
# ==================================================
if selected == "Heart Disease Prediction":

    st.title("❤️ Heart Disease Prediction")

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.number_input("Age", min_value=0, step=1)
    with col2:
        sex = st.number_input("Sex (0 = Female, 1 = Male)", min_value=0, max_value=1)
    with col3:
        cp = st.number_input("Chest Pain Type", min_value=0)

    with col1:
        trestbps = st.number_input("Resting Blood Pressure", min_value=0.0)
    with col2:
        chol = st.number_input("Cholesterol", min_value=0.0)
    with col3:
        fbs = st.number_input("Fasting Blood Sugar > 120", min_value=0, max_value=1)

    with col1:
        restecg = st.number_input("Rest ECG", min_value=0)
    with col2:
        thalach = st.number_input("Max Heart Rate", min_value=0.0)
    with col3:
        exang = st.number_input("Exercise Induced Angina", min_value=0, max_value=1)

    with col1:
        oldpeak = st.number_input("ST Depression", min_value=0.0)
    with col2:
        slope = st.number_input("Slope", min_value=0)
    with col3:
        ca = st.number_input("Major Vessels", min_value=0)

    with col1:
        thal = st.number_input("Thal", min_value=0)

    heart_result = ""

    if st.button("Heart Disease Test Result"):
        user_input = [
            age, sex, cp, trestbps, chol, fbs,
            restecg, thalach, exang, oldpeak,
            slope, ca, thal
        ]

        prediction = heart_disease_model.predict([user_input])

        heart_result = (
            "🔴 Person has heart disease"
            if prediction[0] == 1
            else "🟢 Person does not have heart disease"
        )

    st.success(heart_result)

# ==================================================
# KIDNEY DISEASE PREDICTION
# ==================================================
if selected == "Kidney Disease Prediction":

    st.title("🧬 Kidney Disease Prediction")

    inputs = []
    labels = [
        "Age", "Blood Pressure", "Specific Gravity", "Albumin", "Sugar",
        "Red Blood Cells", "Pus Cell", "Pus Cell Clumps", "Bacteria",
        "Blood Glucose Random", "Blood Urea", "Serum Creatinine",
        "Sodium", "Potassium", "Haemoglobin", "Packed Cell Volume",
        "White Blood Cell Count", "Red Blood Cell Count", "Hypertension",
        "Diabetes Mellitus", "Coronary Artery Disease", "Appetite",
        "Pedal Edema", "Anaemia"
    ]

    cols = st.columns(4)
    for i, label in enumerate(labels):
        with cols[i % 4]:
            inputs.append(st.number_input(label, min_value=0.0))

    kidney_result = ""

    if st.button("Kidney Test Result"):
        prediction = kidney_disease_model.predict([inputs])

        kidney_result = (
            "🔴 The person has kidney disease"
            if prediction[0] == 1
            else "🟢 The person does not have kidney disease"
        )

    st.success(kidney_result)
