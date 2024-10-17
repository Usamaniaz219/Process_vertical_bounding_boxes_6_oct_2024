import cv2
import numpy as np
import os
import math
import easyocr

# Load an image from a file
def load_image(image_path):
    return cv2.imread(image_path)


def is_horizontal(bbox):                               # Check if a bounding box is horizontal
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = bbox
    width = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)  
    height = math.sqrt((x4 - x1) ** 2 + (y4 - y1) ** 2)  
    return width > height


# Draw and fill vertical or tilted bounding boxes
def draw_and_fill_vertical_boxes(bboxes, mask_shape):
    mask = np.zeros(mask_shape, dtype=np.uint8)
    for bbox in bboxes:
        if not is_horizontal(bbox):
            bbox_array = np.array(bbox, dtype=np.int32)
            cv2.fillPoly(mask, [bbox_array], color=255)
    return mask

# Extract tiles from the image and save them individually
def extract_and_save_tiles(image, tile_width, tile_height, overlap, output_dir):
    tile_paths = []
    tile_count = 0

    for start_y in range(0, image.shape[0], tile_height - overlap):
        for start_x in range(0, image.shape[1], tile_width - overlap):
            end_x = min(start_x + tile_width, image.shape[1])
            end_y = min(start_y + tile_height, image.shape[0])
            tile = image[start_y:end_y, start_x:end_x]

            # if tile.shape[0] == tile_height and tile.shape[1] == tile_width:
            tile_filename = f"tile_{tile_count}.jpg"
            tile_path = os.path.join(output_dir, tile_filename)
            cv2.imwrite(tile_path, tile)
            tile_paths.append(tile_path)
            tile_count += 1

    return tile_paths

# Apply EasyOCR on each saved tile and save the annotated results
def apply_ocr_on_tiles(tile_paths, reader, output_dir):
    for i, tile_path in enumerate(tile_paths):
        tile = cv2.imread(tile_path)
        if tile is None:
            print(f"Failed to load tile: {tile_path}")
            continue

        result = reader.readtext(tile, width_ths=0.65)
        if result:
            mask_shape = tile.shape[:2]
            vertical_boxes = []

            for bbox, text, _ in result:
                try:
                    [[x1, y1], [x2, y2], [x3, y3], [x4, y4]] = bbox
                except ValueError:
                    continue

                mapped_bbox = np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]], dtype=np.int32).reshape((-1, 1, 2))
                cv2.polylines(tile, [mapped_bbox], isClosed=True, color=(0, 255, 0), thickness=2)
                cv2.putText(tile, text, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2, cv2.LINE_AA)

                # Collect vertical or tilted boxes for further processing
                if not is_horizontal(bbox):
                    vertical_boxes.append(bbox)

            # Draw and fill vertical/tilted boxes on the mask
            if vertical_boxes:
                mask = draw_and_fill_vertical_boxes(vertical_boxes, mask_shape)
                mask_path = os.path.join(output_dir, f"tile_{i}_vertical_mask.jpg")
                cv2.imwrite(mask_path, mask)

        processed_tile_path = os.path.join(output_dir, f"tile_{i}_processed.jpg")
        cv2.imwrite(processed_tile_path, tile)

# Process images by extracting tiles, saving them, and applying EasyOCR
def process_images(directory_path, tile_width=2450, tile_height=2450, overlap=1000):
    reader = easyocr.Reader(['en'], gpu=True)
    for filename in os.listdir(directory_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(directory_path, filename)
            print(f"Processing image: {image_path}")
            image = load_image(image_path)

            if image is not None:
                image_output_dir = os.path.join('/home/usama/Home_data/vertical_bbox_reterival_4_oct_2024/vertical_bbox_reterival_results/', os.path.splitext(filename)[0])
                os.makedirs(image_output_dir, exist_ok=True)

                tile_paths = extract_and_save_tiles(image, tile_width, tile_height, overlap, image_output_dir)
                apply_ocr_on_tiles(tile_paths, reader, image_output_dir)
            else:
                print(f"Failed to read {image_path}")

# Example usage
image_directory = '/home/usama/input_2_oct_2024/'
process_images(image_directory)
