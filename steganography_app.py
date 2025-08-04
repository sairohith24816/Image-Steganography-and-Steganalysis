import streamlit as st
from PIL import Image
import numpy as np
import io
import uuid
import input_generator
from encode_decode import decode_message, encode_message

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
                # Generate a unique key for this encoding
                key = str(uuid.uuid4())[:8]
                
                # Update parameters with message and key
                params.update({
                    'message': user_message,
                    'key': key
                })
                
                # Encode the image
                stego_image = encode_image(image, user_message, params)
                if stego_image is None:
                    st.error("Encoding failed. Please try with a different message or image.")
                else:
                    st.image(stego_image, caption="Steganographed Image", use_container_width=True)
                    st.subheader("Your Secret Key:")
                    st.code(key, language="text")
                    st.info("Keep this key safe! You'll need it to decode the message later.")
                    st.subheader("Parameters Used (for manual decoding):")
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
                    # Store the last encoded image and parameters in session state
                    st.session_state['last_encoded_image'] = stego_image
                    st.session_state['last_params'] = params
    elif action == "Detect hidden message in the image":
        st.header("Detect Hidden Message")
        image_to_check = image
        
        # Initialize default parameters
        current_params = {
            'start_position': (0, 0),
            'gap': 0,
            'channels': 'RGB',
            'num_bits': 1,
            'delimiter_start': '#',
            'delimiter_end': '#',
            'horizontal': 1
        }
        
        # Initialize option with default value
        option = "Uploaded Image"
        
        # Option to select image source
        if 'last_encoded_image' in st.session_state:
            option = st.radio(
                "Which image do you want to check for a hidden message?",
                ("Uploaded Image", "Last Encoded Image"),
                horizontal=True,
                key='image_selection'
            )
            
            if option == "Last Encoded Image":
                image_to_check = st.session_state['last_encoded_image']
                if 'last_params' in st.session_state:
                    current_params = st.session_state['last_params'].copy()
                    st.info("Using parameters from last encoded image. You can modify them below if needed.")
        
        # Create two columns for key and manual input
        key_col, manual_col = st.columns(2)
        
        with key_col:
            st.subheader("Decode with Key")
            # Pre-fill the key if we're using the last encoded image and have last_params
            default_key = ''
            if option == "Last Encoded Image" and 'last_params' in st.session_state:
                default_key = st.session_state['last_params'].get('key', '')
            key = st.text_input("Enter your secret key:", value=default_key)
            decode_with_key = st.button("Decode using Key")
            
            if decode_with_key:
                if not key:
                    st.warning("Please enter a secret key")
                else:
                    found = False
                    # Only check last_params if we're looking at the last encoded image
                    if option == "Last Encoded Image" and 'last_params' in st.session_state:
                        if st.session_state['last_params'].get('key') == key:
                            found, msg = detect_hidden_message(image_to_check, st.session_state['last_params'])
                            if found:
                                st.success("Message successfully decoded!")
                                st.write(f"Hidden message: {msg}")
                    
                    if not found:
                        st.error("Invalid key or no message found. Try manual parameters.")
        
        with manual_col:
            st.subheader("Decode with Manual Parameters")
            with st.form("manual_params_form"):
                row, col = current_params['start_position']
                key_start_position = st.text_input("Start Position (row,col)", value=f"{row},{col}")
                key_gap = st.number_input("Gap", min_value=0, value=current_params['gap'])
                key_channels = st.text_input("Channels (RGB, R, G, B, RG, etc.)", value=current_params['channels'])
                key_num_bits = st.number_input("Number of Bits", min_value=1, max_value=8, value=current_params['num_bits'])
                delim_idx = next((i for i, x in enumerate(delimiter_options) if x[0] == current_params['delimiter_start'] and x[1] == current_params['delimiter_end']), 0)
                delim_choice = st.selectbox("Choose Delimiters", delimiter_options, index=delim_idx)
                key_horizontal = st.selectbox("Traversal Direction", ["Horizontal", "Vertical"], index=0 if current_params['horizontal'] else 1)
                
                submitted = st.form_submit_button("Decode with Parameters")
            
            if submitted:
                try:
                    row, col = [int(x.strip()) for x in key_start_position.split(",")]
                    channels = key_channels.strip().upper()
                    delimiter_start, delimiter_end = delim_choice
                    horizontal = key_horizontal == "Horizontal"
                    
                    manual_params = {
                        'start_position': (row, col),
                        'gap': key_gap,
                        'channels': channels,
                        'num_bits': key_num_bits,
                        'delimiter_start': delimiter_start,
                        'delimiter_end': delimiter_end,
                        'horizontal': horizontal
                    }
                    
                    found, msg = detect_hidden_message(image_to_check, manual_params)
                    
                    if found:
                        st.success("Hidden message found!")
                        st.write(f"Message: {msg}")
                        st.subheader("Parameters Used:")
                        st.json(manual_params)
                    else:
                        st.error("No valid message found with these parameters. Try different parameters.")
                        
                except ValueError as ve:
                    st.error(f"Invalid input: Please check your parameters. {str(ve)}")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")