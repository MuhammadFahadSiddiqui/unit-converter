import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ Error: API Key is missing! Please check your .env file.")
else:
    genai.configure(api_key=api_key)

# Streamlit App Configuration
st.set_page_config(page_title="AI Unit Converter", layout="centered")
st.title("My AI Unit Converter")
st.write("Convert units effortlessly using AI!")

# Unit Categories
types_of_units = {
    "Length": ["Meters", "Kilometers", "Miles", "Inches", "Feet", "Yards"],
    "Weight": ["Grams", "Kilograms", "Pounds", "Ounces", "Tons"],
    "Time": ["Seconds", "Minutes", "Hours", "Days", "Weeks", "Months", "Years"],
    "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
    "Energy": ["Joules", "Calories", "Kilowatt-hours"],
    "Volume": ["Liters", "Milliliters", "Cubic Meters", "Gallons", "Cups"],
    "Speed": ["Meters/sec", "km/h", "Miles/h"],
    "Area": ["Square Meters", "Square Kilometers", "Hectares", "Acres"]
}

# Unit Selection
unit_type = st.selectbox("Select Unit Type:", list(types_of_units.keys()))
from_unit = st.selectbox("Convert From:", types_of_units[unit_type])
to_unit = st.selectbox("Convert To:", types_of_units[unit_type])

# User Input
input_value = st.text_input("Enter the value to convert:")

if st.button("Convert"):  
    if input_value:
        try:
            # Convert input to float
            numeric_value = float(input_value)

            # Construct Query for AI
            query = f"Convert {numeric_value} {from_unit} to {to_unit}"
            
            # Use the correct model name
            model = genai.GenerativeModel("gemini-1.5-pro")
            response = model.generate_content(query)
            
            # Extract the response
            if hasattr(response, "text"):
                result = response.text.strip()
                st.success(f"**Converted Value:** {result}")
            else:
                st.error("⚠️ AI response was empty. Please try again!")

        except ValueError:
            st.error("⚠️ Please enter a valid numerical value for conversion!")
        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")
    else:
        st.warning("⚠️ Please enter a valid conversion value!")

st.write("Powered by Gemini AI 🚀")
