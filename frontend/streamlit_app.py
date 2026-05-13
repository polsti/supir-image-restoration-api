import io

import requests
import streamlit as st
from PIL import Image


API_URL = "http://127.0.0.1:8000/restore"


st.set_page_config(
    page_title="SUPIR Image Restoration",
    layout="wide",
)


st.title("SUPIR Image Restoration")
st.write(
    "Upload a low-quality image, choose restoration settings, "
    "and send it to the FastAPI backend."
)


uploaded_file = st.file_uploader(
    "Upload image",
    type=["jpg", "jpeg", "png"],
)
# (width * upscale, height * upscale)
# if 300x300 and upscale 2 -> 600x600
# just a resize
upscale = st.selectbox(
    "Upscale factor",
    options=[1, 2, 4],
    index=1,
)

mode = st.selectbox(
    "Restoration mode",
    options=["balanced", "strong", "old_photo"],
    index=0,
)
st.caption(
    "Balanced = normal restoration, Strong = stronger sharpening/contrast, "
    "Old photo = grayscale-style restoration for damaged old images."
)
# either 
# q - quality 
# f - fidelity model
model_type = st.selectbox(
    "SUPIR model type",
    options=["Q", "F"],
    index=0,
)

if uploaded_file is not None:
    original_image = Image.open(uploaded_file).convert("RGB")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original image")
        st.write(
            f"Resolution: "
            f"{original_image.width}x{original_image.height}"
        )
        st.image(
            original_image,
            use_container_width=True,
        )

    if st.button("Restore image"):
        with st.spinner("Sending image to backend..."):
            files = {
                "image": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type,
                )
            }

            data = {
                "upscale": upscale,
                "mode": mode,
                "model_type": model_type,
            }

            response = requests.post(
                API_URL,
                files=files,
                data=data,
                timeout=300,
            )

            if response.status_code == 200:
                restored_image = Image.open(io.BytesIO(response.content))

                with col2:
                    st.subheader("Restored image")
                    st.write(
                        f"Resolution: "
                        f"{restored_image.width}x{restored_image.height}"
                    )
                    st.image(
                        restored_image,
                        use_container_width=True,
                    )
                    
                st.download_button(
                    label="Download restored image",
                    data=response.content,
                    file_name="restored_image.png",
                    mime="image/png",
                )
            else:
                st.error(f"Backend error: {response.status_code}")
                st.text(response.text)
else:
    st.info("Upload an image to start.")