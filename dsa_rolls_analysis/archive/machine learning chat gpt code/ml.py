# Save this code as a module, e.g., 'dsa_ml_model.py'
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split

# Load your dataset here (the path might need to be adjusted)
file_path = '/Users/jakobschwarz/Documents/Coding/Python/DSA rolls/2023-11-10_gerollte_Talente.csv'
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
