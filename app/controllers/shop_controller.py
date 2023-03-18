import enquiries
from app.utils.helper import clear, color_print
from app.constant.color import LIGHT_YELLOW, LIGHT_CYAN, LIGHT_RED
from app.constant.core import BANNER_TEXT, SHOP_LIST
from app.database import Database
from app.types import Session
from typing import List, Dict, Union

shop_options: SHOP_LIST = SHOP_LIST
shop_options['Exit'] = 0

def shop_controller(db: Database, session: Session) -> None:
  clear()

  user_token = db.fetch_one(f'SELECT token FROM users WHERE id = "{session[0]}"')
  user_token = user_token[0]

  while True:
    color_print('Welcome to the shop', LIGHT_YELLOW)
    print(BANNER_TEXT)

    color_print(f'You have {user_token} {"tokens" if user_token > 1 else "token"}', LIGHT_CYAN)
    message = 'Please choose the item you want to buy:'

    choice = enquiries.choose(message, shop_options)

    if choice == 'Exit':
      clear()
      return

    purchased_item_price = shop_options[choice]

    if user_token < purchased_item_price:
      clear()
      color_print('You don\'t have enough token to buy the item', LIGHT_RED)
      continue

    user_token -= purchased_item_price

    db.query(f'UPDATE users SET token = {user_token} WHERE id = "{session[0]}"')
    break

  clear()
  color_print('Thanks for purchasing', LIGHT_CYAN)
