import kaggle
import subprocess
def getdata() : 
    # Set the Kaggle API key using subprocess (ensure the key is correct)
    #Si aucun identifiant kaggle configurer dans .kaggle sur votre machine decommenter la ligne ci-dessous pour utiliser nos identifiants
    #subprocess.run(['kaggle', 'config', 'set', '-n', 'grgoirelefevre', '-v', '6c63be6eb6226de8fbef6cf36edeed91'])
    kaggle.api.authenticate
    kaggle.api.dataset_download_files("piterfm/paris-2024-olympic-summer-games", path="./data/raw",unzip=True)
