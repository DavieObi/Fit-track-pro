import streamlit as st
import os

# Access the API key from secrets
GOOGLE_API_KEY = st.secrets["general"]["GOOGLE_API_KEY"]
os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY

# Example function that uses the GOOGLE_API_KEY
def some_function_that_uses_api():
    # Here we just display the API key for demonstration
    # In a real application, you would use this key to make API calls
    st.write("Using Google API Key:", os.environ['GOOGLE_API_KEY'])
    
    # Example of making an API call (commented out)
    # import requests
    # response = requests.get(f'https://example.com/api?key={os.environ["GOOGLE_API_KEY"]}')
    # st.write(response.json())  # Handle response here

# Streamlit app layout
st.title("My Streamlit App")
st.write("This app uses a Google API key stored in secrets.")

# Call the function
some_function_that_uses_api()
