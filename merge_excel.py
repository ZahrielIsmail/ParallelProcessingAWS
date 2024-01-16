import pandas as pd

# Adjust the chunk_size based on your available memory
chunk_size = 50000

# Replace 'file1.xlsx', 'file2.xlsx', and 'file3.xlsx' with your actual file names
file1_chunks = pd.read_excel('Sentiment 1.xlsx', chunksize=chunk_size)
file2_chunks = pd.read_excel('Sentiment 2.xlsx', chunksize=chunk_size)
file3_chunks = pd.read_excel('Sentiment 3.xlsx', chunksize=chunk_size)

merged_data_chunks = []

# Process file1
print("Reading and processing file1...")
for idx, chunk in enumerate(file1_chunks):
    print(f"Processing chunk {idx + 1} of file1...")
    # Your processing logic here
    merged_data_chunks.append(chunk)

# Process file2
print("Reading and processing file2...")
for idx, chunk in enumerate(file2_chunks):
    print(f"Processing chunk {idx + 1} of file2...")
    # Your processing logic here
    merged_data_chunks.append(chunk)

# Process file3
print("Reading and processing file3...")
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
