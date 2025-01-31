# services/chat_log_processing/chat_log_event_validator.py
import logging

# For example, your known trait names, short or long
TRAITS_LONG = [
    "Mut",
    "Klugheit",
    "Intuition",
    "Charisma",
    "Fingerfertigkeit",
    "Gewandtheit",
    "Konstitution",
    "Körperkraft",
]

# We can keep a dictionary for known corrections
TALENT_CORRECTIONS = {
    "Sinnenschärfe": "Sinnesschärfe",
    "Alchimie": "Alchemie",
    "Fesseln": "Fesseln/Entfesseln",
    "Überreden (Feilschen)": "Überreden",
    "Fischenangeln": "Fischen/Angeln",
}


class ChatLogEventValidator:
    """
    Classifies an individual line (or set of lines) to see what kind
    of event it might represent: trait, talent, spell, attack, damage, etc.
    """

    def __init__(self, characters_and_aliases, talents, spells, attacks):
        """
        :param characters_and_aliases: List of character names and aliases
        :param talents: Set of valid talent names
        :param spells: Set of valid spell names
        :param attacks: Set of valid attack names
        """
        self.logger = logging.getLogger(__name__)
        self.characters_and_aliases = characters_and_aliases
        self.known_talents = talents
        self.known_spells = spells
        self.known_attacks = attacks

    def determine_event_type(self, line: str):
        """
        Given a single line from the chatlog, determine what kind of event it represents.
        """
        # 1) Is this line a character switch? (like "Alrik:")
        if line in (character + ":" for character in self.characters_and_aliases):
            return "character"

        # 2) Correct any known spelling differences
        line = TALENT_CORRECTIONS.get(line, line)

        # 3) If it's a trait from TRAITS_LONG
        if line in TRAITS_LONG:
            return "trait"

        # 4) If it is a known Talent
        if line in self.known_talents:
            return "talent"

        # 5) If it is a known Spell
        if line in self.known_spells:
            return "spell"

        # 6) If it is a known Attack
        if line in self.known_attacks:
            return "attack"

        # 7) If it's initiative
        if "Initiative" in line and "Initiativewurf" not in line:
            return "initiative"

        # 8) If it's damage
        if "treffer" in line.lower():
            return "damage"

        # 9) Otherwise, not recognized
        return None
