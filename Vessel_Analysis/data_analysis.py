"""
This script processes CSV files containing vessel diameter, length, and volume data to categorize vessels
into different size categories and compute statistics for each category. The script iterates over a set
of CSV files located in a specified folder, performs the categorization and aggregation of vessel data,
and saves the results to an output CSV file.
"""


import os
import pandas as pd
from collections import defaultdict
import numpy as np


# Function to categorize vessel sizes
def categorize_vessel_size(value):
    if value <= 30:
        return "small vessel"
    elif 30 < value <= 80:
        return "intermediate vessel"
    else:
        return "large vessel"

# Initialize a dictionary to store the results
results = defaultdict(dict)

# Folder path containing the CSV files
folder_path = ''

# Iterate over the range of numbers (1 to 15)
for i in range(1, 16):
    file_prefix = f'B{i}'

    # Process each type of file
    for file_type in ['cortex-left', 'cortex-right', 'hippo-left', 'hippo-right']:
        file_name = f'{file_prefix}-{file_type}'
        file_path = os.path.join(folder_path, file_name + '.csv')

        if os.path.exists(file_path):
            print('Find ' + f'{file_prefix}-{file_type}.csv')
            df = pd.read_csv(file_path)

            # Calculate the required statistics
            total_length = df['length (um)'].sum()
            total_volume = df['volume (um3)'].sum()

            vessel_sizes = df['diameter (um)'].apply(categorize_vessel_size)
            grouped = df.groupby(vessel_sizes)

            for category, group in grouped:
                results[file_name][f'{category} total length (um)'] = group['length (um)'].sum()
                results[file_name][f'{category} total volume (um3)'] = group['volume (um3)'].sum()
                # results[file_name][f'{category} average length (um)'] = group['length (um)'].mean()
                # results[file_name][f'{category} average volume (um3)'] = group['volume (um3)'].mean()
                # results[file_name][f'{category} stddev length (um)'] = group['length (um)'].std()
                # results[file_name][f'{category} stddev volume (um3)'] = group['volume (um3)'].std()
                # results[file_name][f'{category} median length (um)'] = group['length (um)'].median()
                # results[file_name][f'{category} median volume (um3)'] = group['volume (um3)'].median()
            results[file_name]['total length (um)'] = total_length
            results[file_name]['total volume (um3)'] = total_volume

# Create a DataFrame from the results dictionary
result_df = pd.DataFrame.from_dict(results, orient='index')

# Save the results to an output CSV file
output_file = '/Users/qinghuahan/Desktop/LiuLabProjects/3D_Vessel_Segmentation/Traumatic Brain Injuary Study/Data/output.csv'
if os.path.exists(output_file):
    existing_df = pd.read_csv(output_file, index_col=0)
    result_df = pd.concat([existing_df, result_df], axis=1, sort=False)
result_df.to_csv(output_file)

print(f'Results saved to {output_file}')