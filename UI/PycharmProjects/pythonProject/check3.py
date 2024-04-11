import streamlit as st
from PIL import Image
import os
import subprocess

def load_image_from_folder(folder_path, image_name):
    image_path = os.path.join(folder_path, image_name)
    return Image.open(image_path)

def main():

    st.title("Image Viewer and Model Runner")

    # Define the paths to the folders containing your images
    folder1_path = 'C:/Users/Kaustubha/OneDrive/Desktop/ChangeFormer/samples_LEVIR/A'
    folder2_path = 'C:/Users/Kaustubha/OneDrive/Desktop/ChangeFormer/samples_LEVIR/B'
    folder3_path = 'C:/Users/Kaustubha/OneDrive/Desktop/ChangeFormer/samples_LEVIR/predict_CD_ChangeFormerV6'

    # Initialize variables to store images and model status
    if "image_index" not in st.session_state:
        st.session_state.image_index = 0

    if "model_running" not in st.session_state:
        st.session_state.model_running = False

    image_names = ["test_2_0000_0000.png", "test_2_0000_0512.png", "test_7_0256_0512.png", "test_55_0256_0000.png", "test_77_0512_0256.png", "test_102_0512_0000.png", "test_121_0768_0256.png"]

    before_image = None
    after_image = None
    difference_image = None
    image_name = image_names[st.session_state.image_index]

    # Create columns for better layout
    col1, col2, col3, col4, col5 = st.columns(5)

    # Button to load image from folder1
    if col1.button("BEFORE"):
        before_image = load_image_from_folder(folder1_path, image_name)

    # Button to load image from folder2 with the same name as the first one
    if col2.button("AFTER"):
        after_image = load_image_from_folder(folder2_path, image_name)

    # Button to load image from folder3 with the same name as the first one
    if col3.button("CHANGE"):
        difference_image = load_image_from_folder(folder3_path, image_name)

    # Button to load the next image
    if col4.button("NEXT"):
        st.session_state.image_index = (st.session_state.image_index + 1) % len(image_names)
        image_name = image_names[st.session_state.image_index]
        before_image = load_image_from_folder(folder1_path, image_name)
        after_image = load_image_from_folder(folder2_path, image_name)
        difference_image = load_image_from_folder(folder3_path, image_name)

    if col5.button("RUN MODEL"):
        # st.session_state.model_running = True  # Set the flag to indicate the model is running
        # st.write("Activating conda environment...")
        # st.session_state.model_running = True  # Set running flag
        # os.system("conda activate project")
        # os.chdir("C:/Users/Kaustubha/OneDrive/Desktop/ChangeFormer")
        st.write("Running the model...")
        os.system("python demo_LEVIR.py --img_size 128")
        # st.session_state.model_running = False

    # Display images
    if before_image is not None:
        st.image(before_image, caption="Before Image", use_column_width=True)

    if after_image is not None:
        st.image(after_image, caption="After Image", use_column_width=True)

    if difference_image is not None:
        st.image(difference_image, caption="Difference Image", use_column_width=True)






if __name__ == "__main__":
    main()
