import json

# Load the JSON file
with open('traits.json', 'r') as f:
    data = json.load(f)

# Create a new object to store the categories
categories = {}

# Iterate through the talents in the file
for talent in data['talents']:
    category = talent['category']
    # If the category doesn't exist in the new object, create it
    if category not in categories:
        categories[category] = []
    # Remove the category key from the talent object
    del talent['category']
    # Add the talent object to the appropriate category
    categories[category].append(talent)
# Iterate through the talents in the file
for spell in data['spells']:
    category = spell['category']
    # If the category doesn't exist in the new object, create it
    if category not in categories:
        categories[category] = []
    # Remove the category key from the talent object
    del spell['category']
    # Add the talent object to the appropriate category
    categories[category].append(spell)


# Save the new object to a new JSON file
with open('output.json', 'w') as f:
    json.dump({"categories": categories}, f)
