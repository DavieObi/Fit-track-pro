import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as gpt

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  
os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY

# Define a cached function for creating recommendations
@st.cache_data
def create_recommendations(user_data):
    prompt_text = f"""
    As a health and fitness consultant, provide tailored advice for a user with the following details:

    - Name: {user_data['name']}
    - Age: {user_data['age']}
    - Height: {user_data['height']}
    - Weight: {user_data['weight']}
    """

    # Call the API to generate advice
    try:
        model = gpt.GenerativeModel("gemini-1.5-pro")
        result = model.generate_content([prompt_text])
        return result.text
    except Exception as error:
        st.error(f"API Error: {error}")
        return ""

# Function to compute BMI
def compute_bmi(weight_kg, height_cm):
    height_m = height_cm / 100  # Convert height from cm to meters
    return weight_kg / (height_m ** 2)

# Function to determine BMI classification
def bmi_classification(bmi_value):
    if bmi_value < 18.5:
        return "Underweight"
    elif 18.5 <= bmi_value < 24.9:
        return "Normal Weight"
    elif 25 <= bmi_value < 29.9:
        return "Overweight"
    else:
        return "Obese"

# Streamlit app layout
st.title("FitTrack Pro")

# Input form for user details
with st.form(key='user_data_form'):
    user_name = st.text_input("Enter your name")
    user_age = st.number_input("Age", min_value=1)
    user_height = st.number_input("Height (cm)", min_value=50, max_value=250)
    user_weight = st.number_input("Weight (kg)", min_value=10, max_value=300)
    calculate_button = st.form_submit_button("Compute BMI & Recommendations")

if calculate_button:
    if user_height > 0 and user_weight > 0:
        bmi_value = compute_bmi(user_weight, user_height)
        classification = bmi_classification(bmi_value)

        st.write(f"Hello, {user_name}! Your BMI is: {bmi_value:.2f} ({classification}).")

        # Create user data dictionary
        user_data = {
            'name': user_name,
            'age': user_age,
            'height': user_height,
            'weight': user_weight
        }

        # Call the cached function to get recommendations
        recommendations = create_recommendations(user_data)
        st.markdown("**Personalized Recommendations:**")
        st.write(recommendations)
    else:
        st.error("Height and weight must be valid positive values.")
