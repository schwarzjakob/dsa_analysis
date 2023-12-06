import pprint
# Using readlines()
chatlogFile = open('2022-08-14_ChatLog.txt', 'r')
chatlogLines = chatlogFile.readlines()

# Eigenschaften
attributes = {"MU": 0, "KL": 0, "IN": 0, "CH": 0, "FF": 0, "GE": 0, "KO": 0, "KK": 0}

# Talent-Kategorien
talents = {
	# Kategorie Körper
	"Körper": {
					"Athletik": ["GE", "KO", "KK", 0],
					"Klettern": ["MU", "GE", "KK", 0],
					"Körperbeherrschung": ["MU", "IN", "GE", 0],
					"Schleichen": ["MU", "IN", "GE", 0],
					"Schwimmen": ["GE", "KO", "KK", 0],
					"Selbstbeherrschung": ["MU", "KO", "KK", 0],
					"Sich verstecken": ["MU", "IN", "KK", 0],
					"Singen": ["IN", "CH", "CH", 0],
					"Sinnesschärfe": ["KL", "IN", "IN", 0],
					"Stimmenimitieren": ["KL", "IN", "CH", 0],
					"Tanzen": ["CH", "GE", "GE", 0],
					"Taschendiebstahl": ["MU", "IN", "FF", 0],
					"Zechen": ["IN", "KO", "KK", 0],
					"Akrobatik": ["MU", "GE", "KK", 0],
					"Fliegen": ["MU", "IN", "GE", 0],
					"Gaukeleien": ["MU", "CH", "FF", 0],
					"Reiten": ["CH", "GE", "KK", 0],
					"Skifahren": ["GE", "GE", "KK", 0],
					"Stimmenimitieren": ["KL", "IN", "CH", 0],
					"Taschendiebstahl": ["MU", "IN", "FF", 0]
	},

	# Kategorie Gesellschaft
	"Gesellschaft": {
					
					"Betören": ["IN", "CH", "CH", 0],
					"Etikette": ["KL", "IN", "CH", 0],
					"Gassenwissen": ["KL", "IN", "CH", 0],
					"Lehren": ["KL", "IN", "CH", 0],
					"Menschenkenntnis": ["KL", "IN", "CH", 0],
					"Schauspielerei": ["MU", "KL", "IN", 0],
					"Schriftlicher Ausdruck": ["KL", "IN", "IN", 0],
					"Sich Verkleiden": ["MU", "CH", "GE", 0],
					"Überreden": ["MU", "IN", "CH", 0],
					"Überzeugen": ["KL", "IN", "CH", 0],
	},
	# Kategorie Natur
	"Natur": {
					"Fährtensuchen": ["KL", "IN", "IN", 0],
					"Fallenstellen": ["KL", "FF", "KK", 0],
					"Fesseln/Entfesseln": ["FF", "GE", "KK", 0],
					"Fischen/Angeln": ["IN", "FF", "KK", 0],
					"Orientierung": ["KL", "IN", "IN", 0],
					"Wettervorhersage": ["KL", "IN", "IN", 0],
					"Wildnisleben": ["IN", "GE", "KO", 0]
	},
	# Kategorie Wissen
	"Wissen": {
					"Anatomie": ["MU", "KL", "FF", 0],
					"Baukunst": ["KL", "KL", "FF", 0],
					"Brett- /Kartenspiel": ["KL", "KL", "IN", 0],
					"Geographie": ["KL", "KL", "IN", 0],
					"Geschichtswissen": ["KL", "KL", "IN", 0],
					"Gesteinskunde": ["KL", "IN", "FF", 0],
					"Götter/Kulte": ["KL", "KL", "IN", 0],
					"Heraldik": ["KL", "KL", "FF", 0],
					"Hüttenkunde": ["KL", "IN", "KO", 0],
					"Kriegskunst": ["MU", "KL", "CH", 0],
					"Kryptographie": ["KL", "KL", "IN", 0],
					"Magiekunde": ["KL", "KL", "IN", 0],
					"Mechanik": ["KL", "KL", "FF", 0],
					"Pflanzenkunde": ["KL", "IN", "FF", 0],
					"Philosophie": ["KL", "KL", "IN", 0],
					"Rechnen": ["KL", "KL", "IN", 0],
					"Rechtskunde": ["KL", "KL", "IN", 0],
					"Sagen/Legenden": ["KL", "IN", "CH", 0],
					"Schätzen": ["KL", "IN", "IN", 0],
					"Sprachenkunde": ["KL", "KL", "IN", 0],
					"Staatskunst": ["KL", "IN", "CH", 0],
					"Sternkunde": ["KL", "KL", "IN", 0],
					"Tierkunde": ["MU", "KL", "IN", 0]
	},
	# Kategorie Handwerk
	"Handwerk": {
					"Abrichten": ["MU", "IN", "CH", 0],
					"Ackerbau": ["IN", "FF", "KO", 0],
					"Alchemie": ["MU", "KL", "FF", 0],
					"Bergbau": ["IN", "KO", "KK", 0],
					"Bogenbau": ["KL", "IN", "FF", 0],
					"Bootefahren": ["GE", "KO", "FF", 0],
					"Brauer": ["KL", "FF", "KK", 0],
					"Drucker": ["KL", "FF", "KK", 0],
					"Fahrzeuglenken": ["IN", "CH", "FF", 0],
					"Falschspiel": ["MU", "CH", "FF", 0],
					"Feinmechanik": ["KL", "FF", "FF", 0],
					"Feuersteinbearbeitung": ["KL", "FF", "FF", 0],
					"Fleischer": ["KL", "FF", "KK", 0],
					"Gerber/Kürschner": ["KL", "FF", "KO", 0],
					"Glaskunst": ["FF", "FF", "KO", 0],
					"Grobschmied": ["FL", "KO", "KK", 0],
					"Handel": ["KL", "IN", "CH", 0],
					"Hauswirstschaft": ["IN", "CH", "FF", 0],
					"Heilkunde Gift": ["MU", "KL", "IN", 0],
					"Heilkunde Krankheiten": ["MU", "KL", "CH", 0],
					"Heilkunde Seele": ["IN", "CH", "CH", 0],
					"Heilkunde Wunden": ["KL", "CH", "FF", 0],
					"Holzbearbeitung": ["KL", "FF", "KK", 0],
					"Instrumentenbauer": ["KL", "IN", "FF", 0],
					"Kartopgraphie": ["KL", "KL", "FF", 0],
					"Kochen": ["KL", "IN", "FF",0 ],
					"Kristallzuch": ["KL", "IN", "FF", 0],
					"Maurer": ["FF", "GE", "KK", 0],
					"Metallguss": ["KL", "FF", "KK", 0],
					"Musizieren": ["IN", "CH", "FF", 0],
					"Schlösser knacken": ["IN", "FF", "FF", 0],
					"Schnapsbrennen": ["KL", "IN", "FF", 0],
					"Seefahrt": ["FF", "GE", "KK", 0],
					"Seiler": ["FF", "FF", "KK", 0],
					"Steinmetz": ["FF", "FF", "KK", 0],
					"Steinscheider/Juwelier": ["IN", "FF", "FF", 0],
					"Stellmacher": ["KL", "FF", "KK", 0],
					"Stoffefärben": ["KL", "FF", "KK", 0],
					"Tätowieren": ["IN", "FF", "FF", 0],
					"Töpfern": ["KL", "FF", "FF", 0],
					"Viehzucht": ["KL", "IN", "KK", 0],
					"Webkunst": ["FF", "FF", "KK", 0],
					"Winzer": ["KL", "FF", "KK", 0],
					"Zimmermann": ["KL", "FF", "KK", 0],
	},
	# Kategorie Gaben
	"Gaben": {
					"Gefahreninstinkt": ["KL", "IN", "IN", 0]
	}
}

