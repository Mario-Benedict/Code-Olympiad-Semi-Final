import enquiries
from app.utils.helper import clear, get_file_dir
from app.utils.formatting import printf
from app.constant.core import TRASH_CATEGORIES
from app.database import Database
from app.types import Session
from app.config import GAME_FILE
from app.constant.color import LIGHT_YELLOW, BOLD, END, LIGHT_CYAN
import time
from typing import List, Dict, Union
import random
from datetime import datetime, timedelta

answer_options = [answer['name'] for answer in TRASH_CATEGORIES]

total_questions = 5

def generate_questions() -> List[Dict[str, str]]:
  items =  [{ 'name': item, 'answer': category['name']} for category in TRASH_CATEGORIES for item in category['items']]

  for _ in range(total_questions):
    random.shuffle(items)

  return random.sample(items, total_questions)

def check_user_played_today() -> bool:
  try:
    with open(get_file_dir(GAME_FILE), 'r') as f:
      data = f.read()
      if data != '':
        last_played = datetime.strptime(data.strip(), '%Y-%m-%d %H:%M:%S')
        if last_played > datetime.now():
          return True

      return False
  except FileNotFoundError:
    return False

def generate_token_value(score: int) -> int:
  return int((score / total_questions) * random.randint(1, 100))

def game_controller(db: Database, session: Session) -> None:
  clear()

  if check_user_played_today():
    printf('You have already played today. Please come back tomorrow.', LIGHT_YELLOW)
    return

  questions: List[Dict[str, str]] = generate_questions()

  score: int = 0
  for number, question in enumerate(questions, start=1):
    printf(f'Question {number} of {len(questions)}', LIGHT_YELLOW)
    question_text = f'What is the correct category for {BOLD}{question["name"]}{END}?'

    user_answer = enquiries.choose(question_text, answer_options)

    if user_answer == question['answer']:
      score += 1

    time.sleep(1)

    clear()

  with open(get_file_dir(GAME_FILE), 'w+') as f:
    time_to_play = datetime.now() + timedelta(days=1)
    f.write(f'{time_to_play.strftime("%Y-%m-%d %H:%M:%S")}')

  tokens = generate_token_value(score)

  db.query(f'UPDATE users SET token = token + {tokens} WHERE id = "{session[0]}"')

  printf(f'Your score is {score} out of {total_questions}', LIGHT_CYAN)
  printf(f'You have earned {tokens} {"tokens" if tokens > 1 else "token"}', LIGHT_CYAN)
