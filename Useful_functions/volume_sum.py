"""
This script processes .nrrd files located in a specified folder. For each file, it loads the data from the .nrrd file and filters out zero values.
A threshold is then calculated based on the specified percentile of the non-zero data.
The script counts the number of voxels that exceed this threshold and converts this count into cubic millimeters using the provided voxel size.
Finally, the results are appended to a CSV file.
"""


import os
import numpy as np
import nrrd
import pandas as pd
from tqdm import tqdm

def process_nrrd_files(folder_path, output_csv="your_csv_name_here.csv", voxel_size_um=(2.68, 2.68, 2.68), percentile=30):
    """
    Processes .nrrd files in the specified folder, applies a threshold based on the specified percentile, 
    and saves the volume of voxels above the threshold to a CSV file.

    Parameters:
        folder_path (str): Path to the folder containing .nrrd files.
        output_csv (str): Name of the output CSV file.
        voxel_size_um (tuple): Voxel size in micrometers.
        percentile (int): Percentile used to determine the threshold.
    """
    # Ensure the output CSV file exists
    if not os.path.exists(output_csv):
        df = pd.DataFrame(columns=["File Name", "Threshold Value", "Voxels Above Threshold (mm^3)"])
        df.to_csv(output_csv, index=False)

    # List all .nrrd files in the specified folder
    nrrd_files = [f for f in os.listdir(folder_path) if f.endswith(".nrrd")]

    # Convert voxel size from micrometers to millimeters
    voxel_volume_mm3 = np.prod(voxel_size_um) / 1e9

    # Process each .nrrd file
    for nrrd_file in tqdm(nrrd_files, desc="Processing files"):
        file_path = os.path.join(folder_path, nrrd_file)

        # Load data from the .nrrd file
        data, _ = nrrd.read(file_path)

        # Filter non-zero data and determine threshold
        non_zero_data = data[data > 0]
        threshold = np.percentile(non_zero_data, percentile) if non_zero_data.size > 0 else 0

        # Count voxels above threshold and convert volume to mm^3
        above_threshold = (data > threshold).sum()
        above_threshold_mm3 = above_threshold * voxel_volume_mm3

        # Prepare result and append to CSV
        result_df = pd.DataFrame({
            "File Name": [os.path.splitext(nrrd_file)[0]],
            "Threshold Value": [threshold],
            "Voxels Above Threshold (mm^3)": [above_threshold_mm3]
        })
        result_df.to_csv(output_csv, mode='a', header=False, index=False)

    print(f"Processing complete. Results saved in {output_csv}")

# Example usage
folder_path = "your_folder_path_here"
process_nrrd_files(folder_path)