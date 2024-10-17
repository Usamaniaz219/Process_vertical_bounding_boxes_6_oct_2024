

import os
import shutil
import re

# Directories for source and destination
source_dir = '/home/usama/Home_data/vertical_bbox_reterival_4_oct_2024/vertical_bbox_reterival_results/Amberley-Ohio/'  # Set your source directory path here
destination_dir = '/home/usama/Home_data/vertical_bbox_reterival_4_oct_2024/Data_for_pixel_transformation/'  # Set your destination directory path here

# Create destination directory if it doesn't exist
if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)

# Regular expression to match filenames like "tile_<number>.<extension>" and "tile_<number>_vertical_mask.<extension>"
pattern_tile = re.compile(r"^tile_(\d+)\.(jpg|png|jpeg|bmp|tiff)$")
pattern_mask = re.compile(r"^tile_(\d+)_vertical_mask\.(jpg|png|jpeg|bmp|tiff)$")

# Dictionary to store matching files by their number
tile_files = {}

# Iterate through files in the source directory
for filename in os.listdir(source_dir):
    tile_match = pattern_tile.match(filename)
    mask_match = pattern_mask.match(filename)
    
    if tile_match:
        number = tile_match.group(1)  # Extract the number part (e.g., '0' in 'tile_0')
        tile_files[number] = {'tile': filename, 'mask': tile_files.get(number, {}).get('mask')}
    
    elif mask_match:
        number = mask_match.group(1)  # Extract the number part (e.g., '0' in 'tile_0_vertical_mask')
        tile_files[number] = {'mask': filename, 'tile': tile_files.get(number, {}).get('tile')}

# Now move both tile and mask if both exist for the same number
for number, files in tile_files.items():
    tile_filename = files.get('tile')
    mask_filename = files.get('mask')
    
    # Check if both the tile and corresponding vertical mask exist
    if tile_filename and mask_filename:
        # Move both files to the destination directory
        shutil.move(os.path.join(source_dir, tile_filename), os.path.join(destination_dir, tile_filename))
        shutil.move(os.path.join(source_dir, mask_filename), os.path.join(destination_dir, mask_filename))
        print(f"Moved: {tile_filename} and {mask_filename} to {destination_dir}")