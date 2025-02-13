import logging
import re

from models.dice_event import DiceEvent


class ChatLogEventProcessor:
    """
    Processes events and collects rows for database insertion.
    Instead of pandas DataFrames, events are stored as lists of dictionaries.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.traits_rows = []  # List[dict] for trait events
        self.talents_rows = []  # List[dict] for talent events
        self.spells_rows = []  # List[dict] for spell events
        self.attacks_rows = []  # List[dict] for attack events
        self.initiatives_rows = []  # List[dict] for initiative events
        self.total_damage_rows = {}  # Dictionary mapping character to total damage

    def process_event(self, dice_event: DiceEvent):
        character_name = dice_event.character
        event_type = dice_event.event_type
        lines = dice_event.lines

        if event_type == "trait":
            self._process_trait_event(character_name, lines)
        elif event_type == "talent":
            self._process_talent_event(character_name, lines)
        elif event_type == "spell":
            self._process_spell_event(character_name, lines)
        elif event_type == "attack":
            self._process_attack_event(character_name, lines)
        elif event_type == "initiative":
            self._process_initiative_event(character_name, lines)
        elif event_type == "damage":
            self._process_damage_event(character_name, lines)
        else:
            self.logger.warning(f"Unknown event type: {event_type}")

    def _process_trait_event(self, character_name, lines):
        # Expected lines:
        #   lines[0]: Trait name
        #   lines[1]: Roll info (e.g., "Wurfprobe ±2 gelungen (3 EP*).")
        #   lines[2]: Additional info with value (e.g., "Eigenschaften: 14/15/15  EW: 5")
        trait_name = lines[0].strip()
        second_line = lines[1].strip()
        third_line = lines[2].strip()

        current_success, current_modifier = self._mod_and_success_check(second_line)
        current_points = self._extract_talent_or_spell_points(second_line, " EP")
        current_value = self._extract_talent_or_spell_value(third_line, "EW:")

        row = {
            "character_name": character_name,
            "talent": trait_name,
            "modifier": current_modifier,
            "success": bool(current_success),
            "tap_zfp": current_points,
            "taw_zfw": current_value,
        }
        self.traits_rows.append(row)

    def _process_talent_event(self, character_name, lines):
        talent_name = lines[0].strip()
        second_line = lines[1].strip()
        third_line = lines[2].strip()

        current_success, current_modifier = self._mod_and_success_check(second_line)
        current_points = self._extract_talent_or_spell_points(second_line, "TaP")
        current_value = self._extract_talent_or_spell_value(third_line, "TaW:")
        trait_values = self._extract_trait_values(third_line)

        row = {
            "character_name": character_name,
            "talent": talent_name,
            "modifier": current_modifier,
            "success": bool(current_success),
            "tap_zfp": current_points,
            "taw_zfw": current_value,
            "trait_value1": trait_values[0],
            "trait_value2": trait_values[1],
            "trait_value3": trait_values[2],
        }
        self.talents_rows.append(row)

    def _process_spell_event(self, character_name, lines):
        spell_name = lines[0].strip()
        second_line = lines[1].strip()
        third_line = lines[2].strip()

        current_success, current_modifier = self._mod_and_success_check(second_line)
        current_points = self._extract_talent_or_spell_points(second_line, "ZfP")
        current_value = self._extract_talent_or_spell_value(third_line, "ZfW:")
        trait_values = self._extract_trait_values(third_line)

        row = {
            "character_name": character_name,
            "spell": spell_name,
            "modifier": current_modifier,
            "success": bool(current_success),
            "tap_zfp": current_points,
            "taw_zfw": current_value,
            "trait_value1": trait_values[0],
            "trait_value2": trait_values[1],
            "trait_value3": trait_values[2],
        }
        self.spells_rows.append(row)

    def _process_attack_event(self, character_name, lines):
        attack_name = lines[0].strip()
        second_line = lines[1].strip()
        third_line = lines[2].strip()

        modifier, tap_zfp = self._extract_attack_mod_and_tap_zfp(second_line)
        taw_zfw = self._extract_attack_taw_zfw(third_line)
        current_success = 1 if (taw_zfw - modifier - tap_zfp) >= 0 else 0

        row = {
            "character_name": character_name,
            "attack": attack_name,
            "modifier": modifier,
            "success": bool(current_success),
            "tap_zfp": tap_zfp,
            "taw_zfw": taw_zfw,
        }
        self.attacks_rows.append(row)

    def _process_initiative_event(self, character_name, lines):
        first_line = lines[0].strip()
        second_line = lines[1].strip()

        rolled_ini = self._extract_rolled_initiative(first_line)
        current_ini, current_mod = self._extract_current_initiative_and_mod(second_line)

        row = {
            "character_name": character_name,
            "rolled_ini": rolled_ini,
            "current_ini": current_ini,
            "modifier": current_mod,
        }
        self.initiatives_rows.append(row)

    def _process_damage_event(self, character_name, lines):
        damage_line = lines[0]
        match = re.search(r"\d+", damage_line)
        dmg = int(match.group()) if match else 0

        # Accumulate damage per character
        if character_name in self.total_damage_rows:
            self.total_damage_rows[character_name] += dmg
        else:
            self.total_damage_rows[character_name] = dmg

    # --------------------------------------------------------------------------
    # Helper / extraction methods
    # --------------------------------------------------------------------------
    def _mod_and_success_check(self, line: str):
        """
        Returns (success_flag, mod_value).
        success_flag is 1 or 0
        """
        parts = line.split()
        current_mod = 0
        current_success = 0
        if len(parts) >= 2:
            mod_part = parts[1].replace("±", "")
            try:
                current_mod = int(mod_part)
            except ValueError:
                current_mod = 0
        if "gelungen" in line.lower():
            current_success = 1
        return (current_success, current_mod)

    def _extract_talent_or_spell_points(self, line: str, pattern="TaP"):
        """
        Extracts talent or spell points, allowing for negative values.
        Example patterns:
            - "(16 TaP*)"
            - "(-2 TaP*)"
        Returns the integer found or 0 if not found.
        """
        match = re.search(r"\((-?\d+)\s+" + re.escape(pattern), line)
        return int(match.group(1)) if match else 0

    def _extract_talent_or_spell_value(self, line: str, prefix="TaW:"):
        """
        e.g. if the line says "Eigenschaften: 14/15/15  TaW: 5"
        we want to get 5
        """
        match = re.search(re.escape(prefix) + r"\s*(\d+)", line)
        return int(match.group(1)) if match else 0

    def _extract_trait_values(self, line: str):
        """
        e.g. line: "Eigenschaften: 14/15/15"
        Return a tuple (14,15,15)
        """
        match = re.search(r"Eigenschaften:\s*(\d+)\s*/\s*(\d+)\s*/\s*(\d+)", line)
        if match:
            return [int(match.group(1)), int(match.group(2)), int(match.group(3))]
        return [0, 0, 0]

    def _extract_attack_mod_and_tap_zfp(self, line: str):
        """
        Extracts the attack modifier and the attack roll (tap_zfp) from the same line.
        For example, given a line like "FK-Angriff +1  (7).", it returns (1, 7).
        """
        parts = line.split()
        mod = 0
        tap_zfp = 0
        if len(parts) >= 2:
            mod_str = parts[1].replace("±", "")
            try:
                mod = int(mod_str)
            except ValueError:
                mod = 0
        match = re.search(r"\((\d+)\)", line)
        if match:
            tap_zfp = int(match.group(1))
        return mod, tap_zfp

    def _extract_attack_taw_zfw(self, line: str) -> int:
        """
        Extracts the attack value from the third line.
        Depending on the type of attack the prefix may be:
          - "FK-Wert:" for Fernkampfangriff
          - "AT-Wert:" for Nahkampfangriff
          - "PA-Wert:" for Nahkampfparade
        """
        for prefix in ["FK-Wert:", "AT-Wert:", "PA-Wert:"]:
            if prefix in line:
                match = re.search(re.escape(prefix) + r"\s*(\d+)", line)
                if match:
                    return int(match.group(1))
        return 0

    def _extract_rolled_initiative(self, line: str) -> int:
        match = re.search(r"Initiative.*?(\d+)", line)
        return int(match.group(1)) if match else 0

    def _extract_current_initiative_and_mod(self, line: str):
        """
        Extracts the current initiative (IB value) and modifier from a line.
        Expected line format (example):
            "#W6: 1    IB: 11    BE:    Mod.: 0"
        Returns a tuple (current_ini, current_mod) where current_ini is taken from the IB field.
        """
        current_ini = 0
        current_mod = 0
        match_ini = re.search(r"IB:\s*(\d+)", line)
        if match_ini:
            current_ini = int(match_ini.group(1))
        match_mod = re.search(r"Mod.*?(\d+)", line)
        if match_mod:
            current_mod = int(match_mod.group(1))
        return (current_ini, current_mod)
