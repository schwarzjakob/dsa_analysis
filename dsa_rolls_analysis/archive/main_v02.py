from datetime import datetime
import json
import csv
import re

class dsaStats(object):
	"""docstring for dsaStats"""
	def __init__(self, charakter: list):
		super(dsaStats, self).__init__()
		self.traits = ["MU", "KL", "IN", "CH", "FF", "GE", "KO", "KK"]
		self.traitsLong = ["Mut", "Klugheit", "Intuition", "Charisma", "Fingerfertigkeit", "Gewandtheit", "Konstitution", "Körperkraft"]
		self.charakter = charakter
		self.currentChar = ""
		self.charakterWithColon = self.charakterAddColon()
		self.totalTalentsDiced = []
		self.talentsFile = json.load(open('traits.json'))

	def charakterAddColon(self):
		charakterWithColon = []
		for char in self.charakter:
			charakterWithColon.append(char + ":")
		return charakterWithColon

	def currentCharCorrection(self):
		# Korrektur für anderweitige Usernames
		if self.currentChar == "Luisa B.":
			self.currentChar = "Walpurga Hausmännin"
		if self.currentChar == "Yannik F.":
			self.currentChar = "Bargaan Treuwall"
		if self.currentChar == "Niko K.":
			self.currentChar = "Elanor Walham"

	def talentsCurrection(self, potentialEvent: str) -> str:
		# Korrektur für falsche Talente
		if potentialEvent == "Sinnenschärfe":
			potentialEvent = "Sinnesschärfe"
		if potentialEvent == "Alchimie":
			potentialEvent = "Alchemie"
		if potentialEvent == "Fesseln":
			potentialEvent = "Fesseln/Entfesseln"
		if potentialEvent == "Überreden (Feilschen)":
			potentialEvent = "Überreden"
		if potentialEvent == "Fischenangeln":
			potentialEvent = "Fischen/Angeln"
		return potentialEvent


	def validateTrait(self, potentialTrait: str):
		if potentialTrait in self.traitsLong:
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

	# Ergebnis eines Wurfes auslesen und in Einzelteilen zurückgeben bspw. TaW
	def resultCheck(self, talentOrSpell: str, secondLine: str, thirdLine: str):
		
		# Wurfmodifikator
		currentMod = re.split(r' ', secondLine)[1]
		if "±" in currentMod:
			currentMod = currentMod.replace("±", "")
		currentMod = int(currentMod)

		# Wurferfolg
		currentSuccess = 0
		if "gelungen" in secondLine:
			currentSuccess = 1

		# Wurf TaP (Talentpunkte)/ ZfP (Zauberpunkte) /EP (Eigenschaftsprobe)
		if "automatisch" in secondLine and talentOrSpell == "trait":
			currentTaPZfP = int(re.split(r' EP\*\)\.', re.split(r'\(', secondLine)[2])[0])
		elif "automatisch" not in secondLine and talentOrSpell == "trait":
			currentTaPZfP = int(re.split(r' EP\*\)\.', re.split(r'\(', secondLine)[1])[0])
		if "automatisch" in secondLine and talentOrSpell == "talent":
			currentTaPZfP = int(re.split(r' TaP\*\)\.', re.split(r'\(', secondLine)[2])[0])
		elif "automatisch" not in secondLine and talentOrSpell == "talent":
			currentTaPZfP = int(re.split(r' TaP\*\)\.', re.split(r'\(', secondLine)[1])[0])
		if "automatisch" in secondLine and talentOrSpell == "spell":
			currentTaPZfP = int(re.split(r' ZfP\*\)\.', re.split(r'\(', secondLine)[2])[0])
		elif "automatisch" not in secondLine and talentOrSpell == "spell":
			currentTaPZfP = int(re.split(r' ZfP\*\)\.', re.split(r'\(', secondLine)[1])[0])

		# Wurfeigenschaften bspw.: KL/IN/IN = 14/15/15
		if talentOrSpell != "trait" :
			currentTraitLevel = re.split(r'/',(re.split(r'Eigenschaften: ', thirdLine))[1])
		
		#Wurf TaW (Talentwert) / ZfW (Zauberpunkte)
		if talentOrSpell == "trait":
			currentTaWZfW = int(re.split(r'EW: ', (re.split(r'Eigenschaften: ', thirdLine))[0])[1].replace(" ", ""))
		if talentOrSpell == "talent":
			currentTaWZfW = int(re.split(r'TaW: ', (re.split(r'Eigenschaften: ', thirdLine))[0])[1].replace(" ", ""))
		if talentOrSpell == "spell":
			currentTaWZfW = int(re.split(r'ZfW: ', (re.split(r'Eigenschaften: ', thirdLine))[0])[1].replace(" ", ""))


		#if "automatisch" in secondLine:
		# if talentOrSpell == "spell":
		# 	print("currentMod: ", currentMod, ", currentSuccess: ", currentSuccess, ", currentTaPZfP: ", currentTaPZfP, ", currentTaWZfW: ", currentTaWZfW, ", currentTraitLevel: ", currentTraitLevel)
		# 	print("currentMod: ", type(currentMod), ", currentSuccess: ", type(currentSuccess), ", currentTaPZfP: ", type(currentTaPZfP), ", currentTaWZfW: ", type(currentTaWZfW), ", currentTraitLevel: ", type(currentTraitLevel))
		if talentOrSpell == "trait":
			return currentMod, currentSuccess, currentTaPZfP, currentTaWZfW
		return currentMod, currentSuccess, currentTaPZfP, currentTaWZfW, int(currentTraitLevel[0]), int(currentTraitLevel[1]), int(currentTraitLevel[2])

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
		
	def attackResult(self, attack: str):
		pass

	def writeTotalTalentsDiced(self, rolledTalents: list):
		today = datetime.today().strftime('%Y-%m-%d')	
		with open(today+'_gerollte_Talente.csv', 'w', encoding='utf8') as file:
			writer = csv.writer(file)
			writer.writerow(["Held", "Kategorie", "Talent", "Eigenschaft 1", "Eigenschaft 2", "Eigenschaft 3", "Modifikator", "Erfolg", "TaP/ZfP", "TaW/ZfW", "Eigneschaftswert 1", "Eigenschaftswert 2", "Eigenschaftswert 3"])
			writer.writerows(rolledTalents)
		# for i in rolledTalents:
		#  	print(i)

	# Erstellt eine Excel/CSV Datei mit allen gewürfelten Talenten aller angegebnen Charaktere
	def main(self):
		#Dafür wird die chatLogFile geöffnet und die Lines ausgelesen und anschließen jede Line nach einem Charakter durchsucht um das folgende Talent festzustellen
		chatlogFile = open('2023-01-10_chatlog_dsa.txt', 'r')
		chatlogLines = chatlogFile.readlines()
		nonUsedLines = []

		for i in range(len(chatlogLines)):
			potentialEvent = chatlogLines[i].strip()
			if potentialEvent in self.charakterWithColon:
				self.currentChar = potentialEvent.replace(":", "")
				continue

			#Kontrolle ob ein Wurf von einem nicht vorhandenen Charakter geworfen wurde
			if self.currentChar == "":
				continue

			# Korrektur für anderweitige Usernames
			self.currentCharCorrection()

			#Korrektur für "  ()" hinter einem Talent (vielleicht Spezwurf?)
			if " ()" in potentialEvent:
				potentialEvent = potentialEvent.replace(" ()", "")

			# Korrektur für falsche Talente
			potentialEvent = self.talentsCurrection(potentialEvent)

			#Prüfe ob Eigenschaftsprobe stattgefunden hat
			if self.validateTrait(potentialEvent):
				currentMod, currentSuccess, currentTaPZfP, currentTaWZfW = self.traitResult(chatlogLines[i+1].strip(), chatlogLines[i+2].strip())			
				self.totalTalentsDiced.append([self.currentChar, "Eigenschaftsprobe", potentialEvent, self.traits[self.traitsLong.index(potentialEvent)], "#NULL!", "NULL!", currentMod, currentSuccess, currentTaPZfP, "NULL!", currentTaWZfW, "NULL!", "NULL!"])
				continue

			# Prüfe ob Talent geworfen wurde
			if self.validateTalent(potentialEvent):
				category, trait1, trait2, trait3 = self.getTraits("talent", potentialEvent)

				# Ergebnis des Wurfs prüfen 
				currentMod, currentSuccess, currentTaP, currentTaW, currentTrait1, currentTrait2, currentTrait3 = self.talentResult(chatlogLines[i+1].strip(), chatlogLines[i+2].strip())
				self.totalTalentsDiced.append([self.currentChar, category, potentialEvent, trait1, trait2, trait3, currentMod, currentSuccess, currentTaP, currentTaW, currentTrait1, currentTrait2, currentTrait3])
				continue

			# Prüfe on Zauber geworfen wurde
			if self.validateSpell(potentialEvent):
				category, trait1, trait2, trait3 = self.getTraits("spell", potentialEvent)

				# Ergebnis des Wurfs prüfen
				currentMod, currentSuccess, currentZfP, currentZfW, currentTrait1, currentTrait2, currentTrait3 = self.spellResult(chatlogLines[i+1].strip(), chatlogLines[i+2].strip())	
				self.totalTalentsDiced.append([self.currentChar, category, potentialEvent, trait1, trait2, trait3, currentMod, currentSuccess, currentZfP, currentZfW, currentTrait1, currentTrait2, currentTrait3])
				continue

			# Prüfe Angriff oder Fernkampfangriff
			if self.validateAttack(potentialEvent):
				pass

			# Prüfe Parade oder Ausweichmanöver


		# Verbleibende Einträge gegenchecken
			if "Talentprobe" in potentialEvent:
				continue
			if "Eigenschaftsprobe" in potentialEvent:
				continue
			if "Eigenschaften" in potentialEvent:
				continue
			if "Zauberprobe" in potentialEvent:
				continue
			nonUsedLines.append(potentialEvent)

		for i in nonUsedLines:
			print(i)

		self.writeTotalTalentsDiced(self.totalTalentsDiced)



if __name__ == '__main__':
	charakter = "Akira Masamune", "Hanzo Shimada", "Niko K.", "Elanor Walham", "Yannik F.", "Bargaan Treuwall", "Luisa B.", "Walpurga Hausmännin"
	myDSA = dsaStats(charakter)
	myDSA.main()