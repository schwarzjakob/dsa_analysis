# Save this code as a script or integrate into an existing Python program
import pandas as pd

# Function to make predictions based on user input
def predict_outcome(hero, talent, trait1, trait2, trait3, TaW_ZfW, modificator=0):
    # Create a data frame for the input
    input_data = pd.DataFrame({
        'Held': [hero],
        'Kategorie': ['the_category_for_talent'],  # Replace with actual category if available
        'Talent': [talent],
        'Eigenschaft 1': [trait1],
        'Eigenschaft 2': [trait2],
        'Eigenschaft 3': [trait3],
        'Modifikator': [modificator],
        'TaW/ZfW': [TaW_ZfW],
        # Add 'Eigenschaftswert' columns with appropriate values if necessary
        # 'Eigenschaftswert 1': [value1],
        # 'Eigenschaftswert 2': [value2],
        # 'Eigenschaftswert 3': [value3],
    })

    # Use the model to make predictions
    success_prediction = pipeline_class.predict(input_data)
    quality_prediction = pipeline_reg.predict(input_data)

    # Print the predictions
    print("Predicted Success (1 for Erfolg, 0 for No Erfolg):", success_prediction[0])
    print("Predicted Quality (TaP/ZfP):", quality_prediction[0])

# Example usage:
# You need to provide the actual values for 'the_category_for_talent' and 'Eigenschaftswert' columns
# predict_outcome('Hanzo Shimada', 'Fährtensuchen', 'KL', 'IN', 'IN', 8)
