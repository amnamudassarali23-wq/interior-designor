import streamlit as st
from openai import OpenAI

# Page Config
st.set_page_config(page_title="AI Interior Designer", layout="centered")
st.title("🏠 AI Interior Designer")

# Sidebar for API Key (or use Streamlit Secrets)
api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")

if api_key:
    client = OpenAI(api_key=api_key)

    # User Inputs
    col1, col2 = st.columns(2)
    with col1:
        room_type = st.selectbox("Room Type", ["Living Room", "Bedroom", "Kitchen", "Office", "Bathroom"])
        dimensions = st.text_input("Dimensions (e.g., 12x15 ft)", "10x10 ft")
    
    with col2:
        primary_color = st.color_picker("Primary Color", "#F5F5DC")
        contrast = st.select_slider("Color Contrast", options=["Low", "Medium", "High"])

    style = st.selectbox("Design Style", ["Modern", "Minimalist", "Industrial", "Bohemian", "Scandinavian"])

    if st.button("Generate Design"):
        with st.spinner("Designing your space..."):
            # Prompt Engineering: Combining inputs into a professional prompt
            prompt = (f"A professional architectural interior design photo of a {style} {room_type}. "
                      f"The room size is {dimensions}. The primary color theme is {primary_color} "
                      f"with {contrast} contrast lighting. High-end furniture, realistic textures, "
                      f"8k resolution, cinematic lighting, architectural photography.")

            try:
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    size="1024x1024",
                    quality="standard",
                    n=1,
                )

                image_url = response.data[0].url
                st.image(image_url, caption=f"Your {style} {room_type}")
                st.balloons()
            except Exception as e:
                st.error(f"An error occurred: {e}")
else:
    st.info("Please enter your OpenAI API key in the sidebar to start.")
