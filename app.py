import os 
import streamlit as st
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Custom CSS for styling
def set_custom_css():
    st.markdown(
        """
        <style>
        .title { font-size: 30px; text-align: center; }
        .subheader { font-size: 20px; text-align: center; }
        .custom-prompt-label { font-size: 18px; }
        .stTextInput > div > input { font-size: 18px; }
        .file-uploader label { font-size: 18px; }
        .stButton button { font-size: 20px; width: 100%; }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Initialize the model globally
model = genai.GenerativeModel("gemini-1.5-flash-002")

# Set the model behavior
model_behavior = """
    You are a finance operations expert who understands the overall structure of the invoice and has a deep understanding of it.
    You will be shared with, the invoice image and you have to answer the question based on the information available in the image.
"""

# Method to read the uploaded image in bytes
def get_image_bytes(uploaded_image):
    if uploaded_image is not None:
        image_bytes = uploaded_image.getvalue()
        image_info = [{"mime_type": uploaded_image.type, "data": image_bytes}]
        return image_info
    else:
        raise FileNotFoundError("Upload a valid image file!")

# Method to get the response from the Gemini API
def get_response(image, prompt):
    response = model.generate_content([model_behavior, image[0], prompt])
    return response.text

def main():
    # Set the Streamlit page configuration
    st.set_page_config(page_title="Invoice Extraction Bot")

    # Apply custom CSS
    set_custom_css()

    # Title
    st.markdown("<h1 class='title'>⮮ AIOCR ⮀ Gemini 1.5 Flash ⮯</h1>", unsafe_allow_html=True)

    # Prompt label
    st.markdown('<h1 class="custom-prompt-label">Enter your prompt</h1>', unsafe_allow_html=True)

    # Prompt input
    prompt = st.text_area(
        "Prompt",
        key="prompt",
        label_visibility="collapsed",
        placeholder="Type your message here...",
        height=50,
    )

    # Submit button
    submit = st.button("Upload & Submit")

    # Sidebar for file uploader
    with st.sidebar:
        st.markdown(
            "<h1 style='text-align: center; font-size: 18px;'>Choose an image</h1>",
            unsafe_allow_html=True,
        )

        # File uploader widget
        uploaded_image = st.file_uploader(
            "Image", type=["jpg", "png", "jpeg"], label_visibility="collapsed"
        )

        if uploaded_image is not None:
            image = Image.open(uploaded_image)
            st.image(image, caption="Your image", use_column_width=True)

    # If user pressed submit button or entered a prompt
    if submit or prompt:
        if len(prompt) > 0:
            if uploaded_image is not None:
                # Get uploaded image file in bytes
                image_info = get_image_bytes(uploaded_image)
                response = get_response(image_info, prompt)
                st.write(response)
            else:
                st.error("Please upload a valid image file!")
        else:
            st.error("Please enter a valid prompt!")

# Invoking main function
if __name__ == "__main__":
    main()
