import os
import sys
import sqlite3
import bcrypt
from app.config import DATABASE_FILE, METADATA_FILE
from app.utils.logging import logger
from app.constant.color import LIGHT_RED, END, LIGHT_YELLOW, WHITE, LIGHT_GREEN, BOLD, LIGHT_CYAN
from app.database import Database
from maskpass import askpass
from app.utils.helper import get_file_dir, remove_file_home_dir, file_checker, clear, color_print
from datetime import datetime, timedelta
from typing import List, Union
import enquiries
from app.controllers import game_controller, shop_controller

class InLifeInterpreter:
  def __init__(self) -> None:
    clear()
    file_checker(DATABASE_FILE, lambda: remove_file_home_dir(METADATA_FILE))
    self.__db = Database()
    self.session = self.get_session()
    self.start() if self.session is not None else self.authentication()

  def print_banner(self) -> None:
    banner = f'''    {LIGHT_RED}____            __   _    ____
   /  _/  ____     / /  (_)  / __/  ___
   / /   / __ \   / /  / /  / /_   / _ \\
 _/ /   / / / /  / /  / /  / __/  /  __/
/___/  /_/ /_/  /_/  /_/  /_/     \___/{END}
    '''

    banner += f'''
{LIGHT_YELLOW}[*] Created By    : {WHITE}Mario Benedict
 {LIGHT_YELLOW}|---> Github     : {WHITE}https://github.com/Mario-Benedict
{LIGHT_YELLOW}[*] Version       : {WHITE}1.0.0
    '''

    banner += f'''
{LIGHT_CYAN}Welcome back, {self.session[1].upper()}!{END}
'''

    print(banner)

  def authentication(self) -> None:
    while True:
      print(f'''{BOLD}You are not authenticated. Please login to continue or register if you don\'t have an account.{END}
  {LIGHT_GREEN}[1] {END}Login
  {LIGHT_GREEN}[2] {END}Register
      '''
      )

      choice = input('Choice: ')

      if choice == '1':
        self.login()
        break
      elif choice == '2':
        self.register()
        break
      else:
        color_print('Invalid choice.', LIGHT_YELLOW)
        continue

  def start(self) -> None:
    self.session = self.get_session()
    self.print_banner()

    choices = {
      'Minigame': lambda: game_controller(),
      'Option 2': lambda: print('Option 2'),
      'Shop': lambda: shop_controller(),
      'Logout': lambda: self.logout(),
      'Exit': lambda: sys.exit(1)
    }

    option = enquiries.choose("Choose one of this option", choices)

    choices[option]()

  def get_session(self) -> Union[List[str], None]:
    if not os.path.isfile(get_file_dir(METADATA_FILE)):
      return None

    with open(get_file_dir(METADATA_FILE), 'r') as f:
      session = f.read().split(', ')
      return session

  def login(self) -> None:
    while True:
      color_print('Login to your account', BOLD)
      username = input('Username: ')
      password = askpass('Password: ')

      user = self.__db.fetch_one(f'SELECT * FROM users WHERE username = "{username}"')

      if user is None:
        color_print('Invalid username or password', LIGHT_YELLOW)
        continue

      if bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
        with open(get_file_dir(METADATA_FILE), 'w') as f:
            expiration_date = datetime.now() + timedelta(days=30)
            f.write(f'{str(user[0])}, {str(user[1])}, {expiration_date.strftime("%Y-%m-%d %H:%M:%S")}')

        clear()
        color_print('Login successful', LIGHT_CYAN)
        break

      color_print('Invalid username or password', LIGHT_YELLOW)
      continue

    self.start()

  def register(self) -> None:
    while True:
      color_print('Register your account', BOLD)
      username = input('Username: ')
      password = askpass('Password: ')
      confirm_password = askpass('Confirm Password: ')

      if password != confirm_password:
          color_print('Password doesn\'t match', LIGHT_YELLOW)
      elif self.__db.fetch_one(f'SELECT id FROM users WHERE username = "{username}"') is not None:
          color_print('Username already taken', LIGHT_YELLOW)
      else:
          hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
          self.__db.query(f'INSERT INTO users (username, password) VALUES ("{username}", "{hashed_password}")')
          color_print('Registration successful', LIGHT_CYAN)
          break


  def logout(self) -> None:
    remove_file_home_dir(METADATA_FILE)

    print(f'{LIGHT_CYAN}Good bye! {END}')
