import cv2
import numpy as np
from PIL import Image
import easyocr
import os

# Initialize the EasyOCR reader
reader = easyocr.Reader(['en'])

# Define the directory containing the tiles and vertical masks
tile_directory = '/home/usama/Home_data/vertical_bbox_reterival_4_oct_2024/Data_for_pixel_transformation/'  # Update the path as necessary
output_directory = '/home/usama/Home_data/vertical_bbox_reterival_4_oct_2024/output/'  # Update the path as necessary

# Get a list of tile filenames and corresponding mask filenames
tiles = [f for f in os.listdir(tile_directory) if f.endswith('.jpg') and 'vertical_mask' not in f]

for tile_file in tiles:
    # Derive the mask filename based on the tile filename
    tile_path = os.path.join(tile_directory, tile_file)
    mask_filename = tile_file.replace('.jpg', '_vertical_mask.jpg')
    mask_path = os.path.join(tile_directory, mask_filename)

    # Check if the mask file exists
    if not os.path.exists(mask_path):
        print(f"Mask for {tile_file} not found. Skipping...")
        continue

    # Step 1: Load the original tile and mask image containing tilted bounding boxes
    tile = cv2.imread(tile_path)
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

    # Create a blank image with the same dimensions as the original tile
    blank_image = np.zeros_like(tile)

    # Step 2: Find contours of the bounding boxes in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Step 3: Loop over each bounding box to extract, rotate, and place it on the blank image
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)  # Get bounding box coordinates

        # Extract the ROI corresponding to the bounding box
        roi = tile[y:y+h, x:x+w]

        # Convert to BGR if not already
        if len(roi.shape) == 2:
            roi = cv2.cvtColor(roi, cv2.COLOR_GRAY2BGR)

        # Convert the ROI to RGB for processing
        roi_pil = Image.fromarray(cv2.cvtColor(roi, cv2.COLOR_BGR2RGB))

        # Rotate the ROI (adjust the angle as needed)
        rotated_roi = roi_pil.rotate(270, expand=True)

        # Convert the rotated ROI back to OpenCV format (BGR)
        rotated_roi_bgr = cv2.cvtColor(np.array(rotated_roi), cv2.COLOR_RGB2BGR)

        # Calculate the center of the original bounding box
        center_x, center_y = x + w // 2, y + h // 2

        # Calculate the size of the rotated ROI
        rotated_h, rotated_w = rotated_roi_bgr.shape[:2]

        # Determine the top-left corner to place the rotated ROI on the blank image
        top_left_x = center_x - rotated_w // 2
        top_left_y = center_y - rotated_h // 2

        # Make sure we are within the image boundaries before placing the ROI
        if top_left_x >= 0 and top_left_y >= 0 and top_left_x + rotated_w <= blank_image.shape[1] and top_left_y + rotated_h <= blank_image.shape[0]:
            blank_image[top_left_y:top_left_y+rotated_h, top_left_x:top_left_x+rotated_w] = rotated_roi_bgr

    # Step 4: Save the final image with all rotated bounding boxes placed on the blank image
    rotated_bboxes_filename = f"rotated_bboxes_on_blank_{tile_file}"
    rotated_bboxes_path = os.path.join(output_directory, rotated_bboxes_filename)
    cv2.imwrite(rotated_bboxes_path, blank_image)

    # Step 5: Convert the blank image to RGB for OCR
    blank_image_rgb = cv2.cvtColor(blank_image, cv2.COLOR_BGR2RGB)

    # Step 6: Apply EasyOCR to the blank image containing rotated bounding boxes
    ocr_results = reader.readtext(blank_image_rgb)

    # Step 7: Draw the detected bounding boxes and annotate the text on the blank image
    for (bbox, text, prob) in ocr_results:
        with open("/home/usama/Amberley-Ohio.txt","a") as file:
            file.write(text + '\n')
        # Extract the bounding box coordinates
        top_left = tuple(map(int, bbox[0]))
        bottom_right = tuple(map(int, bbox[2]))

        # Draw the bounding box on the blank image
        cv2.rectangle(blank_image, top_left, bottom_right, (0, 255, 0), 2)

        # Annotate the detected text on the blank image
        cv2.putText(blank_image, text, (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Step 8: Save the final annotated image with OCR results
    annotated_image_filename = f"ocr_rotated_bboxes_annotated_{tile_file}"
    annotated_image_path = os.path.join(output_directory, annotated_image_filename)
    cv2.imwrite(annotated_image_path, blank_image)

    print(f"Processing complete for {tile_file}. Annotated image saved as '{annotated_image_filename}'.")
