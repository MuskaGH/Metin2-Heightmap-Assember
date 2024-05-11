import os
from utility import utility

def main():
    utility.display_startup_banner() # Display the startup banner
    
    map_folder_name = input("Enter the name of the Metin2's map folder: ") # Example: "metin2_map_a1"
    pad_option = input("Do you wish to add additional padding to achieve a 1:1 resolution ratio? (YES/NO): ").lower()
    add_padding = pad_option == 'yes' # Convert the user's input to a boolean

    if not os.path.exists(map_folder_name): # Check if the specified folder exists
        print("The specified folder does not exist. Make sure the folder is in the same directory as this script and try again.")
    else: # Generate the complete heightmap
        if utility.generate_complete_heightmap(map_folder_name, add_padding): # Check if the heightmap was generated successfully
            print()
            print("The heightmap has been generated successfully! Check the script's directory for the 'generated_heightmap.png' file.")
            print()
            print("Specific Details:")
            print(" - Format: Grayscale, 16-bit integer")
            print(" - Color Space: sRGB")
            print(" - Appropriate padding applied to generate 1:1 resolution ratio" if pad_option == "yes" else " - Original dimensions preserved, no padding applied")
        else: # Display an error message if the heightmap generation failed
            print("Failed to generate the heightmap. Make sure the folder contains the necessary height.raw files and is consistent with Metin2's map folder structure.")

    print()
    input("Press Enter to exit...") # Wait for the user to press Enter before closing the program

if __name__ == "__main__":
    main()