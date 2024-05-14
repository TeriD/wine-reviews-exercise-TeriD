import zipfile
import os
import pandas as pd


def unzip_file(zip_file_path, extract_to):
    # Unzip the zipfile to the data directory.
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
        return [os.path.join(extract_to, file) for file in zip_ref.namelist()]


# MAIN

# Get the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Set the data folder name
data_dir = os.path.join(script_dir, "data")

# Set zip file name
zip_filename = "winemag-data-130k-v2.csv.zip"

# Define the zip file path
zip_file_path = os.path.join(data_dir,  zip_filename)

# Unzip the file
extracted_files = unzip_file(zip_file_path, data_dir)

print("Files extracted to:", extracted_files)

# Load the first extracted file into a pandas DataFrame
df = pd.read_csv(extracted_files[0])

# Print the first few rows of the DataFrame
print(df.head())

# Create the summary
summary = df.groupby('country').agg(
    count=pd.NamedAgg(column='title', aggfunc='count'),
    points=pd.NamedAgg(column='points', aggfunc='mean')
).round(1).reset_index()

# Write the summary to a new CSV file
summary.to_csv(os.path.join(data_dir, 'reviews-per-country.csv'), index=False)
print("Summary written to reviews-per-country.csv")
