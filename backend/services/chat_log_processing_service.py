import logging
from typing import Dict

# Import our 3 modules
from services.chat_log_processing.chat_log_parser import ChatLogParser
from services.chat_log_processing.chat_log_event_validator import ChatLogEventValidator
from services.chat_log_processing.chat_log_event_processor import ChatLogEventProcessor


class ChatLogProcessingService:
    """
    Orchestrates:
      1) Parsing raw lines
      2) Determining event types
      3) Processing and collecting results
      4) Returning DataFrames (NO insertion to DB)
    """

    def __init__(self, characters_and_aliases, talents, spells, attacks):
        """
        :param db_conn: psycopg2 connection
        :param sqlalchemy_engine: SQLAlchemy Engine
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

        # Initialize the new modules
        self.parser = ChatLogParser()
        self.validator = ChatLogEventValidator(
            self.characters_and_aliases, self.known_talents, self.known_spells, self.known_attacks
        )
        self.processor = ChatLogEventProcessor()

    def process_chat_log(self, file_path: str) -> Dict[str, "pd.DataFrame"]:
        """
        Main pipeline: parse -> validate -> process -> return DataFrames
        """
        # 1) Parse lines
        lines = self.parser.parse(file_path)

        # 2) Classify lines & gather events in DataFrames
        i = 0
        while i < len(lines):
            event_type = self.validator.determine_event_type(lines[i])
            if event_type:
                i = self.processor.process_event(event_type, lines, i)
            else:
                i += 1

        # 3) Return the final DataFrames (DO NOT insert here)
        return {
            "traits_df": self.processor.traits_df,
            "talents_df": self.processor.talents_df,
            "spells_df": self.processor.spells_df,
            "attacks_df": self.processor.attacks_df,
            "initiatives_df": self.processor.initiatives_df,
            "total_damage_df": self.processor.total_damage_df,
        }
