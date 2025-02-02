from pydantic import BaseModel
from typing import List


class DiceEvent(BaseModel):
    character: str
    event_type: str
    lines: List[str]
