"""
This function reads 3D image files (in .tif or .nrrd format) from the input directory,
crops them using the `crop_3d_image_with_margin` function, and saves the cropped images 
to the output directory. The images are processed one by one, and errors during processing 
are reported.

It expects that the input directory and output directory paths are specified and 
that the output directory will be created if it does not exist.
"""


import numpy as np
import nrrd
import os

def crop_3d_image_with_margin(img, margin=50):
    """
    Crop a 3D numpy image to remove all-zero planes from all six sides,
    but leave a margin of specified number of pixels.
    
    :param img: 3D numpy array representing the image.
    :param margin: Number of pixels to leave as margin after cropping.
    :return: Cropped 3D numpy array.
    """
    # Find the indices of the first and last non-zero elements along each axis
    non_zero_coords = np.argwhere(img)
    x_min, y_min, z_min = non_zero_coords.min(axis=0)
    x_max, y_max, z_max = non_zero_coords.max(axis=0) + 1  # +1 for inclusive slicing

    # Add margin and ensure indices are within the image bounds
    x_min = max(x_min - margin, 0)
    y_min = max(y_min - margin, 0)
    z_min = max(z_min - margin, 0)
    x_max = min(x_max + margin, img.shape[0])
    y_max = min(y_max + margin, img.shape[1])
    z_max = min(z_max + margin, img.shape[2])

    # Crop the image
    cropped_img = img[x_min:x_max, y_min:y_max, z_min:z_max]

    return cropped_img

def main():
    # Define input and output directories
    input_directory = '/path/to/input_directory/'  # Update this path
    output_directory = '/path/to/output_directory/'  # Update this path

    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)
    
    # List all files in the input directory
    files = [f for f in os.listdir(input_directory) if f.endswith('.tif') or f.endswith('.nrrd')]
    
    for filename in files:
        try:
            # Load the image
            img, header = nrrd.read(os.path.join(input_directory, filename))

            # Crop the image with margin
            cropped_img = crop_3d_image_with_margin(img)

            # Save the cropped image
            output_file_path = os.path.join(output_directory, filename)
            nrrd.write(output_file_path, cropped_img, header)
            
            print(f"Processed and saved: {filename}")
        
        except Exception as e:
            print(f"Error processing file {filename}: {e}")

if __name__ == "__main__":
    main()
