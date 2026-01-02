import streamlit as st
import requests
import io
from PIL import Image

# Page Config
st.set_page_config(page_title="Free AI Interior Designer", layout="centered")
st.title("🏠 Free AI Interior Designer")

# Securely get your token from Streamlit Secrets or Sidebar
hf_token = st.sidebar.text_input("Enter Hugging Face Token (hf_...)", type="password")

# Free Model URL (Stable Diffusion XL is great for interiors)
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {hf_token}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

# User Inputs
col1, col2 = st.columns(2)
with col1:
    room_type = st.selectbox("Room Type", ["Living Room", "Bedroom", "Kitchen", "Office"])
    dimensions = st.text_input("Dimensions (e.g., 10x12 ft)", "12x15 ft")

with col2:
    color = st.color_picker("Main Color", "#E0D7C6")
    style = st.selectbox("Style", ["Modern", "Minimalist", "Scandinavian", "Industrial"])

if st.button("Generate Design"):
    if not hf_token:
        st.error("Please enter your Hugging Face token in the sidebar!")
    else:
        with st.spinner("Generating free design..."):
            # Constructing the prompt
            prompt = (f"High quality interior design photography of a {style} {room_type}, "
                      f"room size {dimensions}, primary color {color}, professional lighting, "
                      f"highly detailed, 8k resolution, architectural digest style.")
            
            image_bytes = query({"inputs": prompt})
            
            try:
                image = Image.open(io.BytesIO(image_bytes))
                st.image(image, caption=f"Your {style} {room_type}")
            except:
                st.error("The model is still loading or busy. Please wait 30 seconds and try again!")
