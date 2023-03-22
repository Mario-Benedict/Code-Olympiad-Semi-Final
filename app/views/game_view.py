from typing import List, Self

import enquiries
from app.constant.color import BOLD, LIGHT_CYAN, LIGHT_YELLOW
from app.controllers import GameController
from app.controllers.game_controller import Question
from app.utils.formatting import format_str, printf
from app.utils.helper import clear

class GameView:
  def __init__(self, controller: GameController) -> None:
    self.__controller = controller

  def start(self, uid: str) -> None:
    clear()

    if self.__controller.has_user_played_today():
      printf('You have already played today. Please come back tomorrow.', LIGHT_YELLOW)
      return

    questions: List[Question] = self.__controller.get_questions()
    total_questions: int = len(questions)

    score: int = 0

    for number, question in enumerate(questions, start=1):
      printf(f'Question {number} of {total_questions}', LIGHT_YELLOW)

      question_name = format_str(question['question'], BOLD)
      question_text = f'What is the correct category for {question_name}?'

      options = self.__controller.get_options()
      user_answer = enquiries.choose(question_text, options)

      if user_answer == question['category'].value:
        score += 1

      clear()

    reward = self.__controller.finish_session(uid, score)

    printf(f'Your score is {score} out of {total_questions}', LIGHT_CYAN)
    printf(f'You have earned {reward} tokens', LIGHT_CYAN)
