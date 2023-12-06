import tkinter as tk
from tkinter import ttk
import pandas as pd
import json

# Load the talents data
with open('talents.json', 'r') as f:
    talents_data = json.load(f)
    talents_list = [talent["talent"] for talent in talents_data["talents"]]
    # Creating a dictionary for traits to easily access them based on selected talent
    traits_dict = {talent["talent"]: talent for talent in talents_data["talents"]}

# The list of characters provided in the main program
characters = ["Akira Masamune", "Hanzo Shimada", "Niko K.", "Elanor Walham", "Yannik F.", "Bargaan Treuwall", "Luisa B.", "Walpurga Hausmännin"]

# Machine learning pipeline function goes here (from the previous example)
# Save this code as a module, e.g., 'dsa_ml_model.py'
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split

# Load your dataset here (the path might need to be adjusted)
file_path = '/Users/jakobschwarz/Documents/Coding/Python/DSA rolls/rolled_dices.csv'
dsa_data = pd.read_csv(file_path)

# Data preprocessing steps from earlier should be applied here...

# Define your features and labels
X = dsa_data.drop(['Erfolg', 'TaP/ZfP'], axis=1)
y_class = dsa_data['Erfolg']  # Classification target
y_reg = dsa_data['TaP/ZfP']   # Regression target

# Split the data into training and test sets
X_train, X_test, y_train_class, y_test_class, y_train_reg, y_test_reg = train_test_split(
    X, y_class, y_reg, test_size=0.2, random_state=42)

# Preprocessing and model training pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), ['Modifikator', 'TaW/ZfW', 'Eigenschaftswert 1', 'Eigenschaftswert 2', 'Eigenschaftswert 3']),
        ('cat', OneHotEncoder(), ['Held', 'Kategorie', 'Talent', 'Eigenschaft 1', 'Eigenschaft 2', 'Eigenschaft 3'])
    ])

classifier = RandomForestClassifier(random_state=42)
regressor = RandomForestRegressor(random_state=42)

pipeline_class = Pipeline(steps=[('preprocessor', preprocessor), ('classifier', classifier)])
pipeline_reg = Pipeline(steps=[('preprocessor', preprocessor), ('regressor', regressor)])

# Train the models
pipeline_class.fit(X_train, y_train_class)
pipeline_reg.fit(X_train, y_train_reg)

# The trained 'pipeline_class' and 'pipeline_reg' can be used for prediction

# Function to predict outcomes based on the selected character, talent, and entered trait values
def predict():
    # Extract the selected character and talent
    selected_character = character_var.get()
    selected_talent = talent_var.get()

    # Get the associated trait labels for the selected talent
    trait_labels = [traits_dict[selected_talent][f"trait{i+1}"] for i in range(3)]
    
    # Extract trait values and TaW/ZfW from the user's input
    trait_values = [float(trait_entry.get()) for trait_entry in trait_entries]
    TaW_ZfW_value = float(taw_zfw_entry.get())
    
    # Prepare input data for prediction (using a placeholder for 'Kategorie' and 'Modifikator')
    input_data = pd.DataFrame({
        'Held': [selected_character],
        'Kategorie': ['Placeholder'],  # Replace with actual category if known
        'Talent': [selected_talent],
        'Eigenschaft 1': [trait_labels[0]],
        'Eigenschaft 2': [trait_labels[1]],
        'Eigenschaft 3': [trait_labels[2]],
        'Modifikator': [0],  # Assuming no modifier for simplicity
        'TaW/ZfW': [TaW_ZfW_value],
        'Eigenschaftswert 1': [trait_values[0]],
        'Eigenschaftswert 2': [trait_values[1]],
        'Eigenschaftswert 3': [trait_values[2]],
    })
    
    # Predict success and quality of result
    success = pipeline_class.predict(input_data)[0]
    quality = pipeline_reg.predict(input_data)[0]
    
    # Update the labels with the prediction results
    success_label.config(text=f"Predicted Success: {'Erfolg' if success else 'No Erfolg'}")
    quality_label.config(text=f"Predicted Quality (TaP/ZfP): {quality:.2f}")

# GUI setup
root = tk.Tk()
root.title("DSA Talent Prediction")

# Dropdown to select character
tk.Label(root, text="Select Character:").grid(row=0, column=0, sticky='w')
character_var = tk.StringVar()
character_dropdown = ttk.Combobox(root, textvariable=character_var, values=characters)
character_dropdown.grid(row=0, column=1)

# Dropdown to select talent
tk.Label(root, text="Select Talent:").grid(row=1, column=0, sticky='w')
talent_var = tk.StringVar()
talent_dropdown = ttk.Combobox(root, textvariable=talent_var, values=talents_list)
talent_dropdown.grid(row=1, column=1)

# Entries for trait values and TaW/ZfW
trait_entries = []
for i in range(3):
    tk.Label(root, text=f"Trait {i+1} Value:").grid(row=2+i, column=0, sticky='w')
    trait_entry = tk.Entry(root)
    trait_entry.grid(row=2+i, column=1)
    trait_entries.append(trait_entry)

tk.Label(root, text="TaW/ZfW Value:").grid(row=5, column=0, sticky='w')
taw_zfw_entry = tk.Entry(root)
taw_zfw_entry.grid(row=5, column=1)

# Button to run prediction
predict_button = tk.Button(root, text="Predict", command=predict)
predict_button.grid(row=6, column=0, columnspan=2)

# Labels to show prediction results
success_label = tk.Label(root, text="Predicted Success: N/A")
success_label.grid(row=7, column=0, columnspan=2)
quality_label = tk.Label(root, text="Predicted Quality (TaP/ZfP): N/A")
quality_label.grid(row=8, column=0, columnspan=2)

# Run the GUI event loop
root.mainloop()
