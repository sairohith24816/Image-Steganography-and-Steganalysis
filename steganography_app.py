import streamlit as st
from PIL import Image
import numpy as np
import io
import input_generator
from encoding_decoding import decode_message, encode_message

# Use the actual encoding function from encoding_decoding.py

def encode_image(image, message, params):
    # Save the uploaded image to a temporary file
    temp_in = "temp_input.png"
    temp_out = "temp_encoded.png"
    image.save(temp_in)
    # Call the real encode_message function
    success = encode_message(
        img_path=temp_in,
        out_path=temp_out,
        message=message,
        start_position=params['start_position'],
        gap=params['gap'],
        channels=params['channels'],
        num_bits=params['num_bits'],
        delimiter_start=params['delimiter_start'],
        delimiter_end=params['delimiter_end'],
        horizontal=params['horizontal']
    )
    if not success:
        return None
    return Image.open(temp_out)

def detect_hidden_message(image, key_params):
    # Save the uploaded image to a temporary file for decoding
    temp_path = "temp_uploaded.png"
    image.save(temp_path)
    try:
        msg = decode_message(
            img_path=temp_path,
            start_position=key_params['start_position'],
            gap=key_params['gap'],
            channels=key_params['channels'],
            num_bits=key_params['num_bits'],
            delimiter_start=key_params['delimiter_start'],
            delimiter_end=key_params['delimiter_end'],
            horizontal=key_params['horizontal']
        )
        if msg and all(32 <= ord(c) < 127 for c in msg):
            return True, msg
        else:
            return False, ""
    except Exception as e:
        return False, f"Error: {e}"

st.title("Image Steganography & Detection App")

st.header("1. Upload an Image")
uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

delimiter_options = [
    ('#', '#'), ('##', '##'), ('***', '***'), ('[START]', '[END]'),
    ('<START>', '<END>'), ('<<START>>', '<<END>>'), ('<<', '>>'),
    ('{', '}'), ('|', '|'), ('+++', '+++'), ('BEGIN', 'END'),
    ('---', '---'), ('!!!', '!!!'), ('$$$', '$$$'), ('&&&', '&&&'), ('@@', '@@')
]

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)
    action = st.radio(
        "What do you want to do?",
        ("Hide a message in the image", "Detect hidden message in the image")
    )
    if action == "Hide a message in the image":
        st.header("Hide a Message in the Image")
        user_message = st.text_area("Enter the message you want to hide:")
        if st.button("Generate Steganography Input & Encode"):
            if not user_message:
                st.warning("Please enter a message to hide.")
            else:
                # Generate parameters using input_generator
                params = input_generator.generate_steganography_input(
                    rows=image.height, columns=image.width
                )
                params['message'] = user_message  # Overwrite with user message
                # Encode the image
                stego_image = encode_image(image, user_message, params)
                if stego_image is None:
                    st.error("Encoding failed. Please try with a different message or image.")
                else:
                    st.image(stego_image, caption="Steganographed Image", use_container_width=True)
                    st.subheader("Parameters Used:")
                    st.json(params)
                    # Download option
                    buf = io.BytesIO()
                    stego_image.save(buf, format="PNG")
                    byte_im = buf.getvalue()
                    st.download_button(
                        label="Download Steganographed Image",
                        data=byte_im,
                        file_name="steganographed.png",
                        mime="image/png"
                    )
                    # Store the last encoded image in session state
                    st.session_state['last_encoded_image'] = stego_image
    elif action == "Detect hidden message in the image":
        st.header("Detect Hidden Image (Key Required)")
        image_to_check = image
        if 'last_encoded_image' in st.session_state:
            option = st.radio(
                "Which image do you want to check for a hidden message?",
                ("Uploaded Image", "Last Encoded Image"),
                horizontal=True
            )
            if option == "Last Encoded Image":
                image_to_check = st.session_state['last_encoded_image']
        with st.form("key_form"):
            key_start_position = st.text_input("Start Position (row,col)", value="0,0")
            key_gap = st.text_input("Gap", value="0")
            key_channels = st.text_input("Channels (e.g. RGB, R, G, B, RG, etc.)", value="RGB")
            key_num_bits = st.text_input("Num Bits", value="1")
            key_delimiter_start = st.text_input("Delimiter Start", value="#")
            key_delimiter_end = st.text_input("Delimiter End", value="#")
            key_horizontal = st.selectbox("Horizontal (1=row-wise, 0=column-wise)", [1, 0], index=0)
            submitted = st.form_submit_button("Check for Hidden Image")
        if submitted:
            try:
                row, col = [int(x.strip()) for x in key_start_position.split(",")]
                gap = int(key_gap)
                channels = key_channels.strip().upper()
                num_bits = int(key_num_bits)
                delimiter_start = key_delimiter_start
                delimiter_end = key_delimiter_end
                horizontal = int(key_horizontal)
                key_params = {
                    'start_position': (row, col),
                    'gap': gap,
                    'channels': channels,
                    'num_bits': num_bits,
                    'delimiter_start': delimiter_start,
                    'delimiter_end': delimiter_end,
                    'horizontal': horizontal
                }
                found, msg = detect_hidden_message(image_to_check, key_params)
                if found:
                    st.success("A hidden message/image was detected with the provided key!")
                    st.write("Decoded message:")
                    st.code(msg)
                else:
                    st.info("No hidden message/image detected with the provided key.")
            except Exception as e:
                st.error(f"Error using provided key: {e}")
