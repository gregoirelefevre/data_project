import pandas as pd
from datetime import datetime
import pprint

def load_and_clean_data(file_path):
    try:
        data = pd.read_csv(file_path)

        #Le format des sports sur 'athletes.csv' est par exemple : ['Wrestling']
        data['sport'] = data['disciplines'].str.strip("[]").str.replace("'", "").apply(
            lambda x: x.split(',')[0] if pd.notnull(x) else None
        )
        #On calcul l'âge de chaque athletes 
        current_year = datetime.now().year
        #Calcul l'âge des athlètes avec la date d'aujourd'hui 
        data['age'] = data['birth_date'].apply(lambda x: current_year if pd.notnull(x) else None)
        #Ajout de .copy() car sinon erreur Panda car c'est les mêmes dataframes
        cleaned_data = data[['sport', 'age']].copy()
        return cleaned_data

    except Exception as e:
        print(f"An error occurred while loading or cleaning the data: {e}")
        raise

def age_distribution_by_sport(cleaned_df):
    try:
        # Create a nested dictionary for age distribution by sport
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
    dictionnaire = dict(age_distribution_by_sport(load_and_clean_data(file_path)))
    #pour debug
    pprint.pprint(dictionnaire)
    return dictionnaire
