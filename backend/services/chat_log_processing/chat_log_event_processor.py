# services/chat_log_processing/chat_log_event_processor.py
import logging
import re
import pandas as pd

from models.dice_event import DiceEvent


class ChatLogEventProcessor:
    """
    Contains methods to process each event type (trait, talent, etc.).
    Populates local DataFrames or does direct DB inserts.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        # Prepare DataFrames
        self.traits_df = pd.DataFrame(columns=["character_name", "talent", "modifier", "success", "tap_zfp", "taw_zfw"])
        self.talents_df = pd.DataFrame(
            columns=[
                "character_name",
                "talent",
                "modifier",
                "success",
                "tap_zfp",
                "taw_zfw",
                "trait_value1",
                "trait_value2",
                "trait_value3",
            ]
        )
        self.spells_df = pd.DataFrame(
            columns=[
                "character_name",
                "spell",
                "modifier",
                "success",
                "tap_zfp",
                "taw_zfw",
                "trait_value1",
                "trait_value2",
                "trait_value3",
            ]
        )
        self.attacks_df = pd.DataFrame(
            columns=["character_name", "attack", "modifier", "success", "tap_zfp", "taw_zfw"]
        )
        self.initiatives_df = pd.DataFrame(columns=["character_name", "rolled_ini", "current_ini", "modifier"])
        self.total_damage_df = pd.DataFrame(columns=["character_name", "total_damage"])

    def process_event(self, dice_event: DiceEvent):

        character_name = dice_event.character
        event_type = dice_event.event_type
        lines = dice_event.lines

        # lines[0] => "<CharacterName>:"
        # lines[1], lines[2], lines[3] => vary by event

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
        # no return needed

    def _process_trait_event(self, character_name, lines):
        """
        lines might look like:
        line[0] -> "Mut"
        line[1] -> "Wurfprobe ±2 gelungen (3 TaP*)"
        """

        trait_name = lines[0].strip()
        second_line = lines[1].strip()
        third_line = lines[2].strip()

        # Extract roll data
        current_success, current_modifier = self._mod_and_success_check(second_line)
        current_talent_or_spell_points = self._extract_talent_or_spell_points(second_line, " EP")
        current_talent_or_spell_value = self._extract_talent_or_spell_value(third_line, "EW:")

        # Insert into self.traits_df
        new_row = {
            "character_name": character_name,
            "talent": trait_name,
            "modifier": current_modifier,
            "success": bool(current_success),
            "tap_zfp": current_talent_or_spell_points,
            "taw_zfw": current_talent_or_spell_value,
        }
        self.traits_df = pd.concat([self.traits_df, pd.DataFrame([new_row])], ignore_index=True)

    def _process_talent_event(self, character_name, lines):

        talent_name = lines[0].strip()
        second_line = lines[1].strip()
        third_line = lines[2].strip()

        current_success, current_modifier = self._mod_and_success_check(second_line)
        current_talent_or_spell_points = self._extract_talent_or_spell_points(second_line, "TaP")
        current_talent_or_spell_value = self._extract_talent_or_spell_value(third_line, "TaW:")
        # For the trait values in the third line, e.g. "Eigenschaften: 14/15/15"
        trait_values = self._extract_trait_values(third_line)

        new_row = {
            "character_name": character_name,
            "talent": talent_name,
            "modifier": current_modifier,
            "success": bool(current_success),
            "tap_zfp": current_talent_or_spell_points,
            "taw_zfw": current_talent_or_spell_value,
            "trait_value1": trait_values[0],
            "trait_value2": trait_values[1],
            "trait_value3": trait_values[2],
        }
        self.talents_df = pd.concat([self.talents_df, pd.DataFrame([new_row])], ignore_index=True)

    def _process_spell_event(self, character_name, lines):

        spell_name = lines[0].strip()
        second_line = lines[1].strip()
        third_line = lines[2].strip()

        current_success, current_modifier = self._mod_and_success_check(second_line)
        current_talent_or_spell_points = self._extract_talent_or_spell_points(second_line, "ZfP")
        current_talent_or_spell_value = self._extract_talent_or_spell_value(third_line, "ZfW:")
        trait_values = self._extract_trait_values(third_line)

        new_row = {
            "character_name": character_name,
            "spell": spell_name,
            "modifier": current_modifier,
            "success": bool(current_success),
            "tap_zfp": current_talent_or_spell_points,
            "taw_zfw": current_talent_or_spell_value,
            "trait_value1": trait_values[0],
            "trait_value2": trait_values[1],
            "trait_value3": trait_values[2],
        }
        self.spells_df = pd.concat([self.spells_df, pd.DataFrame([new_row])], ignore_index=True)

    def _process_attack_event(self, character_name, lines):
        attack_name = lines[0].strip()
        second_line = lines[1].strip()
        third_line = lines[2].strip()

        # Extract the attack modifier and the attack roll (tap_zfp) from the same line
        current_modifier, current_tap_zfp = self._extract_attack_mod_and_tap_zfp(second_line)
        current_taw_zfw = self._extract_attack_taw_zfw(third_line)

        # Compute success similarly to the old logic:
        # success if (taw - modifier - roll) >= 0
        current_success = 1 if (current_taw_zfw - current_modifier - current_tap_zfp) >= 0 else 0

        new_row = {
            "character_name": character_name,
            "attack": attack_name,
            "modifier": current_modifier,
            "success": bool(current_success),
            "tap_zfp": current_tap_zfp,
            "taw_zfw": current_taw_zfw,
        }
        self.attacks_df = pd.concat([self.attacks_df, pd.DataFrame([new_row])], ignore_index=True)

    def _process_initiative_event(self, character_name, lines):

        # Example approach
        first_line = lines[0].strip()
        second_line = lines[1].strip()

        rolled_ini = self._extract_rolled_initiative(first_line)
        (current_ini, current_mod) = self._extract_current_initiative_and_mod(second_line)

        new_row = {
            "character_name": character_name,
            "rolled_ini": rolled_ini,
            "current_ini": current_ini,
            "modifier": current_mod,
        }
        self.initiatives_df = pd.concat([self.initiatives_df, pd.DataFrame([new_row])], ignore_index=True)

    def _process_damage_event(self, character_name, lines):

        damage_line = lines[0]
        # Example parse
        match = re.search(r"\d+", damage_line)
        dmg = int(match.group()) if match else 0

        # Update total damage in self.total_damage_df
        existing = self.total_damage_df[self.total_damage_df["character_name"] == character_name]
        if not existing.empty:
            idx = existing.index[0]
            self.total_damage_df.at[idx, "total_damage"] += dmg
        else:
            new_row = {"character_name": character_name, "total_damage": dmg}
            self.total_damage_df = pd.concat([self.total_damage_df, pd.DataFrame([new_row])], ignore_index=True)

    # --------------------------------------------------------------------------
    # Helper / extraction methods
    # --------------------------------------------------------------------------
    def _mod_and_success_check(self, line: str):
        """
        Returns (success_flag, mod_value).
        success_flag is 1 or 0
        """
        parts = line.split()
        # A naive example: "Wurfprobe ±2 gelungen" => parts = ["Wurfprobe", "±2", "gelungen"]
        current_mod = 0
        current_success = 0
        if len(parts) >= 2:
            mod_part = parts[1]
            mod_part = mod_part.replace("±", "")  # e.g. ±2 => 2
            try:
                current_mod = int(mod_part)
            except ValueError:
                current_mod = 0
        # success?
        if "gelungen" in line.lower():
            current_success = 1
        return (current_success, current_mod)

    def _extract_talent_or_spell_points(self, line: str, pattern="TaP"):
        """
        Looks for e.g. "(16 TaP*)." or "(16 ZfP*)."
        Return the integer found or 0 if not found.
        """
        # One naive approach: try to split on "(" then parse the second part
        # e.g. line = "Wurfprobe ±2 gelungen (3 TaP*)."
        match = re.search(r"\((\d+)\s+" + re.escape(pattern), line)
        if match:
            return int(match.group(1))
        return 0

    def _extract_talent_or_spell_value(self, line: str, prefix="TaW:"):
        """
        e.g. if the line says "Eigenschaften: 14/15/15  TaW: 5"
        we want to get 5
        """
        match = re.search(re.escape(prefix) + r"\s*(\d+)", line)
        if match:
            return int(match.group(1))
        return 0

    def _extract_trait_values(self, line: str):
        """
        e.g. line: "Eigenschaften: 14/15/15"
        Return a tuple (14,15,15)
        """
        match = re.search(r"Eigenschaften:\s*(\d+)\s*/\s*(\d+)\s*/\s*(\d+)", line)
        if match:
            return [int(match.group(1)), int(match.group(2)), int(match.group(3))]
        # fallback
        return [0, 0, 0]

    def _extract_attack_mod_and_tap_zfp(self, line: str):
        """
        Extracts the attack modifier and the attack roll (tap_zfp) from the same line.
        For example, given a line like "FK-Angriff +1  (7).", it returns (1, 7).
        """
        mod = 0
        tap_zfp = 0

        # Extract modifier from the second token of the line
        parts = line.split()
        if len(parts) >= 2:
            mod_str = parts[1].replace("±", "")
            try:
                mod = int(mod_str)
            except ValueError:
                mod = 0

        # Extract tap_zfp by searching for the number in parentheses
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
        # e.g. line might be "Alrik Initiative (rolled) = 14"
        match = re.search(r"Initiative.*?(\d+)", line)
        if match:
            return int(match.group(1))
        return 0

    def _extract_current_initiative_and_mod(self, line: str):
        """
        Extracts the current initiative (IB value) and modifier from a line.
        Expected line format (example):
            "#W6: 1    IB: 11    BE:    Mod.: 0"
        Returns a tuple (current_ini, current_mod) where current_ini is taken from the IB field.
        """
        current_ini = 0
        current_mod = 0

        # Extract the IB value instead of the first number encountered
        match_ini = re.search(r"IB:\s*(\d+)", line)
        if match_ini:
            current_ini = int(match_ini.group(1))

        # Extract the modifier using the existing pattern
        match_mod = re.search(r"Mod.*?(\d+)", line)
        if match_mod:
            current_mod = int(match_mod.group(1))

        return (current_ini, current_mod)
