from dataclasses import dataclass
from enum import Enum

class TrashCategory(Enum):
  Household = 'Household'
  Hazardous = 'Hazardous'
  Medical = 'Medical'
  Electrical = 'Electrical'
  Construction = 'Construction'
  Organic = 'Organic'

@dataclass
class Question:
  question: str
  category: TrashCategory
