import json
import os

TALENTS_JSON_PATH = os.path.join('.', 'dsa_analysis_app', 'data', 'json', 'talents.json')

def get_talents_json():
    with open(TALENTS_JSON_PATH, 'r') as f:
        talents_json = json.load(f)
    return talents_json

def get_traits_for_selected_talents(talents_name_list):
    print(talents_name_list)
    talents_json = get_talents_json()
    #print(talents_json)
    trait_counts = {"MU": 0, "KL": 0, "IN": 0, "CH": 0, "FF": 0, "GE": 0, "KO": 0, "KK": 0}
    for talent_name in talents_name_list:
        # Find the talent in the list
        talent = next((talent for talent in talents_json["talents"] if talent["talent"] == talent_name), None)
        if talent:
            # Update trait counts
            trait_counts[talent["trait1"]] += 1
            trait_counts[talent["trait2"]] += 1
            trait_counts[talent["trait3"]] += 1
        else:
            print("Talent {} not found in talents.json".format(talent_name))

    return trait_counts
        

if __name__ == "__main__":
    app.run(debug=True)