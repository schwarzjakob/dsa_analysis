import csv
import os

# Constants for CSV file paths
CSV_BASE_PATH = './dsa_analysis/data/rolls_results/000000_rolls_results_recent/'
TALENTS_CSV = os.path.join(CSV_BASE_PATH, 'talents.csv')
TRAITS_CSV = os.path.join(CSV_BASE_PATH, 'trait_usage.csv')
TRAIT_VALUES_CSV = os.path.join(CSV_BASE_PATH, 'trait_values.csv')

CHARACTER_KEY = 'Character'
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

#get character's specific talents
def process_talents(character_name):
    """Processes talents for a given character."""
    talents_data = read_csv(TALENTS_CSV)
    talents = {}
    for row in talents_data:
        if row[CHARACTER_KEY] == character_name:
            talent = row[TALENT_KEY]
            talents[talent] = talents.get(talent, 0) + 1

    return sorted(talents.items(), key=lambda x: x[1], reverse=True)

def process_traits(character_name):
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

def get_traits_values(character_name):
    """Gets trait values for a given character."""
    traits_values_data = read_csv(TRAIT_VALUES_CSV)
    for row in traits_values_data:
        if row[CHARACTER_KEY] == character_name:
            return {trait: row[trait] for trait in row if trait != CHARACTER_KEY}
    return {}

def talent_line_chart(character_name, talent):
    """Generates data for a talent line chart for a given character."""
    talents_data = read_csv(TALENTS_CSV)
    return [row[TALENT_POINTS_KEY] for row in talents_data if row[CHARACTER_KEY] == character_name and row[TALENT_KEY] == talent]

if __name__ == "__main__":
    app.run(debug=True)