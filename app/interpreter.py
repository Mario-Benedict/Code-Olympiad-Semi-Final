import os
import sys
import sqlite3
import bcrypt
from app.config import DATABASE_FILE
from app.utils.logging import logger
from app.constant.color import LIGHT_RED, END, LIGHT_YELLOW, WHITE, LIGHT_GREEN, BOLD, LIGHT_CYAN
from app.database import Database
from maskpass import askpass
from app.utils.helper import get_home_dir, remove_file_dir, check_file_exists
from datetime import datetime, timedelta
from typing import List, Union

class InLifeInterpreter:
  def __init__(self) -> None:
    self.clear()
    check_file_exists(DATABASE_FILE, lambda: remove_file_dir('.inlife'))

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
{LIGHT_CYAN}Welcome back, {self.session[1].upper()}!{END}'''
    print(banner)

  def authentication(self) -> None:
    print(f'''{BOLD}You are not authenticated. Please login to continue or register if you don\'t have an account.{END}
{LIGHT_GREEN}[1] {END}Login
{LIGHT_GREEN}[2] {END}Register
    ''', end='\r'
    )

    choice = input('Choice: ')

    if choice == '1': self.login()
    elif choice == '2': self.register()
    else:
      print(f'{LIGHT_YELLOW}Invalid choice.{END}')
      self.authentication()

  def start(self) -> None:
    self.session = self.get_session()
    self.print_banner()

  def get_session(self) -> Union[List[str], None]:
    if not os.path.isfile(f'{get_home_dir()}/.inlife'):
      return None

    with open(f'{get_home_dir()}/.inlife', 'r') as f:
      session = f.read().split(', ')
      return session

  def login(self) -> None:
    print(f'{BOLD}Login to your account.{END}')
    username = input('Username: ')
    password = askpass('Password: ')

    user = self.__db.fetch_one(f'SELECT * FROM users WHERE username = "{username}"')

    if user is None:
      print(f'{LIGHT_YELLOW}Invalid username or password.{END}')
      self.login()

    else:
      if bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
        os.system(f'touch ~/.inlife') if os.name == 'posix' else os.system(f'type nul > "%USERPROFILE%\\.inlife"')

        with open(f'{get_home_dir()}/.inlife', 'w') as f:

          expiration_date = datetime.now() + timedelta(days=30)
          f.write(f'{str(user[0])}, {str(user[1])}, {expiration_date.strftime("%Y-%m-%d %H:%M:%S")}')

        print(f'{LIGHT_GREEN}Login successful.{END}')
        self.start()
      else:
        print(f'{LIGHT_YELLOW}Invalid username or password.{END}')
        self.login()

  def register(self) -> None:
    print(f'{BOLD}Register your account.{END}')
    username = input('Username: ')
    password = askpass('Password: ')
    confirm_password = askpass('Confirm Password: ')

    if password != confirm_password:
      print(f'{LIGHT_YELLOW}Password doesn\'t match.{END}')
      self.register()
    else:
      user = self.__db.fetch_one(f'SELECT * FROM users WHERE username = "{username}"')

      if user is not None:
        print(f'{LIGHT_YELLOW}Username already taken.{END}')
        self.register()
      else:
        self.__db.query(f'INSERT INTO users (username, password) VALUES ("{username}", "{bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")}")')

  def clear(self) -> None:
    os.system('clear') if os.name == 'posix' else os.system('cls')
