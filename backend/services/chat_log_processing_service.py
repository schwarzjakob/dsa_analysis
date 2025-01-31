import logging
from typing import Dict, List

# Import event validator and processor
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
        :param talents: Set of valid talent names from DB
        :param spells: Set of valid spell names from DB
        :param attacks: Set of valid attack names from DB
        """
        self.logger = logging.getLogger(__name__)

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
        """
        Main pipeline: classify events -> extract events -> return events (DataFrames)
        """
        i = 0
        while i < len(lines):
            event_type = self.event_validator.determine_event_type(lines[i])
            if event_type:
                i = self.event_processor.process_event(event_type, lines, i)
            else:
                i += 1

        # Return the final DataFrames
        return {
            "traits_df": self.event_processor.traits_df,
            "talents_df": self.event_processor.talents_df,
            "spells_df": self.event_processor.spells_df,
            "attacks_df": self.event_processor.attacks_df,
            "initiatives_df": self.event_processor.initiatives_df,
            "total_damage_df": self.event_processor.total_damage_df,
        }
