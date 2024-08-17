# flask-server/dsa_analysis_app/chat_processing/chat_log_parser.py
import json
import csv
import re
from datetime import datetime
import os
import argparse
import logging

# Enabling logging (must come first to enable it globally, also for imported modules and packages)
logger_format = "[%(asctime)s %(filename)s->%(funcName)s():%(lineno)d] %(levelname)s: %(message)s"
logging.basicConfig(format=logger_format, level=logging.DEBUG)
logger = logging.getLogger(__name__)

today = datetime.today().strftime('%y%m%d')

# Define base directory and constants for file paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CHARACTERS_JSON_PATH = os.path.join(BASE_DIR, 'data', 'json', 'characters.json')
TALENTS_JSON_PATH = os.path.join(BASE_DIR, 'data', 'json', 'talents.json')
USER_CORRECTIONS_JSON_PATH = os.path.join(BASE_DIR, 'data', 'json', 'user_corrections.json')
TALENT_CORRECTIONS_JSON_PATH = os.path.join(BASE_DIR, 'data', 'json', 'talent_corrections.json')
TRAITS = ["MU", "KL", "IN", "CH", "FF", "GE", "KO", "KK"]
TRAITS_LONG = ["Mut", "Klugheit", "Intuition", "Charisma", "Fingerfertigkeit", "Gewandtheit", "Konstitution", "Körperkraft"]


