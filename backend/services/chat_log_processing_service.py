from typing import Dict, List

from config.logger_config import logger
from services.chat_log_processing.chat_log_event_validator import ChatLogEventValidator
from services.chat_log_processing.chat_log_event_processor import ChatLogEventProcessor


class ChatLogProcessingService:
    """
    Orchestrates:
      1) Receiving ChatLog lines
      2) Determining event types
      3) Processing and collecting results
      4) Returning DataFrames (NO insertion to DB)
    """

    def __init__(self, characters_and_aliases, talents, spells, attacks):
        """
        :param characters_and_aliases: List of names & aliases from DB
        :param talents: Dictionary of valid talent names from DB (hash map)
        :param spells: Dictionary of valid spell names from DB (hash map)
        :param attacks: Dictionary of valid attack names from DB (hash map)
        """

        self.characters_and_aliases = characters_and_aliases
        self.known_talents = talents
        self.known_spells = spells
        self.known_attacks = attacks

        # Initialize modules
        self.event_validator = ChatLogEventValidator(
            self.characters_and_aliases, self.known_talents, self.known_spells, self.known_attacks
        )
        self.event_processor = ChatLogEventProcessor()

    def process_chat_log(self, lines: List[str]) -> Dict[str, "pd.DataFrame"]:
        i = 0
        n = len(lines)

        while i < n:
            # Grab up to 4 lines from i onward
            chunk = lines[i : i + 5]
            dice_event = self.event_validator.determine_dice_event(chunk)

            if dice_event is None:
                # No recognized event: just move forward by 1 line
                i += 1
                continue

            # We have a recognized event
            # Let the processor handle these lines
            self.event_processor.process_event(dice_event)

            # The number of lines consumed depends on the event's lines length
            consumed = len(dice_event.lines)
            i += consumed

        # Return the final DataFrames
        return {
            "traits": self.event_processor.traits_rows,
            "talents": self.event_processor.talents_rows,
            "spells": self.event_processor.spells_rows,
            "attacks": self.event_processor.attacks_rows,
            "initiatives": self.event_processor.initiatives_rows,
            "total_damage": self.event_processor.total_damage_rows,
        }
