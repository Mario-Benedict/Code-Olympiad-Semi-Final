from dataclasses import dataclass
from enum import Enum
from app.constant.database import USERS_TABLE
from app.controllers.base_controller import BaseController
from typing import List
import random
from datetime import datetime, timedelta

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

_TOTAL_QUESTIONS = 5
_COOLDOWN_HOURS = 24

class GameController(BaseController):
  def get_questions(self) -> List[Question]:
    return random.sample(_QUESTIONS, _TOTAL_QUESTIONS)

  def get_options(self) -> List[TrashCategory]:
    return [category.value for category in TrashCategory]

  def has_user_played_today(self, uid: str) -> bool:
    sql = f'SELECT last_played FROM {USERS_TABLE} WHERE id = ?'
    last_played = self._db.fetch_one(sql, uid)['last_played']

    if last_played is None:
      return False

    time_allowed_to_play = last_played + timedelta(hours=_COOLDOWN_HOURS)
    return time_allowed_to_play > datetime.now()

  def finish_session(self, uid: str, score: int) -> int:
    reward = self.__get_reward(score)

    sql = f'UPDATE {USERS_TABLE} SET token = token + ?, last_played = CURRENT_TIMESTAMP WHERE id = ?'
    self._db.query(sql, self.__get_reward(score), uid)

    return reward

  def __get_reward(self, score: int) -> int:
    return int((score / _TOTAL_QUESTIONS) * random.randint(1, 100))

_QUESTIONS: List[Question] = [
  {
    'category': TrashCategory.Household,
    'question': "Newspapers"
  },
  {
    'category': TrashCategory.Household,
    'question': "Cardboards"
  },
  {
    'category': TrashCategory.Household,
    'question': "Plastic Bags"
  },
  {
    'category': TrashCategory.Household,
    'question': "Glass Bottles"
  },
  {
    'category': TrashCategory.Household,
    'question': "Metal Cans"
  },
  {
    'category': TrashCategory.Hazardous,
    'question': "Batteries"
  },
  {
    'category': TrashCategory.Hazardous,
    'question': "Light Bulbs"
  },
  {
    'category': TrashCategory.Hazardous,
    'question': "Fluorescent Tubes"
  },
  {
    'category': TrashCategory.Hazardous,
    'question': "Paint"
  },
  {
    'category': TrashCategory.Hazardous,
    'question': "Oil"
  },
  {
    'category': TrashCategory.Medical,
    'question': "Bandages"
  },
  {
    'category': TrashCategory.Medical,
    'question': "Syringes"
  },
  {
    'category': TrashCategory.Medical,
    'question': "Gloves"
  },
  {
    'category': TrashCategory.Medical,
    'question': "Pills"
  },
  {
    'category': TrashCategory.Medical,
    'question': "Needles"
  },
  {
    'category': TrashCategory.Electrical,
    'question': "Old Computers"
  },
  {
    'category': TrashCategory.Electrical,
    'question': "Old Laptops"
  },
  {
    'category': TrashCategory.Electrical,
    'question': "Old Mobile Phones"
  },
  {
    'category': TrashCategory.Electrical,
    'question': "Old Printers"
  },
  {
    'category': TrashCategory.Electrical,
    'question': "Old Printers"
  },
  {
    'category': TrashCategory.Construction,
    'question': "Bricks"
  },
  {
    'category': TrashCategory.Construction,
    'question': "Gypsum"
  },
  {
    'category': TrashCategory.Construction,
    'question': "Sawdust"
  },
  {
    'category': TrashCategory.Construction,
    'question': "Steel"
  },
  {
    'category': TrashCategory.Construction,
    'question': "Broken Windows"
  },
  {
    'category': TrashCategory.Organic,
    'question': "Fruits"
  },
  {
    'category': TrashCategory.Organic,
    'question': "Vegetables"
  },
  {
    'category': TrashCategory.Organic,
    'question': "Leaves"
  },
  {
    'category': TrashCategory.Organic,
    'question': "Grass"
  },
  {
    'category': TrashCategory.Organic,
    'question': "Flowers"
  },
]
