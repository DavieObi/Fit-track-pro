import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as gpt

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  
os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY

@st.cache_data
def calculate_bmi(weight_kg, height_cm):
    height_m = height_cm / 100
    return weight_kg / (height_m ** 2)

@st.cache_data
def generate_recommendations(user_data):
    prompt_text = f"Provide health advice for {user_data['name']} who is {user_data['age']} years old, {user_data['height']} cm tall, and weighs {user_data['weight']} kg."
    try:
        model = gpt.GenerativeModel("gemini-1.5-pro")
        result = model.generate_content([prompt_text])
        return result.text
    except Exception as error:
        st.error(f"API Error: {error}")
        return ""

def bmi_classification(bmi_value):
    if bmi_value < 18.5:
        return "Underweight"
    elif 18.5 <= bmi_value < 24.9:
        return "Normal Weight"
    elif 25 <= bmi_value < 29.9:
        return "Overweight"
    else:
        return "Obese"

st.title("FitTrack Pro")

with st.form(key='user_data_form'):
    user_name = st.text_input("Enter your name")
    user_age = st.number_input("Age", min_value=1)
    user_height = st.number_input("Height (cm)", min_value=50, max_value=250)
    user_weight = st.number_input("Weight (kg)", min_value=10, max_value=300)
    calculate_button = st.form_submit_button("Compute BMI & Recommendations")

if calculate_button:
    if user_height > 0 and user_weight > 0:
        bmi_value = calculate_bmi(user_weight, user_height)
        classification = bmi_classification(bmi_value)
        
        st.write(f"Hello, {user_name}! Your BMI is: {bmi_value:.2f} ({classification}).")

        user_data = {
            'name': user_name,
            'age': user_age,
            'height': user_height,
            'weight': user_weight
        }

        recommendations = generate_recommendations(user_data)
        st.markdown("**Personalized Recommendations:**")
        st.write(recommendations)
    else:
        st.error("Height and weight must be valid positive values.")


