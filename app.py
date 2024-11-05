import streamlit as st
import os
# Remove load_dotenv() since we are using secrets.toml

# Access the API key from secrets
try:
    GOOGLE_API_KEY = st.secrets["general"]["GOOGLE_API_KEY"]
    os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY
    st.write("API Key loaded successfully.")
except KeyError:
    st.error("API Key not found in secrets. Please check your secrets.toml file.")



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

# Function to determine ideal weight range based on height
def calculate_ideal_weight(height_cm):
    height_m = height_cm / 100
    ideal_bmi_low = 18.5
    ideal_bmi_high = 24.9
    min_weight = ideal_bmi_low * (height_m ** 2)
    max_weight = ideal_bmi_high * (height_m ** 2)
    return min_weight, max_weight

# Function to generate advice using the Gemini API
def fetch_gpt_advice(prompt_text):
    try:
        model = gpt.GenerativeModel("gemini-1.5-pro")
        result = model.generate_content([prompt_text])
        return result.text
    except Exception as error:
        st.error(f"API Error: {error}")
        return ""

# Styled app title
st.markdown(
    "<h1 style='text-align: center; font-weight: bold; color: #4A90E2;'>FitTrack Pro</h1>", 
    unsafe_allow_html=True
)

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
        min_weight, max_weight = calculate_ideal_weight(user_height)

        st.write(f"Hello, {user_name}! Your BMI is: {bmi_value:.2f} ({classification})")
        st.write(f"For a BMI between 18.5 and 24.9, your ideal weight range is: {min_weight:.2f} kg - {max_weight:.2f} kg.")

        # Construct prompt for API response
        advice_prompt = f"""
        As a health and fitness consultant, provide tailored advice for a user with the following details:
        
        - BMI: {bmi_value:.2f}
        - Category: {classification}
        - Recommended Weight Range: {min_weight:.2f} kg - {max_weight:.2f} kg
        
        Please include:
        1. A diet plan with sample meals and suggested daily caloric intake.
        2. A workout plan suitable for this BMI category.
        3. General wellness tips for weight maintenance or goal achievement.
        """

        with st.spinner("Creating personalized recommendations..."):
            advice_response = fetch_gpt_advice(advice_prompt)
            st.markdown("**Personalized Recommendations:**")
            st.write(advice_response)
    else:
        st.error("Height and weight must be valid positive values.")