class DsaStats:
    def __init__(self):
        super(DsaStats, self).__init__()
        with open(CHARACTERS_JSON_PATH, 'r') as file:
            users_data = json.load(file)
        self.characters = {char["name"]: char["alias"] for char in users_data["characters"]}
        self.currentChar = ""

        self.charactersWithColon = []
        for char_name, aliases in self.characters.items():
            self.charactersWithColon.append(char_name + ":")
            for alias in aliases:
                self.charactersWithColon.append(alias + ":")

        with open(TALENTS_JSON_PATH, 'r') as file:
            self.talentsFile = json.load(file)
        with open(TALENT_CORRECTIONS_JSON_PATH, 'r') as file:
            self.talent_corrections = json.load(file)
        self.traitsRolls = []
        self.talentsRolls = []
        self.spellsRolls = []
        self.attacksRolls = []
        self.initiativesRolls = []
        self.totalDmg = {char: 0 for char in self.characters}
        self.traitUsageCounts = {char: {trait: 0 for trait in TRAITS} for char in self.characters}
        self.traitValues = {char: {trait: 0 for trait in TRAITS} for char in self.characters}

        self.directoryDateDependent = os.path.join(BASE_DIR, 'data', 'rolls_results', f'{today}_rolls_results')
        self.directoryRecent = os.path.join(BASE_DIR, 'data', 'rolls_results', '000000_rolls_results_recent')


    # retrieved chatlog parsing
    def process_chatlog(self, chatlog_path):
        with open(chatlog_path, 'r') as chatlogFile:
            chatlogLines = chatlogFile.readlines()
        return chatlogLines

    # Esnure the directory for result files exist or is created
    def ensure_directories(self):
        # Create directories if they don't exist
        if not os.path.exists(self.directoryDateDependent):
            os.makedirs(self.directoryDateDependent)
        if not os.path.exists(self.directoryRecent):
            os.makedirs(self.directoryRecent)

    def currentCharCorrection(self):
    # Iterate through each character and their aliases
        for char_name, aliases in self.characters.items():
            if self.currentChar in aliases:
                return char_name
        return self.currentChar


    def talentsCurrection(self, talent):
        return self.talent_corrections.get(talent, talent)

    # Potential event cleanup functions
    def validate_item(self, item, category):
        for entry in self.talents_file[category]:
            if entry[category[:-1]] == item:
                return True
        return False

    def validateTrait(self, potentialTrait: str):
        if potentialTrait in TRAITS_LONG:
            return True
        return False

    def validateTalent(self, potentialTalent: str):
        for i in self.talentsFile["talents"]:
            if i["talent"] == potentialTalent:
                return True
        return False

    def validateSpell(self, potentialSpell: str):
        for i in self.talentsFile["spells"]:
            if i["spell"] == potentialSpell:
                return True
        return False

    def validateAttack(self, potentialAttack: str):
        for i in self.talentsFile["attacks"]:
            if i["attack"] == potentialAttack:
                return True
        return False

    # In den talents nach gewürfeltem Talent suchen
    def getTraits(self,talentOrSpell: str, talent: str):
        for k in self.talentsFile[talentOrSpell+"s"]:
            if k[talentOrSpell] == talent:
                return k["category"], k["trait1"], k["trait2"], k["trait3"]

    def updateTraitUsage(self, character, traits):
        # If it was a specific trait roll, then it's not an array but only a string representing on trait to add
        if traits in TRAITS:
            self.traitUsageCounts[character][traits] += 1
        # for talents, and spell rolls an array with the 3 traits needs to be added
        else:
            for trait in traits:
                if trait in TRAITS:
                    self.traitUsageCounts[character][trait] += 1

    def updateTraitValues(self, character, traits, traitValues):
        for trait in traits:
            self.traitValues[character][trait] = traitValues[traits.index(trait)]

    def modAndSuccessCheck(self, secondLine: str):
        # Wurfmodifikator
        currentMod = re.split(r' ', secondLine)[1]
        if "±" in currentMod:
            currentMod = currentMod.replace("±", "")
        currentMod = int(currentMod)

        # Wurferfolg
        currentSuccess = 0
        if "gelungen" in secondLine:
            currentSuccess = 1

        return currentSuccess, currentMod

    def talentResult(self, secondLine: str, thirdLine: str):
        # Wurfmodifikator und Wurferfolg checken
        currentSuccess, currentMod = self.modAndSuccessCheck(secondLine)

        # Wurf TaP (Talentpunkte)/ ZfP (Zauberpunkte) /EP (Eigenschaftsprobe)
        if "automatisch" in secondLine:
            currentTaPZfP = int(re.split(r' TaP\*\)\.', re.split(r'\(', secondLine)[2])[0])
        elif "automatisch" not in secondLine:
            currentTaPZfP = int(re.split(r' TaP\*\)\.', re.split(r'\(', secondLine)[1])[0])
        
        # Wurfeigenschaften bspw.: KL/IN/IN = 14/15/15
        currentTraitLevel = re.split(r'/',(re.split(r'Eigenschaften: ', thirdLine))[1])

        #Wurf TaW (Talentwert) / ZfW (Zauberpunkte)     
        currentTaWZfW = int(re.split(r'TaW: ', (re.split(r'Eigenschaften: ', thirdLine))[0])[1].replace(" ", ""))

        return currentMod, currentSuccess, currentTaPZfP, currentTaWZfW, int(currentTraitLevel[0]), int(currentTraitLevel[1]), int(currentTraitLevel[2])

    def spellResult(self, secondLine: str, thirdLine: str):
        # Wurfmodifikator und Wurferfolg checken
        currentSuccess, currentMod = self.modAndSuccessCheck(secondLine)

        # Wurf TaP (Talentpunkte)/ ZfP (Zauberpunkte) /EP (Eigenschaftsprobe)   
        if "automatisch" in secondLine:
            currentTaPZfP = int(re.split(r' ZfP\*\)\.', re.split(r'\(', secondLine)[2])[0])
        elif "automatisch" not in secondLine:
            currentTaPZfP = int(re.split(r' ZfP\*\)\.', re.split(r'\(', secondLine)[1])[0])

        # Wurfeigenschaften bspw.: KL/IN/IN = 14/15/15
        currentTraitLevel = re.split(r'/',(re.split(r'Eigenschaften: ', thirdLine))[1])

        #Wurf TaW (Talentwert) / ZfW (Zauberpunkte)
        currentTaWZfW = int(re.split(r'ZfW: ', (re.split(r'Eigenschaften: ', thirdLine))[0])[1].replace(" ", ""))

        return currentMod, currentSuccess, currentTaPZfP, currentTaWZfW, int(currentTraitLevel[0]), int(currentTraitLevel[1]), int(currentTraitLevel[2])

    def traitResult(self, secondLine: str,thirdLine: str):
        # Wurfmodifikator und Wurferfolg checken
        currentSuccess, currentMod = self.modAndSuccessCheck(secondLine)

        # Wurf TaP (Talentpunkte)/ ZfP (Zauberpunkte) /EP (Eigenschaftsprobe)
        if "automatisch" in secondLine:
            currentTaPZfP = int(re.split(r' EP\*\)\.', re.split(r'\(', secondLine)[2])[0])
        elif "automatisch" not in secondLine:
            currentTaPZfP = int(re.split(r' EP\*\)\.', re.split(r'\(', secondLine)[1])[0])
        
        #Wurf TaW (Talentwert) / ZfW (Zauberpunkte)
        currentTaWZfW = int(re.split(r'EW: ', (re.split(r'Eigenschaften: ', thirdLine))[0])[1].replace(" ", ""))

        return currentMod, currentSuccess, currentTaPZfP, currentTaWZfW
        
    def attackResult(self, secondLine: str,thirdLine: str):
        # Wurfmodifikator
        currentMod = re.split(r' ', secondLine)[1]
        if "±" in currentMod:
            currentMod = currentMod.replace("±", "")
        currentMod = int(currentMod)


        #Wurf TaW (Talentwert) / ZfW (Zauberpunkte)
        # Improved parsing for currentTaWZfW
        try:
            # Extract the numeric value after 'AT-Wert:', 'PA-Wert:', etc.
            currentTaWZfW = int(re.search(r'(\d+)', thirdLine).group())
        except (ValueError, AttributeError):
            print(f"Error parsing TaW/ZfW in line: {thirdLine}")
            currentTaWZfW = 0

        # Wurf TaP (Talentpunkte)/ ZfP (Zauberpunkte) /EP (Eigenschaftsprobe)
        currentTaPZfP = currentTaWZfW - int(re.split(r'\)\.', re.split(r'\(', secondLine)[1])[0]) - currentMod

        currentSuccess = 1
        if currentTaPZfP < 0:
            currentSuccess = 0

        return currentMod, currentSuccess, currentTaPZfP, currentTaWZfW

    def initativeResult(self, firstLine: str, secondLine: str):
        rolledIni = int(re.split(r' ', firstLine)[4])
        currentIni = int(re.split(r' ', secondLine)[2].replace("\tBE:","").replace("\tBE:\tMod.:","").replace("\tMod.:",""))
        currentMod = int(re.split(r' ', secondLine)[-1])
        return currentIni, rolledIni, currentMod

    def writeTraitUsageCounts(self):
        # Creates files with trait usage counts for the current Day
        # with open(self.directoryDateDependent + f'{today}_trait_usage.csv', 'w', newline='', encoding='utf8') as file:
        #     writer = csv.writer(file)
        #     writer.writerow(["Character"] + TRAITS)
        #     for char, counts in self.traitUsageCounts.items():
        #         writer.writerow([char] + [counts[trait] for trait in TRAITS])

        with open(os.path.join(self.directoryRecent, 'trait_usage.csv'), 'w', newline='', encoding='utf8') as file:
            writer = csv.writer(file)
            writer.writerow(["Character"] + TRAITS)
            for char, counts in self.traitUsageCounts.items():
                try:
                    writer.writerow([char] + [counts[int(trait)] for trait in TRAITS])
                except ValueError:
                    writer.writerow([char] + [counts[trait] for trait in TRAITS])

    def writeTraitValues(self):
        # Creates files with trait values for the current Day
        # with open(self.directoryDateDependent + f'{today}_trait_values.csv', 'w', newline='', encoding='utf8') as file:
        #     writer = csv.writer(file)
        #     writer.writerow(["Character"] + TRAITS)
        #     for char, value in self.traitValues.items():
        #         writer.writerow([char] + [value[trait] for trait in TRAITS])

        with open(os.path.join(self.directoryRecent, 'trait_values.csv'), 'w', newline='', encoding='utf8') as file:
            writer = csv.writer(file)
            writer.writerow(["Character"] + TRAITS)
            for char, value in self.traitValues.items():
                try:
                    writer.writerow([char] + [value[int(trait)] for trait in TRAITS])
                except ValueError:
                    writer.writerow([char] + [value[trait] for trait in TRAITS])

    def writeRollsToFile(self, rolls, rollType, filename):
        try:
            # Write to the recent directory
            recent_file_path = os.path.join(self.directoryRecent, f'{rollType}.csv')
            with open(recent_file_path, 'w', newline='', encoding='utf8') as file:
                writer = csv.writer(file)
                self.write_rolls(writer, rolls, rollType)
            logger.debug(f"{rollType.capitalize()} rolls successfully written to {recent_file_path}")
            # Write to the date-dependent directory
            dated_file_path = os.path.join(self.directoryDateDependent, filename)

            with open(dated_file_path, 'w', newline='', encoding='utf8') as file:
                writer = csv.writer(file)
                self.write_rolls(writer, rolls, rollType)
            
            logger.debug(f"{rollType.capitalize()} rolls successfully written to {dated_file_path}")
        
        except Exception as e:
            logger.error(f"Error writing {rollType} rolls to file: {e}")

    def write_rolls(self, writer, rolls, rollType):
        if rollType == 'traits':
            writer.writerow(["Character", "Category", "Talent", "Eigenschaft 1", "Modifikator", "Erfolg", "TaP/ZfP", "TaW/ZfW"])
            writer.writerows(rolls)
        elif rollType == 'talents' or rollType == 'spells':
            writer.writerow(["Character", "Category", "Talent", "Eigenschaft 1", "Eigenschaft 2", "Eigenschaft 3", "Modifikator", "Erfolg", "TaP/ZfP", "TaW/ZfW", "Eigenschaftswert 1", "Eigenschaftswert 2", "Eigenschaftswert 3"])
            writer.writerows(rolls)
        elif rollType == 'attacks':
            writer.writerow(["Character", "Category", "Talent", "Modifikator", "Erfolg", "TaP/ZfP", "TaW/ZfW"])
            writer.writerows(rolls)
        elif rollType == 'initiative':
            writer.writerow(["Character", "Category", "Talent", "Modifikator", "TaP/ZfP", "TaW/ZfW"])
            writer.writerows(rolls)
        else:
            logger.debug(f'No database for {rollType} rolls')
            
    def countDmg(self, secondLine: str):
        currentDmg = int(re.split(r' ', secondLine)[0])
        self.totalDmg[self.currentChar] += currentDmg


    # Erstellt eine Excel/CSV Datei mit allen gewürfelten Talenten aller angegebnen Charaktere
    def main(self, chatlogLines):

        self.ensure_directories()
        #Dafür wird die chatLogFile geöffnet und die Lines ausgelesen und anschließen jede Line nach einem Charakter durchsucht um das folgende Talent festzustellen
        nonUsedLines = []

        for i in range(len(chatlogLines)):
            potentialEvent = chatlogLines[i].strip()
            if potentialEvent in self.charactersWithColon:
                self.currentChar = potentialEvent.replace(":", "")
                continue

            #Kontrolle ob ein Wurf von einem nicht vorhandenen Charakter geworfen wurde
            if self.currentChar == "":
                continue

            # Korrektur für anderweitige Usernames
            self.currentChar = self.currentCharCorrection()

            #Korrektur für "  ()" hinter einem Talent (vielleicht Spezwurf?)
            if " ()" in potentialEvent:
                potentialEvent = potentialEvent.replace(" ()", "")

            # Korrektur für falsche Talente
            potentialEvent = self.talentsCurrection(potentialEvent)

            #Prüfe ob Eigenschaftsprobe stattgefunden hat
            if self.validateTrait(potentialEvent):
                currentMod, currentSuccess, currentTaPZfP, currentTaWZfW = self.traitResult(chatlogLines[i+1].strip(), chatlogLines[i+2].strip())           
                self.traitsRolls.append([self.currentChar, "Eigenschaftsprobe", potentialEvent, TRAITS[TRAITS_LONG.index(potentialEvent)], currentMod, currentSuccess, currentTaPZfP, currentTaWZfW])
                self.updateTraitUsage(self.currentChar, TRAITS[TRAITS_LONG.index(potentialEvent)])
                continue

            # Prüfe ob Talent geworfen wurde
            if self.validateTalent(potentialEvent):
                category, trait1, trait2, trait3 = self.getTraits("talent", potentialEvent)

                # Ergebnis des Wurfs prüfen 
                currentMod, currentSuccess, currentTaP, currentTaW, currentTrait1, currentTrait2, currentTrait3 = self.talentResult(chatlogLines[i+1].strip(), chatlogLines[i+2].strip())
                self.talentsRolls.append([self.currentChar, category, potentialEvent, trait1, trait2, trait3, currentMod, currentSuccess, currentTaP, currentTaW, currentTrait1, currentTrait2, currentTrait3])
                self.updateTraitUsage(self.currentChar, [trait1, trait2, trait3])
                try:
                    self.updateTraitValues(self.currentChar, [trait1, trait2, trait3], [currentTrait1, currentTrait2, currentTrait3])
                except Exception as error:
                    print(error)
                    
                continue

            # Prüfe on Zauber geworfen wurde
            if self.validateSpell(potentialEvent):
                category, trait1, trait2, trait3 = self.getTraits("spell", potentialEvent)

                # Ergebnis des Wurfs prüfen
                currentMod, currentSuccess, currentZfP, currentZfW, currentTrait1, currentTrait2, currentTrait3 = self.spellResult(chatlogLines[i+1].strip(), chatlogLines[i+2].strip())    
                self.spellsRolls.append([self.currentChar, category, potentialEvent, trait1, trait2, trait3, currentMod, currentSuccess, currentZfP, currentZfW, currentTrait1, currentTrait2, currentTrait3])
                self.updateTraitUsage(self.currentChar, [trait1, trait2, trait3])
                self.updateTraitValues(self.currentChar, [trait1, trait2, trait3], [currentTrait1, currentTrait2, currentTrait3])
                continue

            # Prüfe Nahkampfangriff, Fernkampfangriff, Parade oder Ausweichmanöver
            if self.validateAttack(potentialEvent):
                thirdLine = chatlogLines[i+2].strip()
                if "Kampfgetümmel" in chatlogLines[i+2].strip():
                    thirdLine = chatlogLines[i+3].strip()

                #self.attackResult(chatlogLines[i+1].strip(), thirdLine)
                currentMod, currentSuccess, currentTaPZfP, currentTaWZfW = self.attackResult(chatlogLines[i+1].strip(), thirdLine)
                self.attacksRolls.append([self.currentChar, "Kampfprobe", potentialEvent, currentMod, currentSuccess, currentTaPZfP, currentTaWZfW])
                continue

            # Prüfe Initiativewurf
            if "Initiative" in potentialEvent and not "Initiativewurf" in potentialEvent and self.currentChar in potentialEvent:
                currentIni, rolledIni, currentMod = self.initativeResult(chatlogLines[i].strip(), chatlogLines[i+1].strip())
                self.initiativesRolls.append([self.currentChar, "Initiative", "Initiative", currentMod, rolledIni, currentIni])
                continue

            if "treffer" in potentialEvent:
                self.countDmg(chatlogLines[i+1].strip())
                continue


            # Prüfe Parade oder Ausweichmanöver

        # After processing all lines, write the results to files
        try:
            self.writeTraitValues()
        except Exception as error:
            print(error)
        self.writeTraitUsageCounts()
        self.writeRollsToFile(self.traitsRolls, 'traits', f'{today}_traits_rolls.csv')
        self.writeRollsToFile(self.talentsRolls, 'talents', f'{today}_talents_rolls.csv')
        self.writeRollsToFile(self.spellsRolls, 'spells', f'{today}_spells_rolls.csv')
        self.writeRollsToFile(self.attacksRolls, 'attacks', f'{today}_attacks_rolls.csv')
        self.writeRollsToFile(self.initiativesRolls, 'initiative', f'{today}_initiatives_rolls.csv')

if __name__ == "__main__":
    app.run(debug=True)