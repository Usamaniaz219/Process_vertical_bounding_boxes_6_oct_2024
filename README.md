# Vertical Bounding Box Retrieval

## Overview
`vertical_bbox_reterival.py` is a Python script designed to detect and process vertical or tilted text bounding boxes in images. It utilizes OpenCV for image processing and EasyOCR for text detection. The script divides images into tiles, applies OCR, and extracts vertical bounding boxes, generating corresponding masks.

## Features
- Loads and processes images from a specified directory.
- Divides images into overlapping tiles for better text detection.
- Applies EasyOCR to detect text in each tile.
- Identifies vertical or tilted bounding boxes and creates masks.
- Saves processed images and masks for further analysis.

## Requirements
Ensure you have the following dependencies installed:
```bash
pip install opencv-python numpy easyocr
```
Additionally, GPU acceleration is recommended for EasyOCR.

## Usage
### 1. Place images in a directory
Ensure your images are stored in a directory before running the script.

### 2. Run the script
```bash
python vertical_bbox_reterival.py
```
By default, the script processes images in a specified directory and saves results in an output directory.

## Key Functions
### `load_image(image_path)`
Loads an image from the given path.

### `is_horizontal(bbox)`
Determines whether a bounding box is horizontal based on width and height.

### `draw_and_fill_vertical_boxes(bboxes, mask_shape)`
Creates a mask highlighting vertical or tilted bounding boxes.

### `extract_and_save_tiles(image, tile_width, tile_height, overlap, output_dir)`
Divides the image into overlapping tiles and saves them.

### `apply_ocr_on_tiles(tile_paths, reader, output_dir)`
Applies EasyOCR to detect text and annotate bounding boxes on each tile.

### `process_images(directory_path, tile_width=2450, tile_height=2450, overlap=1000)`
Main function that processes all images in the specified directory.

## Output
- Processed images with detected text.
- Masks highlighting vertical bounding boxes.
- Extracted tiles saved for further processing.

## License
This project is open-source and can be modified as needed.


