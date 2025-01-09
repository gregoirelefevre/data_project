import pandas as pd
from datetime import datetime
import pprint

def load_and_clean_data(file_path):
    try:
        data = pd.read_csv(file_path)
        
        # Le format des sports sur 'athletes.csv' est par exemple : ['Wrestling']
        data['sport'] = data['disciplines'].str.strip("[]").str.replace("'", "").apply(
            lambda x: x.split(',')[0] if pd.notnull(x) else None
        )
        
        # Conversion de la colonne 'birth_date' en datetime
        data['birth_date'] = pd.to_datetime(data['birth_date'], errors='coerce')
        
        # Calcul de l'âge des athlètes
        current_year = datetime.now().year
        data['age'] = data['birth_date'].apply(lambda x: current_year - x.year if pd.notnull(x) else None)
        
        # Ajout de .copy() pour éviter une erreur d'avertissement pandas
        cleaned_data = data[['sport', 'age']].copy()
        return cleaned_data

    except Exception as e:
        print(f"An error occurred while loading or cleaning the data: {e}")
        raise

def age_distribution_by_sport(cleaned_df):
    try:
        # Crée un dictionnaire imbriqué pour la distribution des âges par sport
        sport_age_distribution = {}
        grouped = cleaned_df.groupby('sport')

        for sport, group in grouped:
            age_counts = group['age'].value_counts().sort_index()
            sport_age_distribution[sport] = dict(age_counts)

        return dict(sport_age_distribution)
    except Exception as e:
        print(f"An error occurred while creating the nested dictionary: {e}")
        raise

def clean_data_histo(file_path):
    dictionnaire = age_distribution_by_sport(load_and_clean_data(file_path))
    #pprint.pprint(dictionnaire)  # Pour le debug
    #print(dictionnaire)
    return dictionnaire


def load_ranking() :
    try:
        # data <= CSV contenant la liste des pays médaillés et leurs résultats
        data = pd.read_csv('data/raw/27/medals_total.csv')
        # ranking_dict <= country_code : name, gold, silver, bronze, total, rank
        ranking_dict = {
            row['country_code']: {
                'name': row['country'],
                'gold': row['Gold Medal'],
                'silver': row['Silver Medal'],
                'bronze': row['Bronze Medal'],
                'total': row['Total'],
                'rank': index + 1
            }
            for index, row in data.iterrows()
        }
        return ranking_dict

    except Exception as e:
        print(f"Erreur lors de load_ranking() {e}")
        raise


def load_country() :
    try:
        # data <= CSV contenant la liste des pays participants
        data = pd.read_csv('data/raw/27/nocs.csv')
        # return la liste des Noms et codes des pays participants
        return data['code'].tolist() + data['country'].tolist()
    
    except Exception as e:
        print(f"Erreur lors de load_country() {e}")
        raise