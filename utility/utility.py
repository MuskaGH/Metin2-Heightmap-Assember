import os
import cv2
import numpy
import time

# Display my personal banner at the start of the program ^_^
def display_startup_banner():
    print("""
    █████████████████████████████████████████████████████████████████████████████████████████████████████████████████
          
        ███    ███  █████  ██████  ███████     ██████  ██    ██     ███    ███ ██    ██ ███████ ██   ██  █████  
        ████  ████ ██   ██ ██   ██ ██          ██   ██  ██  ██      ████  ████ ██    ██ ██      ██  ██  ██   ██ 
        ██ ████ ██ ███████ ██   ██ █████       ██████    ████       ██ ████ ██ ██    ██ ███████ █████   ███████ 
        ██  ██  ██ ██   ██ ██   ██ ██          ██   ██    ██        ██  ██  ██ ██    ██      ██ ██  ██  ██   ██ 
        ██      ██ ██   ██ ██████  ███████     ██████     ██        ██      ██  ██████  ███████ ██   ██ ██   ██
          
    █████████████████████████████████████████████████████████████████████████████████████████████████████████████████
          
--------------------------------------------------------------
Welcome to Metin2 Heightmap Assembler! I'm happy you decided to use my software! ^_^
If you encounter any issues or have suggestions for improvements, feel free to contact me!
          
Discord: muskadev
Twitter: @Muska_Dev
Website: www.martinmusil.com
--------------------------------------------------------------
          """)

# Converts the RAW heightmap files to Grayscale, 16-bit, PNG format
def convert_to_correct_format(map_folder):
    sub_heightmap_height = 131 
    sub_heightmap_width = 131

    # Loop through the subfolders and convert the height.raw files to PNG
    for subdir, dirs, files in os.walk(map_folder):
        for file in files:
            if file == 'height.raw':
                raw_path = os.path.join(subdir, file)
                with open(raw_path, "rb") as rawimg:
                    img = numpy.fromfile(rawimg, dtype=numpy.uint16, count=sub_heightmap_width * sub_heightmap_height).reshape(sub_heightmap_height, sub_heightmap_width)
                    
                    cropped_img = img[3:131, 3:131] # Crop the image to remove the padding
                    
                    output_path = os.path.join(subdir, 'sub_heightmap.png')
                    cv2.imwrite(output_path, cropped_img, [cv2.IMWRITE_PNG_COMPRESSION, 0, cv2.IMWRITE_PNG_BILEVEL, 1]) # Save the image as a 16-bit PNG

# Calculate the dimensions of the grid based on the subfolders structure
def calculate_grid_dimensions(map_folder):
    columns = set()
    rows = set()

    # Loop through the subfolders and extract the column and row indices
    for subdir, _, files in os.walk(map_folder):
        dir_name = os.path.basename(subdir)
        if dir_name.isdigit() and len(dir_name) >= 6:
            col_index = int(dir_name[:3])
            row_index = int(dir_name[3:])
            columns.add(col_index)
            rows.add(row_index)

    return max(columns) + 1, max(rows) + 1 # Return the number of columns and rows

# Find the closest recommended size to achieve a 1:1 resolution ratio
def find_closest_recommended_size(width, height):
    recommended_sizes = [127, 253, 505, 1009, 2017, 4033, 8129]
    max_dimension = max(width, height)
    closest_size = min(recommended_sizes, key=lambda x: x if x >= max_dimension else float('inf')) # Find the closest recommended size
    print()
    print(f"Original max dimension: {max_dimension}, Closest recommended size detected to create 1:1 ratio: {closest_size}")
    time.sleep(1.5)
    print()
    print(f"Padding to {closest_size}x{closest_size}...")
    time.sleep(2)

    return closest_size

# Pad the heightmap to achieve a 1:1 resolution ratio
def pad_to_recommended_size(heightmap):
    current_height, current_width = heightmap.shape[:2]
    target_size = find_closest_recommended_size(current_width, current_height)
    top_pad = (target_size - current_height) // 2
    bottom_pad = target_size - current_height - top_pad
    left_pad = (target_size - current_width) // 2
    right_pad = target_size - current_width - left_pad
    padded_image = cv2.copyMakeBorder(heightmap, top_pad, bottom_pad, left_pad, right_pad, cv2.BORDER_CONSTANT, value=[0, 0, 0]) # Pad the image with black pixels

    return padded_image

# Generate the complete heightmap by combining the sub-heightmaps
def generate_complete_heightmap(map_folder, add_padding=False):
    convert_to_correct_format(map_folder) # Convert the RAW files to PNG
    num_cols, num_rows = calculate_grid_dimensions(map_folder)

    grid_image = []

    # Loop through the subfolders and concatenate the sub-heightmaps
    for row in range(num_rows):
        row_images = []
        for col in range(num_cols):
            path = os.path.join(map_folder, f'{col:03d}{row:03d}', 'sub_heightmap.png') # Path to the sub-heightmap
            if os.path.exists(path):
                img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
                if img is not None:
                    row_images.append(img) # Append the sub-heightmap to the row_images list
        
        if row_images: # If the row_images list is not empty, concatenate the sub-heightmaps
            concatenated_row = cv2.hconcat(row_images)
            grid_image.append(concatenated_row)

    if grid_image: # If the grid_image list is not empty, concatenate the rows
        final_heightmap = cv2.vconcat(grid_image)
        if add_padding: # If the user wants to add padding, pad the heightmap
            final_heightmap = pad_to_recommended_size(final_heightmap)
        
        print()
        print("Generating the final heightmap...")
        time.sleep(1.5)

        script_directory = os.getcwd() # Get the current working directory
        final_path = os.path.join(script_directory, 'generated_heightmap.png') # Path to the final heightmap
        cv2.imwrite(final_path, final_heightmap, [cv2.IMWRITE_PNG_COMPRESSION, 0]) # Save the final heightmap as a PNG
        return True # Return True if the heightmap was generated successfully
    
    return False # Return False if the heightmap generation failed