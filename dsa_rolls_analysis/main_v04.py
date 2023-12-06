import json
import csv
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple

# Constants
TRAITS_SHORT = ["MU", "KL", "IN", "CH", "FF", "GE", "KO", "KK"]
TRAITS_LONG = ["Mut", "Klugheit", "Intuition", "Charisma", "Fingerfertigkeit", "Gewandtheit", "Konstitution", "Körperkraft"]
USER_NAME_CORRECTIONS = {
    "Luisa B.": "Walpurga Hausmännin",
    "Yannik F.": "Bargaan Treuwall",
    "Niko K.": "Elanor Walham",
    "Walpurga Hausmännin (Walla Burija Sabu Hasmanin)": "Walpurga Hausmännin"
}
TALENT_CORRECTIONS = {
    "Sinnenschärfe": "Sinnesschärfe",
    "Alchimie": "Alchemie",
    "Fesseln": "Fesseln/Entfesseln",
    "Überreden (Feilschen)": "Überreden",
    "Fischenangeln": "Fischen/Angeln"
}

class DsaStats:
    def __init__(self, characters: List[str]):
        self.characters = characters
        self.current_char = ""
        self.characters_with_colon = [char + ":" for char in characters]
        self.talents_file = json.load(open('talents.json'))
        self.rolls = {
            "Eigenschaftsprobe": [],
            "Talent": [],
            "Zauber": [],
            "Kampfprobe": [],
            "Initiative": []
        }
        self.total_dmg = {char: 0 for char in characters}

    def correct_user_name(self, username: str) -> str:
        return USER_NAME_CORRECTIONS.get(username, username)

    def correct_talent(self, talent: str) -> str:
        return TALENT_CORRECTIONS.get(talent, talent)

    def validate_item(self, item: str, category: str) -> bool:
        for entry in self.talents_file[category]:
            if entry[category[:-1]] == item:
                return True
        return False

    def parse_roll_result(self, line: str, roll_type: str) -> Tuple[int, int, int, int, List[int]]:
        # Parse the result based on the roll type
        # ...

    def add_roll_entry(self, category: str, event: str, second_line: str, third_line: str):
        mod, success, ta_p_zfp, ta_w_zfw, trait_levels = self.parse_roll_result(event, category)
        entry = [self.current_char, category, event, *trait_levels, mod, success, ta_p_zfp, ta_w_zfw]
        self.rolls[category].append(entry)

    def read_chat_log(self, filepath: str):
        with open(filepath, 'r') as file:
            lines = file.readlines()

        for i, line in enumerate(lines):
            line = line.strip()
            if line in self.characters_with_colon:
                self.current_char = self.correct_user_name(line.replace(":", ""))
                continue

            if not self.current_char:
                continue

            line = self.correct_talent(line)

            if self.validate_item(line, "talents"):
                self.add_roll_entry("Talent", line, lines[i+1], lines[i+2])
            elif self.validate_item(line, "spells"):
                self.add_roll_entry("Zauber", line, lines[i+1], lines[i+2])
            # Add checks for other categories...

    def save_rolls_to_files(self, folder: str):
        Path(folder).mkdir(exist_ok=True)
        for category, data in self.rolls.items():
            filename = f"{folder}/{datetime.today().strftime('%Y-%m-%d')}_{category}.csv"
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Held", "Kategorie", "Event", "Trait 1", "Trait 2", "Trait 3", "Modifikator", "Erfolg", "TaP/ZfP", "TaW/ZfW"])
                writer.writerows(data)

if __name__ == '__main__':
    characters = ["Akira Masamune", "Hanzo Shimada", "Niko K.", "Elanor Walham", "Yannik F.", "Bargaan Treuwall", "Luisa B.", "Walpurga Hausmännin"]
    myDSA = DsaStats(characters)
    myDSA.read_chat_log('231110_chatlog.txt')
    myDSA.save_rolls_to_files('dsa_rolls')
