import cv2
import numpy as np
import streamlit as st
import os

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
    # Convert bytes to numpy arrays
    np_img1 = np.frombuffer(img1.read(), np.uint8)
    np_img2 = np.frombuffer(img2.read(), np.uint8)

    # Decode the images using cv2.imdecode
    img1 = cv2.imdecode(np_img1, cv2.IMREAD_COLOR)
    img2 = cv2.imdecode(np_img2, cv2.IMREAD_COLOR)

    # Resize images to ensure they have the same dimensions
    img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    # Change white to red in Image 2
    img2 = change_white_to_red(img2)

    # Remove alpha channel if present
    img1 = remove_alpha_channel(img1)
    img2 = remove_alpha_channel(img2)

    # Overlay images with specified transparency
    blended = cv2.addWeighted(img1, 1 - alpha, img2, alpha, 0)

    return blended

# Streamlit app
st.title("Image Overlay App")

# Upload images
image1 = st.file_uploader("Upload Image 1", type=["jpg", "jpeg", "png"])
image2 = st.file_uploader("Upload Image 2", type=["jpg", "jpeg", "png"])

# Transparency slider
transparency_slider = st.slider("Adjust Transparency", min_value=0.0, max_value=1.0, value=0.2, step=0.01)

# Create a layout with two columns
col1, col2 = st.columns(2)

# Button to overlay images in the first column
with col1:
    if st.button("Overlay Images"):
        try:
            # Perform image overlay
            if image1 and image2:
                overlayed_image = overlay_images(image1, image2, transparency_slider)
                st.image(overlayed_image, caption="Overlayed Image", use_column_width=True)

        except Exception as e:
            st.error(f"Error: {str(e)}")

# Button to save the output image in the second column
with col2:
    if st.button("Save Image"):
        try:
            if image1 and image2:
                # Specify the output folder
                output_folder = "C:/Users/Kaustubha/OneDrive/Desktop/ChangeFormer/UI"

                # Perform image overlay
                overlayed_image = overlay_images(image1, image2, transparency_slider)

                # Save the output image
                output_path = os.path.join(output_folder, "output_image.png")
                cv2.imwrite(output_path, cv2.cvtColor(overlayed_image, cv2.COLOR_RGBA2BGR))

                st.success(f"Image saved successfully! Output saved to {output_path}")

        except Exception as e:
            st.error(f"Error: {str(e)}")
