import streamlit as st
from PIL import Image
import os
import cv2
import numpy as np
import subprocess


def remove_alpha_channel(image):
    # If the image has an alpha channel, remove it
    if image.shape[2] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
    return image


def change_white_to_red(img):
    # Convert the image to BGR format
    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)

    # Define the white color range in BGR
    lower_white = np.array([200, 200, 200])
    upper_white = np.array([255, 255, 255])

    # Create a mask to identify white pixels
    white_mask = cv2.inRange(img_bgr, lower_white, upper_white)

    # Replace white pixels with red
    img_bgr[white_mask > 0] = [0, 0, 255]  # Red color for white pixels

    # Convert the image back to RGBA format
    img_rgba = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGBA)

    return img_rgba


def overlay_images(img1, img2, alpha):
    # Convert PIL Image to NumPy array
    np_img1 = np.array(img1)
    np_img2 = np.array(img2)

    # Resize images to ensure they have the same dimensions
    img2 = cv2.resize(np_img2, (np_img1.shape[1], np_img1.shape[0]))

    # Change white to red in Image 2
    img2 = change_white_to_red(img2)

    # Remove alpha channel if present
    img1 = remove_alpha_channel(np_img1)
    img2 = remove_alpha_channel(img2)

    # Overlay images with specified transparency
    blended = cv2.addWeighted(img1, 1 - alpha, img2, alpha, 0)

    return blended


def load_image_from_folder(folder_path, image_name):
    image_path = os.path.join(folder_path, image_name)
    return Image.open(image_path)


def main():
    st.title("Image Viewer and Model Runner")

    # Define the paths to the folders containing your images
    folder2_path = './samples_LEVIR/B'
    folder1_path = './samples_LEVIR/A'
    folder3_path = './samples_LEVIR/label'

    # Initialize variables to store images and model status
    if "image_index" not in st.session_state:
        st.session_state.image_index = 0

    if "model_running" not in st.session_state:
        st.session_state.model_running = False

    if "before_image" not in st.session_state:
        st.session_state.before_image = None

    if "after_image" not in st.session_state:
        st.session_state.after_image = None

    if "difference_image" not in st.session_state:
        st.session_state.difference_image = None

    image_names = ["test_2_0000_0000.png", "test_2_0000_0512.png", "test_7_0256_0512.png", "test_55_0256_0000.png", "test_77_0512_0256.png", "test_102_0512_0000.png", "test_121_0768_0256.png"]

    image_name = image_names[st.session_state.image_index]

    # Transparency slider
    transparency_slider = st.slider("Adjust Transparency", min_value=0.0, max_value=1.0, value=0.2, step=0.01)

    # Create columns for better layout
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    # Button to load image from folder1
    if col1.button("BEFORE"):
        st.session_state.before_image = load_image_from_folder(folder1_path, image_name)
        st.image(st.session_state.before_image, caption="Before Image")

    # Button to load image from folder2 with the same name as the first one
    if col2.button("AFTER"):
        st.session_state.after_image = load_image_from_folder(folder2_path, image_name)
        st.session_state.difference_image = load_image_from_folder(folder3_path, image_name)
        st.image(st.session_state.after_image, caption="After Image")
        st.image(st.session_state.difference_image, caption="Difference Image")

    # Button to load image from folder3 with the same name as the first one
    if col3.button("CHANGE"):
        try:
            # Perform image overlay
            if st.session_state.after_image and st.session_state.difference_image:
                overlayed_image = overlay_images(st.session_state.after_image, st.session_state.difference_image, transparency_slider)
                st.image(overlayed_image, caption="Overlayed Image")

        except Exception as e:
            st.error(f"Error: {str(e)}")

    # Button to save the output image
    if col4.button("SAVE"):
        try:
            if st.session_state.after_image and st.session_state.difference_image:
                # Specify the output folder
                output_folder = "./UI"

                # Perform image overlay
                overlayed_image = overlay_images(st.session_state.after_image, st.session_state.difference_image, transparency_slider)

                # Save the output image
                output_path = os.path.join(output_folder, "output_image.png")
                cv2.imwrite(output_path, cv2.cvtColor(overlayed_image, cv2.COLOR_RGBA2BGR))

                st.success(f"Image saved successfully! Output saved to {output_path}")

        except Exception as e:
            st.error(f"Error: {str(e)}")

    # Button to load the next image
    if col5.button("NEXT"):
        st.session_state.image_index = (st.session_state.image_index + 1) % len(image_names)
        image_name = image_names[st.session_state.image_index]
        st.session_state.before_image = load_image_from_folder(folder1_path, image_name)
        st.image(st.session_state.before_image, caption="Before Image")

    # Button to run the model
    if col6.button("RUN MODEL"):
        st.write("Running the model...")
        subprocess.run(["python", "demo_LEVIR.py", "--img_size", "128"])
        st.write("Successful!!")

    # Display images
    # if st.session_state.before_image is not None:
    #     st.image(st.session_state.before_image, caption="Before Image", use_column_width=True)
    #
    # if st.session_state.after_image is not None:
    #     st.image(st.session_state.after_image, caption="After Image", use_column_width=True)
    #
    # if st.session_state.difference_image is not None:
    #     st.image(st.session_state.difference_image, caption="Difference Image", use_column_width=True)


if __name__ == "__main__":
    main()
