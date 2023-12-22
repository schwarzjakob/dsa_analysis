import csv
import os
import pandas as pd

# Constants for CSV file paths
CSV_BASE_PATH = './dsa_analysis/data/rolls_results/000000_rolls_results_recent/'
TALENTS_CSV = os.path.join(CSV_BASE_PATH, 'talents.csv')
TRAITS_CSV = os.path.join(CSV_BASE_PATH, 'trait_usage.csv')
TRAIT_VALUES_CSV = os.path.join(CSV_BASE_PATH, 'trait_values.csv')

CHARACTER_KEY = 'Character'
CATEGORY_KEY = 'Category'
TALENT_KEY = 'Talent'
TALENT_POINTS_KEY = 'TaP/ZfP'

def read_csv(file_path):
    """Reads a CSV file and returns a list of dictionaries."""
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            return list(csv.DictReader(csvfile))
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []

def get_character_talents(character_name):
    """Processes talents for a given character."""
    talents_data = read_csv(TALENTS_CSV)
    talents = {}
    for row in talents_data:
        if row[CHARACTER_KEY] == character_name:
            talent = row[TALENT_KEY]
            talents[talent] = talents.get(talent, 0) + 1

    return sorted(talents.items(), key=lambda x: x[1], reverse=True)

def get_character_traits_values(character_name):
    """Gets traits values for a given character."""
    traits_values_data = read_csv(TRAIT_VALUES_CSV)
    for row in traits_values_data:
        if row[CHARACTER_KEY] == character_name:
            return {trait: row[trait] for trait in row if trait != CHARACTER_KEY}
    return {}

def get_character_relative_traits_usage(character_name):
    """Processes traits usage for a given character."""
    traits_data = read_csv(TRAITS_CSV)
    traits_usage = {}
    traits_total = 0
    for row in traits_data:
        if row[CHARACTER_KEY] == character_name:
            for trait, value in row.items():
                if trait != CHARACTER_KEY:
                    value = int(value)
                    traits_total += value
                    traits_usage[trait] = value
    return {trait: round(value / traits_total, 2) for trait, value in traits_usage.items()}

def get_character_relative_talents_categories_usage(character_name):
    """
    Calculate the relative frequency of each category for a specified character.

    :param character: The name of the character to filter by.
    :param df: The DataFrame containing the data.
    :return: A DataFrame with relative frequencies of each category for the specified character.
    """
    # Read the CSV file into a DataFrame
    df = pd.read_csv(TALENTS_CSV)

    # Filter the DataFrame for the specified character
    filtered_df = df[df[CHARACTER_KEY] == character_name]

    # Count the occurrences of each category
    category_counts = filtered_df[CATEGORY_KEY].value_counts()

    # Calculate the relative frequency
    relative_frequencies = category_counts / category_counts.sum()

    # Convert to dictionary and round values to two decimal places
    relative_freq_dict = relative_frequencies.round(2).to_dict()

    return relative_freq_dict

def get_character_talent_line_chart(character_name, talent):
    """Generates data for a talent line chart for a given character."""
    talents_data = read_csv(TALENTS_CSV)
    return [row[TALENT_POINTS_KEY] for row in talents_data if row[CHARACTER_KEY] == character_name and row[TALENT_KEY] == talent]

if __name__ == "__main__":
    app.run(debug=True)