# services/chat_log_processing/chat_log_event_validator.py
import logging
import re

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

    def __init__(self, db_cursor, known_characters_with_colon):
        """
        :param db_cursor: a DB cursor or a DB service that we can use
                          to check if a name is a recognized talent/spell/etc.
        :param known_characters_with_colon: e.g. ['Alrik:', 'Andergast:', ...]
        """
        self.logger = logging.getLogger(__name__)
        self.cursor = db_cursor
        self.known_characters_with_colon = known_characters_with_colon

    def _validate_talent_in_db(self, potential_talent: str) -> bool:
        """
        Check if a talent with this name exists in the 'talents' table.
        """
        try:
            self.cursor.execute(
                "SELECT 1 FROM talents WHERE talent_name = %s LIMIT 1",
                (potential_talent,),
            )
            return self.cursor.fetchone() is not None
        except Exception:
            return False

    def _validate_spell_in_db(self, potential_spell: str) -> bool:
        """
        Check if a spell with this name exists in the 'spells' table.
        """
        try:
            self.cursor.execute(
                "SELECT 1 FROM spells WHERE spell_name = %s LIMIT 1",
                (potential_spell,),
            )
            return self.cursor.fetchone() is not None
        except Exception:
            return False

    def _validate_attack_in_db(self, potential_attack: str) -> bool:
        """
        Check if an attack with this name exists in the 'attacks' table.
        """
        try:
            self.cursor.execute(
                "SELECT 1 FROM attacks WHERE attack_name = %s LIMIT 1",
                (potential_attack,),
            )
            return self.cursor.fetchone() is not None
        except Exception:
            return False

    def determine_event_type(self, line: str):
        """
        Given a single line from the chatlog,
        returns one of the recognized event types or None.
        The logic for referencing i+1, i+2 lines is handled in the processor.
        """
        # 1) Is this line a switch to a new character? (like "Alrik:")
        if line in self.known_characters_with_colon:
            return "character"

        # 2) Correct any known spelling differences
        line = TALENT_CORRECTIONS.get(line, line)

        # 3) If it's a trait from TRAITS_LONG
        if line in TRAITS_LONG:
            return "trait"

        # 4) If it is a known Talent
        if self._validate_talent_in_db(line):
            return "talent"

        # 5) If it is a known Spell
        if self._validate_spell_in_db(line):
            return "spell"

        # 6) If it is a known Attack
        if self._validate_attack_in_db(line):
            return "attack"

        # 7) If it's initiative
        #    e.g. "Alrik Initiative..."
        if "Initiative" in line and "Initiativewurf" not in line:
            return "initiative"

        # 8) If it's damage
        #    e.g. "treffer"
        if "treffer" in line.lower():
            return "damage"

        # 9) Otherwise, not recognized
        return None
