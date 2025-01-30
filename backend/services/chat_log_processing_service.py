# services/chat_log_processing.py
import logging
from sqlalchemy.engine import Engine
from typing import List

# Import our 3 new modules
from services.chat_log_processing.chat_log_parser import ChatLogParser
from services.chat_log_processing.chat_log_event_validator import ChatLogEventValidator
from services.chat_log_processing.chat_log_event_processor import ChatLogEventProcessor


class ChatLogProcessingService:
    """
    Orchestrates:
      1) Parsing raw lines
      2) Determining event types
      3) Processing and collecting results
      4) Returning DataFrames or performing final DB insert
    """

    def __init__(self, db_conn, sqlalchemy_engine: Engine):
        """
        :param db_conn: psycopg2 connection
        :param sqlalchemy_engine: SQLAlchemy Engine for .to_sql
        """
        self.logger = logging.getLogger(__name__)
        self.db_conn = db_conn
        self.engine = sqlalchemy_engine

        # We'll create a cursor for validations and queries
        self.cursor = self.db_conn.cursor()

        # We need to figure out known_characters_with_colon,
        # just like in old `DsaStats`:
        #  e.g. ["Alrik:", "Andergast:"]
        known_characters = self._load_characters_and_aliases()
        self.known_characters_with_colon = []
        for char_name, aliases in known_characters.items():
            self.known_characters_with_colon.append(char_name + ":")
            for alias in aliases:
                self.known_characters_with_colon.append(alias + ":")

        # Initialize the new modules
        self.parser = ChatLogParser()
        self.validator = ChatLogEventValidator(
            db_cursor=self.cursor, known_characters_with_colon=self.known_characters_with_colon
        )
        self.processor = ChatLogEventProcessor(db_conn, sqlalchemy_engine, self.cursor)

    def process_chat_log(self, file_path: str):
        """
        Main pipeline: parse -> validate -> process -> batch_insert
        """
        # 1) Parse lines
        lines = self.parser.parse(file_path)

        # 2) For each line, figure out what it is, pass it to the processor
        i = 0
        while i < len(lines):
            event_type = self.validator.determine_event_type(lines[i])
            if event_type:
                i = self.processor.process_event(event_type, lines, i)
            else:
                # Not recognized -> skip
                i += 1

        # 3) (Optional) do a final .to_sql / DB insert in bulk
        self.processor.batch_insert_to_db()

        # 4) Return the final DataFrames if you want to do something else with them
        return {
            "traits_df": self.processor.traits_df,
            "talents_df": self.processor.talents_df,
            "spells_df": self.processor.spells_df,
            "attacks_df": self.processor.attacks_df,
            "initiatives_df": self.processor.initiatives_df,
            "total_damage_df": self.processor.total_damage_df,
        }

    def _load_characters_and_aliases(self):
        """
        Load the characters + aliases from DB for building known_characters_with_colon
        Return dict: { 'Alrik': ['Alri', 'Alking'] , 'Andergast': [], ... }
        """
        self.cursor.execute("SELECT name, alias FROM characters")
        rows = self.cursor.fetchall()
        if not rows:
            return {}
        return {row[0]: row[1] or [] for row in rows}
