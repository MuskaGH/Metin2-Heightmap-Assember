import os
import cv2
import numpy as np

def convert_to_correct_format(map_folder):
    sub_heightmap_height = 131
    sub_heightmap_width = 131

    for subdir, dirs, files in os.walk(map_folder):
        for file in files:
            if file == 'height.raw':
                raw_path = os.path.join(subdir, file)
                with open(raw_path, "rb") as rawimg:
                    img = np.fromfile(rawimg, dtype=np.uint16, count=sub_heightmap_width * sub_heightmap_height).reshape(sub_heightmap_height, sub_heightmap_width)
                    
                    cropped_img = img[3:131, 3:131]
                    
                    output_path = os.path.join(subdir, 'sub_heightmap.png')
                    cv2.imwrite(output_path, cropped_img, [cv2.IMWRITE_PNG_COMPRESSION, 0, cv2.IMWRITE_PNG_BILEVEL, 1])

def calculate_grid_dimensions(map_folder):
    columns = set()
    rows = set()

    for subdir, _, files in os.walk(map_folder):
        dir_name = os.path.basename(subdir)
        if dir_name.isdigit() and len(dir_name) >= 6:
            col_index = int(dir_name[:3])
            row_index = int(dir_name[3:])
            columns.add(col_index)
            rows.add(row_index)

    return max(columns) + 1, max(rows) + 1

def generate_complete_heightmap(map_folder):
    convert_to_correct_format(map_folder)
    num_cols, num_rows = calculate_grid_dimensions(map_folder)

    grid_image = []

    for row in range(num_rows):
        row_images = []
        for col in range(num_cols):
            path = os.path.join(map_folder, f'{col:03d}{row:03d}', 'sub_heightmap.png')
            if os.path.exists(path):
                img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
                if img is not None:
                    row_images.append(img)
        
        if row_images:
            concatenated_row = cv2.hconcat(row_images)
            grid_image.append(concatenated_row)

    if grid_image:
        final_heightmap = cv2.vconcat(grid_image)
        script_directory = os.getcwd()
        final_path = os.path.join(script_directory, 'generated_heightmap.png')
        cv2.imwrite(final_path, final_heightmap, [cv2.IMWRITE_PNG_COMPRESSION, 0])
        return True
    
    return False