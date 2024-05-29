from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
css = """
<style>
.title {
    font-size: 48px;
    color: #00FFFF;
    text-align: left;
}
.txt {
    font-size: 16px;
    color: #4F8BF9;
    text-align: left;
}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

## Function to load Google Gemini Pro Vision API And get response

def get_gemini_repsonse(input, image, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, image[0], prompt])
    return response.text


def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


##initialize our streamlit app

#st.set_page_config(page_title="NutriGuide Health Ai")
st.markdown('<h1 class="title">🧑🏻‍🍳NutriGuide Health Ai</h1>', unsafe_allow_html=True)
#st.header("NutriGuide Health Ai")
st.markdown('<h1 class="txt">Just Upload the image of the food !!</h1>', unsafe_allow_html=True)
#st.markdown("Just Upload the image of the food !!")
st.markdown('<h1 class="txt">NutriGuide is here to give the entire nutrition breakdown of the itme</h1>', unsafe_allow_html=True)
#st.text("NutriGuide is here to give the entire nutrition breakdown of the itme")
input = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me the total calories")

input_prompt = """
You are an expert in nutritionist where you need to see the food items from the image 
               and tell is the food healthy, suggestion & calculate the total calories, also provide the details of every food items with calories intake
               is below format of list :-

               1. Item 1 - no of calories
               2. Item 2 - no of calories
               ----
               ----


"""

## If submit button is clicked

if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_repsonse(input_prompt, image_data, input)
    st.subheader("The Response is")
    st.write(response)
