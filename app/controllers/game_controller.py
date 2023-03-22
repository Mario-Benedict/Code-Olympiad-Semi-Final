from dataclasses import dataclass
from enum import Enum
from app.constant.database import USERS_TABLE
from app.controllers.base_controller import BaseController
from app.utils.helper import get_file_dir
from app.config import GAME_FILE
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

class GameController(BaseController):
  def get_questions(self) -> List[Question]:
    return random.sample(_QUESTIONS, _TOTAL_QUESTIONS)

  def get_options(self) -> List[TrashCategory]:
    return [category.value for category in TrashCategory]

  def has_user_played_today(self) -> bool:
    try:
      with open(get_file_dir(GAME_FILE), 'r') as f:
        data = f.read().strip()
        if data != '':
          last_played = datetime.strptime(data.strip(), '%Y-%m-%d %H:%M:%S')
          if last_played > datetime.now():
            return True

        return False
    except FileNotFoundError:
        return False

  def finish_session(self, uid: str, score: int) -> int:
    with open(get_file_dir(GAME_FILE), 'w+') as f:
      time_to_play = datetime.now() + timedelta(days=1)
      f.write(f'{time_to_play.strftime("%Y-%m-%d %H:%M:%S")}')

    reward = self.__get_reward(score)

    sql = f'UPDATE {USERS_TABLE} SET token = token + ? WHERE id = ?'
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
