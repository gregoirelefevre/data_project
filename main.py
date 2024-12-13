import kagglehub
import subprocess
import os

# Set the Kaggle API key using subprocess (ensure the key is correct)
subprocess.run(['kaggle', 'config', 'set', '-n', 'grgoirelefevre', '-v', '6c63be6eb6226de8fbef6cf36edeed91'])

# Define the target path relative to your project (the 'data/raw' directory)
target_path = "./data/raw"
print(target_path)

try:
    # Download the dataset to the specified target path (not the default .cache/kagglehub location)
    path = kagglehub.dataset_download("piterfm/paris-2024-olympic-summer-games")
    print("Path to dataset files:", path)
    subprocess.run(['mv', path, target_path], check=True)
    print("Move the data to :", target_path)
except Exception as e:
    print("An error occurred:", e)
