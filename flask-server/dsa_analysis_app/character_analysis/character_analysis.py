import os
import pandas as pd
import numpy as np

# Constants for CSV file paths
CSV_BASE_PATH = "./dsa_analysis_app/data/rolls_results/000000_rolls_results_recent/"
TALENTS_CSV = os.path.join(CSV_BASE_PATH, "talents.csv")
TRAITS_CSV = os.path.join(CSV_BASE_PATH, "trait_usage.csv")
TRAIT_VALUES_CSV = os.path.join(CSV_BASE_PATH, "trait_values.csv")
ATTACKS_CSV = os.path.join(CSV_BASE_PATH, "attacks.csv")

# Constants for CSV column names
CHARACTER_KEY = "Character"
CATEGORY_KEY = "Category"
TALENT_KEY = "Talent"
TALENT_POINTS_KEY = "TaP/ZfP"


# Traits and categories
def get_character_traits_values(character_name):
    """Gets traits values for a given character."""
    df = pd.read_csv(TRAIT_VALUES_CSV)  # Read the CSV file into a DataFrame
    filtered_df = df[
        df[CHARACTER_KEY] == character_name
    ]  # Filter the DataFrame to only include the specified character
    return filtered_df.drop(columns=[CHARACTER_KEY]).to_dict(orient="records")[
        0
    ]  # Convert to dictionary and remove the character name


def get_character_relative_traits_usage(character_name):
    """Gets traits usage distribution for a given character."""
    df = pd.read_csv(TRAITS_CSV)  # Read the CSV file into a DataFrame
    filtered_df = df[
        df[CHARACTER_KEY] == character_name
    ]  # Filter the DataFrame to only include the specified character
    traits_count = filtered_df.drop(columns=[CHARACTER_KEY]).sum()  # Sum the occurrences of each trait
    relative_frequencies = traits_count / traits_count.sum()  # Calculate the relative frequency of each trait
    relative_freq_dict = relative_frequencies.round(
        2
    ).to_dict()  # Convert to dictionary and round values to two decimal places
    return relative_freq_dict


def get_character_relative_talents_categories_usage(character_name):
    """Calculate the relative frequency of each category for a specified character."""
    df = pd.read_csv(TALENTS_CSV)  # Read the CSV file into a DataFrame
    filtered_df = df[
        df[CHARACTER_KEY] == character_name
    ]  # Filter the DataFrame to only include the specified character
    category_counts = filtered_df[CATEGORY_KEY].value_counts()  # Count the occurrences of each category
    relative_frequencies = category_counts / category_counts.sum()  # Calculate the relative frequency of each category
    relative_freq_dict = relative_frequencies.round(
        2
    ).to_dict()  # Convert to dictionary and round values to two decimal places
    return relative_freq_dict


# Talents and talent statistics
def get_character_talents(character_name):
    """Gets talents for a given character."""
    df = pd.read_csv(TALENTS_CSV)  # Read the CSV file into a DataFrame
    filtered_df = df[
        df[CHARACTER_KEY] == character_name
    ]  # Filter the DataFrame to only include the specified character
    talents_metrics = filtered_df.groupby(TALENT_KEY).agg(
        talent_count=(TALENT_KEY, "count"),
        success_rate=("TaP/ZfP", lambda x: sum(x >= 0) / len(x)),
        failure_rate=("TaP/ZfP", lambda x: sum(x < 0) / len(x)),
        avg_score=("TaP/ZfP", "mean"),
        std_dev=("TaP/ZfP", "std"),
    )  # Calculate the performance metrics for each talent
    talents_metrics = talents_metrics.fillna(0)  # Replace NaN values with 0
    talents_metrics = talents_metrics.sort_values(
        by="talent_count", ascending=False
    )  # Sort by descending order of talent count
    return talents_metrics.round(2).to_dict(
        orient="index"
    )  # Convert to dictionary and round values to two decimal places


def get_character_talent_line_chart(character_name, talent):
    """Generates data for a talent line chart for a given character."""
    df = pd.read_csv(TALENTS_CSV)  # Read the CSV file into a DataFrame
    filtered_df = df[
        (df[CHARACTER_KEY] == character_name) & (df[TALENT_KEY] == talent)
    ]  # Filter the DataFrame to only include the specified character and talent
    return filtered_df[TALENT_POINTS_KEY].to_list()  # Return the list of talent points


def get_character_talent_statistics(character_name, talent):
    """Calculates various statistics for a specific talent of a given character."""
    df = pd.read_csv(TALENTS_CSV)  # Read the CSV file into a DataFrame
    # Filter for the specific character and talent
    filtered_df = df[(df[CHARACTER_KEY] == character_name) & (df[TALENT_KEY] == talent)]

    if filtered_df.empty:
        return "No data available for this character and talent."

    # Calculate different statistics
    talent_statistics = {}
    total_attempts = len(filtered_df)
    talent_statistics["Total Attempts"] = total_attempts

    # Use overall average if attempts are less than 50, otherwise calculate first 30 and last 30
    if total_attempts < 50:
        talent_statistics["Average Total"] = filtered_df[TALENT_POINTS_KEY].mean().round(2)
    else:
        talent_statistics["Average First 30 Attempts"] = filtered_df.head(30)[TALENT_POINTS_KEY].mean().round(2)
        talent_statistics["Average Last 30 Attempts"] = filtered_df.tail(30)[TALENT_POINTS_KEY].mean().round(2)

    talent_statistics["Successes"] = sum(filtered_df[TALENT_POINTS_KEY] > 0)
    talent_statistics["Failures"] = sum(filtered_df[TALENT_POINTS_KEY] <= 0)
    talent_statistics["Max Score"] = filtered_df[TALENT_POINTS_KEY].max()
    talent_statistics["Min Score"] = filtered_df[TALENT_POINTS_KEY].min()
    talent_statistics["Standard Deviation"] = filtered_df[TALENT_POINTS_KEY].std().round(2)

    # Convert all int64 values to native Python integers
    talent_statistics = {
        key: int(value) if isinstance(value, np.int64) else value for key, value in talent_statistics.items()
    }

    return talent_statistics


