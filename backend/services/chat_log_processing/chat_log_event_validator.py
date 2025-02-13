from typing import List, Optional

from config.logger_config import logger
from models.dice_event import DiceEvent

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
    def __init__(self, characters_and_aliases, talents, spells, attacks):
        self.characters_and_aliases = characters_and_aliases
        self.known_talents = talents
        self.known_spells = spells
        self.known_attacks = attacks
        self.current_character_name = ""

    def determine_dice_event(self, lines_chunk: List[str]) -> Optional[DiceEvent]:
        """
        lines_chunk: up to 5 consecutive lines from the chat log.
        Returns a DiceEvent if recognized, otherwise None.
        """

        if not lines_chunk:
            return None

        # 1) Check if first line is a character switch, e.g. "Alrik:"
        first_line = lines_chunk[0].strip()
        if first_line in (character + ":" for character in self.characters_and_aliases):
            self.current_character_name = first_line[:-1].strip()

        if not self.current_character_name:
            return None

        # 2) Check if the second line corresponds to a valid event type
        if len(lines_chunk) > 1:
            second_line = lines_chunk[1].strip()
            second_line = TALENT_CORRECTIONS.get(second_line, second_line)

            # -- Trait event --
            if second_line in TRAITS_LONG and len(lines_chunk) >= 3:
                return DiceEvent(character=self.current_character_name, event_type="trait", lines=lines_chunk[1:4])

            # -- Talent event --
            if second_line in self.known_talents and len(lines_chunk) >= 3:
                return DiceEvent(character=self.current_character_name, event_type="talent", lines=lines_chunk[1:4])

            # -- Spell event --
            if second_line in self.known_spells and len(lines_chunk) >= 3:
                return DiceEvent(character=self.current_character_name, event_type="spell", lines=lines_chunk[1:4])

            # -- Attack event --
            if second_line in self.known_attacks:
                if len(lines_chunk) > 3 and "Kampfgetümmel" in lines_chunk[3]:
                    del lines_chunk[3]
                return DiceEvent(character=self.current_character_name, event_type="attack", lines=lines_chunk[1:])

            # -- Initiative event --
            if "Initiative" in second_line and "Initiativewurf" not in second_line:
                return DiceEvent(character=self.current_character_name, event_type="initiative", lines=lines_chunk[1:])

            # -- Damage event --
            if "treffer" in second_line.lower():
                return DiceEvent(character=self.current_character_name, event_type="damage", lines=[lines_chunk[2]])

            else:
                return None

        return None
