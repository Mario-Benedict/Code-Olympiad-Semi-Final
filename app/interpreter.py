import os
import sys
import sqlite3
import bcrypt
from app.config import DATABASE_FILE, METADATA_FILE
from app.utils.logging import logger
from app.constant.color import LIGHT_RED, END, LIGHT_YELLOW, WHITE, LIGHT_GREEN, BOLD, LIGHT_CYAN
from app.constant.core import BANNER_TEXT
from app.database import Database
from app.utils.formatting import printf, format_str
from maskpass import askpass
from app.utils.helper import get_file_dir, remove_file_home_dir, file_checker, clear
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
    banner = BANNER_TEXT

    banner += '\n\n'

    banner += format_str('[*] Created By    : ', LIGHT_YELLOW)
    banner += format_str('Mario Benedict\n', WHITE)

    banner += format_str(' |---> GitHub ', LIGHT_YELLOW)
    banner += format_str('https://github.com/Mario-Benedict\n', WHITE)

    banner += format_str('[*] Version       : ', LIGHT_YELLOW)
    banner += format_str('1.0.0\n', WHITE)

    banner += '\n'

    banner += format_str(f'Welcome back, {self.session[1].upper()}!', LIGHT_CYAN)

    print(banner)

  def authentication(self) -> None:
    while True:
      printf('You are not authenticated. Please login to continue or register if you don\'t have an account.', BOLD)
      print(format_str('  [1]', LIGHT_GREEN), 'Login', sep=' ')
      print(format_str('  [2]', LIGHT_GREEN), 'Register', sep=' ')

      choice = input('Choice: ')

      if choice == '1':
        self.login()
        break
      elif choice == '2':
        self.register()
        break
      else:
        printf('Invalid choice.', LIGHT_YELLOW)
        continue

  def start(self) -> None:
    while True:
      self.session = self.get_session()
      self.print_banner()

      choices = {
        'Minigame': lambda: game_controller(self.__db, self.session),
        'Option 2': lambda: print('Option 2'),
        'Shop': lambda: shop_controller(self.__db, self.session),
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
      printf('Login to your account', BOLD)
      username = input('Username: ')
      password = askpass('Password: ')

      user = self.__db.fetch_one(f'SELECT * FROM users WHERE username = "{username}"')

      if user is None:
        printf('Invalid username or password', LIGHT_YELLOW)
        continue

      if bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
        with open(get_file_dir(METADATA_FILE), 'w') as f:
            expiration_date = datetime.now() + timedelta(days=30)
            f.write(f'{str(user[0])}, {str(user[1])}, {expiration_date.strftime("%Y-%m-%d %H:%M:%S")}')

        clear()
        printf('Login successful', LIGHT_CYAN)
        break

      printf('Invalid username or password', LIGHT_YELLOW)
      continue

    self.start()

  def register(self) -> None:
    while True:
      printf('Register your account', BOLD)
      username = input('Username: ')
      password = askpass('Password: ')
      confirm_password = askpass('Confirm Password: ')

      if password != confirm_password:
          printf('Password doesn\'t match', LIGHT_YELLOW)
      elif self.__db.fetch_one(f'SELECT id FROM users WHERE username = "{username}"') is not None:
          printf('Username already taken', LIGHT_YELLOW)
      else:
          hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
          self.__db.query(f'INSERT INTO users (username, password) VALUES ("{username}", "{hashed_password}")')
          printf('Registration successful', LIGHT_CYAN)
          break

  def logout(self) -> None:
    remove_file_home_dir(METADATA_FILE)
    printf('Good bye!', LIGHT_CYAN)
    sys.exit(1)
