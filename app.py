### Nutrition App Using Gemini Model

#importing required libraries 
from dotenv import load_dotenv 
load_dotenv() #load all the ennv variables
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image 

#configure the genai library by providing API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#implementing the function to get gemini response
def get_gemini_response(input_text, image):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_text, image[0]])
    return response.text

#implementing a function to read the image and set the image format
def input_image_setup(uploaded_file):
    #check if a file as uploaded or not 
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type, #get the mimi type to the uploaded file 
                "data": bytes_data
            }]
        
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

#deploy the model using streamlit framework
st.set_page_config(page_title="AI Nutritionist App")
st.header("AI Nutritionist App")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)
submit = st.button("Tell me the calories")

#writing a prompt for gemini model 
input_prompt = """ 
    You are an expert in nutritionist where you need to see the food items from the image 
    and calculate the total calories, also provide the details of every food items with calories intake 
    is below format

    1. Item 1 - no of calories
    2. Item 2 - no of calories
    --- 
    ---
    After that mention the meal is healthy meal or not and also mention the percentage split of ratio of 
    carbohydrates, proteins, fats, sugar and calories in meal.finally give suggestion which item 
    should be removed and which items should be added it meal to make the meal healthy if it's unhealthy
    and tell if the meal is Managing Diabetes or useful of body building or weight loss 
"""
#if submit button is clicked 
if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data)
    st.subheader("The response is:")
    st.write(response)
