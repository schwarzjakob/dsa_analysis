# services/chat_log_processing/chat_log_parser.py
import logging
from typing import List


class ChatLogParser:
    """
    Handles the raw reading of the uploaded chatlog file
    and returns a list of lines (strings).
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def parse(self, file_path: str) -> List[str]:
        """
        Reads the chatlog file from `file_path` and returns the raw lines.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            # Clean up trailing newline characters, etc.
            return [line.rstrip("\n") for line in lines]
        except Exception as e:
            self.logger.error(f"Error reading chat log file '{file_path}': {e}")
            return []
