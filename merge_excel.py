#!/usr/bin/env python3
import pandas as pd

# Adjust the chunk_size based on your available memory
chunk_size = 50000

# Replace 'file1.xlsx', 'file2.xlsx', and 'file3.xlsx' with your actual file names
file1 = pd.read_excel('Sentiment 1.xlsx')
file2 = pd.read_excel('Sentiment 2.xlsx')
file3 = pd.read_excel('Sentiment 3.xlsx')

# Create chunks manually
file1_chunks = [file1[i:i + chunk_size] for i in range(0, len(file1), chunk_size)]
file2_chunks = [file2[i:i + chunk_size] for i in range(0, len(file2), chunk_size)]
file3_chunks = [file3[i:i + chunk_size] for i in range(0, len(file3), chunk_size)]

merged_data_chunks = []

# Process file1
print("Processing file1 in chunks...")
for idx, chunk in enumerate(file1_chunks):
    print(f"Processing chunk {idx + 1} of file1...")
    # Your processing logic here
    merged_data_chunks.append(chunk)

# Process file2
print("Processing file2 in chunks...")
for idx, chunk in enumerate(file2_chunks):
    print(f"Processing chunk {idx + 1} of file2...")
    # Your processing logic here
    merged_data_chunks.append(chunk)

# Process file3
print("Processing file3 in chunks...")
for idx, chunk in enumerate(file3_chunks):
    print(f"Processing chunk {idx + 1} of file3...")
    # Your processing logic here
    merged_data_chunks.append(chunk)

# Concatenate all chunks
print("Concatenating all files")
merged_data = pd.concat(merged_data_chunks, ignore_index=True)

# Save the merged data to a new Excel file
merged_data.to_excel('sentiment_fullcorpus.xlsx', index=False)

print("Merging completed. Output saved to sentiment_fullcorpus.xlsx.")
