import os
import pandas as pd

# Constants for CSV file paths
CSV_BASE_PATH = './dsa_analysis/data/rolls_results/000000_rolls_results_recent/'
TALENTS_CSV = os.path.join(CSV_BASE_PATH, 'talents.csv')
TRAITS_CSV = os.path.join(CSV_BASE_PATH, 'trait_usage.csv')
TRAIT_VALUES_CSV = os.path.join(CSV_BASE_PATH, 'trait_values.csv')

# Constants for CSV column names
CHARACTER_KEY = 'Character'
CATEGORY_KEY = 'Category'
TALENT_KEY = 'Talent'
TALENT_POINTS_KEY = 'TaP/ZfP'

def get_character_talents(character_name):
    """Gets talents for a given character."""
    df = pd.read_csv(TALENTS_CSV) # Read the CSV file into a DataFrame
    filtered_df = df[df[CHARACTER_KEY] == character_name] # Filter the DataFrame to only include the specified character
    talents_count = filtered_df[TALENT_KEY].value_counts() # Count the occurrences of each talent
    return talents_count.sort_values(ascending=False).to_dict() # Convert to dictionary and sort by descending order

def get_character_traits_values(character_name):
    """Gets traits values for a given character."""
    df = pd.read_csv(TRAIT_VALUES_CSV) # Read the CSV file into a DataFrame
    filtered_df = df[df[CHARACTER_KEY] == character_name] # Filter the DataFrame to only include the specified character
    return filtered_df.drop(columns=[CHARACTER_KEY]).to_dict(orient='records')[0] # Convert to dictionary and remove the character name

def get_character_relative_traits_usage(character_name):
    """Gets traits usage distribution for a given character."""
    df = pd.read_csv(TRAITS_CSV) # Read the CSV file into a DataFrame
    filtered_df = df[df[CHARACTER_KEY] == character_name] # Filter the DataFrame to only include the specified character
    traits_count = filtered_df.drop(columns=[CHARACTER_KEY]).sum() # Sum the occurrences of each trait
    relative_frequencies = traits_count / traits_count.sum() # Calculate the relative frequency of each trait
    relative_freq_dict = relative_frequencies.round(2).to_dict() # Convert to dictionary and round values to two decimal places
    return relative_freq_dict

def get_character_relative_talents_categories_usage(character_name):
    """Calculate the relative frequency of each category for a specified character."""
    df = pd.read_csv(TALENTS_CSV) # Read the CSV file into a DataFrame
    filtered_df = df[df[CHARACTER_KEY] == character_name] # Filter the DataFrame to only include the specified character
    category_counts = filtered_df[CATEGORY_KEY].value_counts() # Count the occurrences of each category
    relative_frequencies = category_counts / category_counts.sum() # Calculate the relative frequency of each category    
    relative_freq_dict = relative_frequencies.round(2).to_dict() # Convert to dictionary and round values to two decimal places
    return relative_freq_dict 

def get_character_talent_line_chart(character_name, talent):
    """Generates data for a talent line chart for a given character."""
    df = pd.read_csv(TALENTS_CSV) # Read the CSV file into a DataFrame
    filtered_df = df[(df[CHARACTER_KEY] == character_name) & (df[TALENT_KEY] == talent)] # Filter the DataFrame to only include the specified character and talent
    return filtered_df[TALENT_POINTS_KEY].to_list() # Return the list of talent points

if __name__ == "__main__":
    app.run(debug=True)