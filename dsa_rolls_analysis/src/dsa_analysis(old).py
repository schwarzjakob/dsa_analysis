import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
file_path = '../data/rolls_results/000000_rolls_results_recent/talents.csv'
df = pd.read_csv(file_path)
df_trait_usage = pd.read_csv('../data/rolls_results/000000_rolls_results_recent/trait_usage.csv')
characters = ["Akira Masamune", "Hanzo Shimada", "Elanor Walham", "Bargaan Treuwall", "Walpurga Hausmännin"]
traits = ["MU", "KL", "IN", "CH", "FF", "GE", "KO", "KK"]

def plot_scatter_eigenschaftswert():
    plt.figure(figsize=(10, 6))
    plt.scatter(df['Eigenschaftswert 1'], df['TaP/ZfP'], label='Eigenschaft 1')
    plt.scatter(df['Eigenschaftswert 2'], df['TaP/ZfP'], label='Eigenschaft 2')
    plt.scatter(df['Eigenschaftswert 3'], df['TaP/ZfP'], label='Eigenschaft 3')
    plt.xlabel('Eigenschaftswert')
    plt.ylabel('TaP/ZfP')
    plt.legend()
    plt.title('TaP/ZfP vs Eigenschaftswert')
    plt.show()

def plot_histogram_tap_zfp():
    plt.figure(figsize=(10, 6))
    plt.hist(df['TaP/ZfP'], bins=20, edgecolor='black')
    plt.xlabel('TaP/ZfP')
    plt.ylabel('Frequency')
    plt.title('Distribution of TaP/ZfP')
    plt.show()

def plot_bar_success_rate():
    success_counts = df['Erfolg'].value_counts()
    plt.figure(figsize=(10, 6))
    success_counts.plot(kind='bar')
    plt.xlabel('Erfolg')
    plt.ylabel('Count')
    plt.title('Success Rate')
    plt.xticks(rotation=0)
    plt.show()

def plot_line_tap_zfp_over_time():
    plt.figure(figsize=(10, 6))
    df['TaP/ZfP'].plot(kind='line')
    plt.xlabel('Roll Number')
    plt.ylabel('TaP/ZfP')
    plt.title('TaP/ZfP Over Time')
    plt.show()

def plot_box_tap_zfp_by_eigenschaft():
    plt.figure(figsize=(10, 6))
    df.boxplot(column='TaP/ZfP', by='Eigenschaftswert 1')
    plt.title('TaP/ZfP by Eigenschaftswert 1')
    plt.suptitle('')
    plt.show()

def plot_heatmap_tap_zfp_vs_modifikator():
    plt.figure(figsize=(10, 6))
    heatmap_data = pd.pivot_table(df, values='TaP/ZfP', index='Modifikator', columns='Eigenschaftswert 1', aggfunc='mean')
    sns.heatmap(heatmap_data, annot=True, cmap='coolwarm')
    plt.title('Heatmap of TaP/ZfP vs Modifikator')
    plt.show()

def plot_scatterplot_matrix():
    sns.pairplot(df[['TaP/ZfP', 'Eigenschaftswert 1', 'Eigenschaftswert 2', 'Eigenschaftswert 3']])
    plt.show()

def plot_correlation_matrix():
    corr_matrix = df[['TaP/ZfP', 'Eigenschaftswert 1', 'Eigenschaftswert 2', 'Eigenschaftswert 3']].corr()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
    plt.title('Correlation Matrix')
    plt.show()

def filter_dataframe(character, category, talent):
    filtered_df = df[(df['Held'] == character) & 
                     (df['Kategorie'] == category) & 
                     (df['Talent'] == talent)]
    return filtered_df.reset_index(drop=True)

def plot_tap_over_time_for_character(filtered_df):
    # Reindexing with a continuous sequence of roll numbers
    filtered_df = filtered_df.reset_index(drop=True)
    
    plt.figure(figsize=(10, 6))
    plt.plot(filtered_df.index, filtered_df['TaP/ZfP'])
    plt.xlabel('Roll Number')
    plt.ylabel('TaP/ZfP')
    plt.title(f'TaP/ZfP Over Time for {character}, {category}, {talent}')
    plt.show()

def plot_tap_taw_mod_over_time(filtered_df):
    plt.figure(figsize=(10, 6))

    # Plotting TaP/ZfP, TaW, and Modifikator on the same axis
    plt.plot(filtered_df.index, filtered_df['TaP/ZfP'], label='TaP/ZfP', color='blue', marker='o')
    plt.plot(filtered_df.index, filtered_df['TaW/ZfW'], label='TaW/ZfW', color='green', marker='x')
    plt.plot(filtered_df.index, filtered_df['Modifikator'], label='Modifikator', color='red', linestyle='--')

    plt.xlabel('Roll Number')
    plt.ylabel('Values')
    plt.title('TaP/ZfP, TaW/ZfW, and Modifikator Over Time')
    plt.legend()
    plt.show()

def plot_stacked_trait_distribution():

    # Define the characters and traits
    characters = df_trait_usage['Character'].tolist()
    traits = df_trait_usage.columns.tolist()[1:]  # Assuming first column is 'Character'

    # Initialize a dictionary to hold trait counts for each character
    char_trait_counts = {character: {} for character in characters}
    
    # Extract trait counts from the DataFrame
    for character in df_trait_usage['Character']:
        for trait in traits:
            char_trait_counts[character][trait] = df_trait_usage[df_trait_usage['Character'] == character][trait].values[0]

    print(char_trait_counts)
    # Convert counts to fractions
    for character in characters:
        total = sum(char_trait_counts[character].values())
        for trait in traits:
            char_trait_counts[character][trait] /= total

    # Plotting
    plt.figure(figsize=(16, 8))
    bottoms = {character: 0 for character in characters}  # Initialize bottom position for each character bar
    for trait in traits:
        trait_values = [char_trait_counts[character][trait] for character in characters]
        plt.bar(characters, trait_values, bottom=[bottoms[character] for character in characters], label=trait)
        for i, character in enumerate(characters):
            if trait_values[i] > 0.05:  # Only display label for significant fractions
                plt.text(i, bottoms[character] + trait_values[i] / 2, f'{trait_values[i]:.2f}', ha='center')
            bottoms[character] += trait_values[i]  # Update bottom position for the next trait

    plt.xlabel('Character')
    plt.ylabel('Fraction of Trait Usage')
    plt.title('Relative Distribution of Trait Usage per Character')
    plt.legend(title='Traits', loc='upper right')
    plt.xticks(range(len(characters)), characters)
    plt.show()






# To plot TaP over time for a specific character, category, and talent

#filtered_df = filter_dataframe('Hanzo Shimada', 'Natur', 'Fährtensuchen')
#plot_tap_taw_mod_over_time(filtered_df)

plot_stacked_trait_distribution()