spells = {
	# Zauber
	"Zauber": {
					
	}
}

def iterateDict(myDict, talent):
	for k, v in myDict.items():
		if isinstance(v, dict):
			iterateDict(v, talent)
		else:
			if k == talent:
				for i in v:

					# Anzahl Würfe zählen: Athletik ['GE', 'KO', 'KK', 2]
					if type(i) is int:
						v[3] += 1
						continue
					attributes[i] = attributes[i]+1 

def iterateDict2(myDict):
	for k,v in myDict.items():
		if isinstance(v, dict):
			print("\n", k,"\n")
			iterateDict2(v)
		elif v[3] > 0:
			print("{:<25} {:<10} {:<15}".format(k, v[3], "mal gewürfelt"))



def countAttributes(charakter):
	
	for i in range(len(chatlogLines)-1):
		if chatlogLines[i].strip() == charakter + ":":
			talent = chatlogLines[i+1].strip()
			iterateDict(talents, talent)


	sortAttributes = sorted(attributes.items(), key=lambda x: x[1], reverse=True)
	for a in sortAttributes:
		print("{:<5} {:<5} {:<15}".format(a[0], a[1], "mal gewürfelt"))
	print("\n")




if __name__ == '__main__':
	charakter = "Akira Masamune"
	print(charakter + ": \n" )
	countAttributes(charakter)
	iterateDict2(talents)


