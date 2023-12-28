import pandas as pd
import os

# Specify the directory containing the CSV files
directory = r'C:\Users\12064\PycharmProjects\mimic\data_file\test'

# Loop through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        # Construct the full file path
        file_path = os.path.join(directory, filename)

        # Read the CSV file
        df = pd.read_csv(file_path)

        # Take the first 10 rows
        df_top10 = df.head(10)

        # Construct the output file path
        output_file_path = os.path.join(directory, f"top10_{filename}")

        # Save the top 10 rows to a new CSV file
        df_top10.to_csv(output_file_path, index=False)

print("Processed all CSV files.")
