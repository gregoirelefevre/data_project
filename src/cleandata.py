import pandas as pd
from datetime import datetime
import pprint

def load_and_clean_data(file_path):
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Extract the first discipline and clean it up
        df['sport'] = df['disciplines'].str.strip("[]").str.replace("'", "").apply(
            lambda x: x.split(',')[0] if pd.notnull(x) else None
        )

        # Calculate the age from the birth date
        current_year = datetime.now().year
        df['birth_date'] = pd.to_datetime(df['birth_date'], errors='coerce')
        df['age'] = df['birth_date'].apply(lambda x: current_year - x.year if pd.notnull(x) else None)

        # Select the relevant columns
        cleaned_df = df[['sport', 'age']].copy()

        # Drop rows with missing values in 'sport' or 'age'
        cleaned_df = cleaned_df.dropna(subset=['sport', 'age'])

        return cleaned_df

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
    pprint.pprint(dictionnaire)
    return dictionnaire
