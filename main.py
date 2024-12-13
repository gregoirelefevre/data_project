import kagglehub
import subprocess
import os

# Set the Kaggle API key using subprocess (ensure the key is correct)
subprocess.run(['kaggle', 'config', 'set', '-n', 'grgoirelefevre', '-v', '6c63be6eb6226de8fbef6cf36edeed91'])
target_path = "./data/raw"


try:
    if not(any(os.path.isfile(os.path.join(target_path, f)) for f in os.listdir(target_path))): 
        path_check = "/Users/gregoirelefevre/.cache/kagglehub/datasets/"
        if not(any(os.path.isfile(os.path.join(path_check, f)) for f in os.listdir(path_check))):
            path = kagglehub.dataset_download("piterfm/paris-2024-olympic-summer-games")
            print("Path to dataset files:", path)
            subprocess.run(['mv', path, target_path], check=True)
            print("Move the data to :", target_path)
        else :
            print("Move the data to :", path_check)
    else :
        print("Already a file in", target_path)
except Exception as e:
    print("An error occurred:", e)
