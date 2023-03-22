from itertools import product
from typing import ItemsView
import enquiries
from app.constant.color import LIGHT_CYAN, LIGHT_YELLOW
from app.constant.core import BANNER_TEXT
from app.controllers import ShopController, ShopException
from app.utils.formatting import printf
from app.utils.helper import clear

class ShopView:
  def __init__(self, controller: ShopController) -> None:
    self.__controller = controller

  def start(self, uid: str) -> None:
    BACK = 'Back'

    clear()

    while True:
      balance = self.__controller.get_balance(uid)

      printf('Welcome to the shop', LIGHT_YELLOW)
      printf(f'You have {balance} tokens', LIGHT_CYAN)

      print(BANNER_TEXT)

      products = self.__controller.get_products()

      choices = { self.__transform_name(name, price): name for name, price in products.items() }
      choices[BACK] = None

      prompt = 'Please choose the item you want to buy:'
      choice = enquiries.choose(prompt, choices)

      if choice == BACK:
        clear()
        return

      try:
        self.__controller.purchase(uid, choices[choice])
        clear()
      except ShopException as e:
        clear()
        printf(e, LIGHT_YELLOW)

  def __transform_name(self, name: str, price: int) -> str:
    return f'{name} ({price}) tokens'
