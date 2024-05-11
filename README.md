# Metin2 Heightmap Assembler

## Overview
Python tool designed to process and convert Metin2 game map files into a unified heightmap in 16-bit grayscale PNG format. This tool is great for people looking to integrate Metin2 maps into different game engines or any other applications that require complete heightmap for the terrain.

## Features
- **Converts RAW heightmap files** to 16-bit Grayscale PNG images.
- **Automatically calculates the grid dimensions** of the map from the subfolder structure.
- **Combines individual sub-heightmaps** according to the map's grid layout to form a complete heightmap.
- **Optional padding**: Adds padding to the heightmap to achieve a 1:1 aspect ratio, automatically selecting the closest recommended resolution to ensure optimal compatibility with game engines like Unreal Engine.

## Prerequisites
- Python 3.6 or higher
- OpenCV library for Python (`cv2`)
- Numpy library

## How to Use
To use the tool, you need to have a folder which contains the original Metin2's map files. Keep in mind that it should be located within this script's root directory.

### Main File (`main.py`)
This file acts as the entry point for the tool. It handles user inputs and initiates the heightmap generation process.

## How to Run
You can simply double-click on the `main.py` file or navigate to the script directory in your command line interface and execute the following command:
`python main.py`

You will be prompted to enter the name of the Metin2 map folder and whether you want to add padding to achieve a 1:1 ratio. The script will then process the heightmaps and output a single file named 'generated_heightmap.png' in the script's directory.
