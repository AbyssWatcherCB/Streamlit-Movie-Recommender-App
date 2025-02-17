import pickle
import os

# Load the original large file
with open("similarity.pkl", "rb") as f:
    similarity_matrix = pickle.load(f)

# Define chunk size (24MB)
chunk_size = 99 * 1024 * 1024  # 24MB

# Serialize the object into bytes
data = pickle.dumps(similarity_matrix)

# Create a folder for chunks
os.makedirs("similarity_parts", exist_ok=True)

# Split and save parts
for i in range(0, len(data), chunk_size):
    part_filename = f"similarity_parts/similarity_part_{i // chunk_size}.pkl"
    with open(part_filename, "wb") as part_file:
        part_file.write(data[i : i + chunk_size])

print("✅ similarity.pkl has been split into 99MB parts!")