def get_character_talent_investment_recommendation(talent_statistics):
    """
    Determines if a user should invest in a talent based on its success rate, improvement over time, and consistency.
    """
    # Define thresholds
    SUCCESS_RATE_THRESHOLD = 0.6  # Success rate below which improvement is needed
    IMPROVEMENT_THRESHOLD = 2  # Minimum improvement needed between first and last 30 attempts
    CONSISTENCY_THRESHOLD = 5  # Standard deviation threshold above which talent is considered inconsistent

    # Calculate success rate
    success_rate = talent_statistics["Successes"] / talent_statistics["Total Attempts"]

    # Check for improvement over time
    improvement = 0
    if "Average Last 30 Attempts" in talent_statistics and "Average First 30 Attempts" in talent_statistics:
        improvement = talent_statistics["Average Last 30 Attempts"] - talent_statistics["Average First 30 Attempts"]

    # Check consistency
    consistency = talent_statistics["Standard Deviation"]

    # Determine recommendation
    if (
        success_rate < SUCCESS_RATE_THRESHOLD
        or improvement < IMPROVEMENT_THRESHOLD
        or consistency > CONSISTENCY_THRESHOLD
    ):
        return "Invest in this talent for improvement."
    else:
        return "No need to invest further in this talent."


# Attacks and attack statistics
def get_character_attacks(character_name):
    """Gets attacks for a given character."""
    df = pd.read_csv(ATTACKS_CSV)  # Read the CSV file into a DataFrame
    filtered_df = df[
        df[CHARACTER_KEY] == character_name
    ]  # Filter the DataFrame to only include the specified character
    attacks_metrics = filtered_df.groupby(TALENT_KEY).agg(
        attack_count=(TALENT_KEY, "count"),
        success_rate=("TaP/ZfP", lambda x: sum(x >= 0) / len(x)),
        failure_rate=("TaP/ZfP", lambda x: sum(x < 0) / len(x)),
        avg_score=("TaP/ZfP", "mean"),
        std_dev=("TaP/ZfP", "std"),
    )  # Calculate the performance metrics for each attack
    attacks_metrics = attacks_metrics.fillna(0)  # Replace NaN values with 0
    attacks_metrics = attacks_metrics.sort_values(
        by="attack_count", ascending=False
    )  # Sort by descending order of attack count
    return attacks_metrics.round(2).to_dict(
        orient="index"
    )  # Convert to dictionary and round values to two decimal places


def get_character_attack_line_chart(character_name, talent):
    df = pd.read_csv(ATTACKS_CSV)  # Read the CSV file into a DataFrame
    filtered_df = df[
        (df[CHARACTER_KEY] == character_name) & (df[TALENT_KEY] == talent)
    ]  # Filter the DataFrame to only include the specified character and talent
    return filtered_df[TALENT_POINTS_KEY].to_list()  # Return the list of talent points


def get_character_attack_statistics(character_name, attack):
    """Calculates various statistics for a specific attack."""
    df = pd.read_csv(ATTACKS_CSV)  # Read the CSV file into a DataFrame
    # Filter for the specific character and attack
    filtered_df = df[(df[CHARACTER_KEY] == character_name) & (df[TALENT_KEY] == attack)]

    if filtered_df.empty:
        return "No data available for this character and attack."

    # Calculate different statistics
    attack_statistics = {}
    total_attempts = len(filtered_df)
    attack_statistics["Total Attempts"] = total_attempts

    # Use overall average if attempts are less than 50, otherwise calculate first 30 and last 30
    if total_attempts < 50:
        attack_statistics["Average Total"] = filtered_df[TALENT_POINTS_KEY].mean().round(2)
    else:
        attack_statistics["Average First 30 Attempts"] = filtered_df.head(30)[TALENT_POINTS_KEY].mean().round(2)
        attack_statistics["Average Last 30 Attempts"] = filtered_df.tail(30)[TALENT_POINTS_KEY].mean().round(2)

    attack_statistics["Successes"] = sum(filtered_df[TALENT_POINTS_KEY] > 0)
    attack_statistics["Failures"] = sum(filtered_df[TALENT_POINTS_KEY] <= 0)
    attack_statistics["Max Score"] = filtered_df[TALENT_POINTS_KEY].max()
    attack_statistics["Min Score"] = filtered_df[TALENT_POINTS_KEY].min()
    attack_statistics["Standard Deviation"] = filtered_df[TALENT_POINTS_KEY].std().round(2)

    # Convert all int64 values to native Python integers
    attack_statistics = {
        key: int(value) if isinstance(value, np.int64) else value for key, value in attack_statistics.items()
    }

    return attack_statistics


if __name__ == "__main__":
    app.run(debug=True)
