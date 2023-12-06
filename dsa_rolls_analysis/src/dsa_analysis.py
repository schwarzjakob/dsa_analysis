import csv
import sys

talents_csv = '../dsa_rolls_analysis/data/rolls_results/000000_rolls_results_recent/talents.csv'
traits_csv = '../dsa_rolls_analysis/data/rolls_results/000000_rolls_results_recent/trait_usage.csv'

def process_talents(character_name):
    talents = {}
    with open(talents_csv, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Held'] == character_name:
                talent = row['Talent']
                talents[talent] = talents.get(talent, 0) + 1

    sorted_talents = sorted(talents.items(), key=lambda x: x[1], reverse=True)
    # for talent, count in sorted_talents:
    #         print(f"{talent}: {count}")
    
    return sorted_talents

def process_traits(character_name):
    traits_usage = {}
    traits_total = 0
    #csv_file_path = '../data/rolls_results/000000_rolls_results_recent/trait_usage.csv'
    with open(traits_csv, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            #print(row)
            if row['Character'] == character_name:
                for trait in row:
                    if trait != 'Character':
                        traits_total += int(row[trait])
                        traits_usage[trait] = int(row[trait])
                for trait in traits_usage:
                    traits_usage[trait] = round(int(traits_usage[trait])/traits_total, 2)

    # for trait, relative_usage in traits_usage.items():
    #         print(f"{trait}: {relative_usage}")

    return traits_usage

def talent_line_chart(character_name, talent):
    # Initialize an empty list to store the data
    talent_data = []

    # Open the CSV file and read the data
    with open(talents_csv, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Iterate through each row in the CSV file
        for row in reader:
            if row['Held'] == character_name and row['Talent'] == talent:
                # Extract the relevant data for the line chart
                # Assuming there's a column for 'Date' and 'Value'
                talent_data.append(row['TaP/ZfP'])

    # Return the data
    return talent_data


if __name__ == "__main__":
    app.run(debug=True)

    # Print the processed data so Flask can capture it
    

