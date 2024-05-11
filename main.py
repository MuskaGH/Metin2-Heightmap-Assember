import os
from utility import utility

def main():
    map_folder_name = input("Enter the name of the Metin2's map folder: ")

    if not os.path.exists(map_folder_name):
        print("The specified folder does not exist. Make sure the folder is in the same directory as this script and try again.")
    else:
        if utility.generate_complete_heightmap(map_folder_name):
            print("The heightmap has been generated successfully! Check the script's directory for the 'generated_heightmap.png' file.")

            print()

            print("Details:")
            print(" - Format: Grayscale, 16-bit integer")
            print(" - Color Space: sRGB")
        else:
            print("Failed to generate the heightmap. Make sure the folder contains the necessary height.raw files and is consistent with Metin2's map folder structure.")

    input("Press Enter to exit...")

if __name__ == "__main__":
    main()