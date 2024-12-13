import kagglehub

# Download latest version
path = kagglehub.dataset_download("piterfm/paris-2024-olympic-summer-games")

print("Path to dataset files:", path)