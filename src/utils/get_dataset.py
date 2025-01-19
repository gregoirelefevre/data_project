import kaggle
import os
import json
def getdata() : 

    q1 = input("Pour récuperer les données sur kaggle il faut vos que vos identifiants soit configurer dans un fichier kaggle.json dans le répértoire .kaggle sur votre machine. Si c'est déjà fait 'y' sinon 'n' : ") 
    if(q1 == "n") : 
        #il vous faut avoir créer un compte kaggle, 
        username = input("Entrez votre identifiant kaggle : ")
        api_key = input("Entrez votre clé API kaggle : ")
        setup_kaggle_json(username, api_key)
        #setup_kaggle_json(grgoirelefevre, 6c63be6eb6226de8fbef6cf36edeed91)
    kaggle.api.authenticate
    kaggle.api.dataset_download_files("piterfm/paris-2024-olympic-summer-games", path="data/raw",unzip=True)

def setup_kaggle_json(username, api_key):
    kaggle_dir = os.path.expanduser("~/.kaggle")
    os.makedirs(kaggle_dir, exist_ok=True)
    
    kaggle_json_path = os.path.join(kaggle_dir, "kaggle.json")
    kaggle_data = {
        "username": username,
        "key": api_key
    }
    
    with open(kaggle_json_path, "w") as f:
        json.dump(kaggle_data, f)
    
    # Set appropriate permissions
    os.chmod(kaggle_json_path, 0o600)

# Replace these with your actual username and API key
setup_kaggle_json("your_username", "your_api_key")

if __name__ == "__main__":
    getdata()