from app.constant.database import USERS_TABLE
from app.controllers.base_controller import BaseController
from typing import List
from app.types import Question, TrashCategory
import random
from datetime import datetime, timedelta

_TOTAL_QUESTIONS = 5
_COOLDOWN_HOURS = 24

class GameController(BaseController):
  def get_questions(self) -> List[Question]:
    _QUESTIONS: List[Question] = self._db.fetch_all('SELECT name as question, category FROM trash')

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
