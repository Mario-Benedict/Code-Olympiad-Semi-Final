from app.config.db_config import METADATA_FILE
from app.constant.database import USERS_TABLE
from app.database import Database
from app.utils.helper import get_file_dir, remove_file_home_dir
from app.utils.password import hash_password, check_password

from datetime import datetime, timedelta
from typing import Union, List

import sys
import os

class AuthException(Exception):
  pass

class AuthController:
  def __init__(self, db: Database) -> None:
    self.db = db

  def register(self, username: str, password: str, password_confirmation: str) -> None:
    if password != password_confirmation:
      raise AuthException('Password doesn\'t match')

    sql = f'SELECT COUNT(id) AS count FROM {USERS_TABLE} WHERE username = ?'
    user_count = self.db.fetch_one(sql, username)['count']

    if user_count > 0:
      raise AuthException('Username already taken')

    hashed_password = hash_password(password)
    sql = f'INSERT INTO {USERS_TABLE} (username, password) VALUES (?, ?)'

    self.db.query(sql, username, hashed_password)

  def login(self, username: str, password: str) -> None:
    sql = f'SELECT id, username, password FROM {USERS_TABLE} WHERE username = ?'
    user = self.db.fetch_one(sql, username)

    if user is None:
      raise AuthException('Invalid username or password')

    if check_password(password, user['password']):
      with open(get_file_dir(METADATA_FILE), 'w') as f:
        expiration_date = datetime.now() + timedelta(days=30)
        f.write(f'{str(user["id"])}, {str(user["username"])}, {expiration_date.strftime("%Y-%m-%d %H:%M:%S")}')

  def logout(self) -> None:
    remove_file_home_dir(METADATA_FILE)
    sys.exit(1)

  def get_session(self) -> Union[List[str], None]:
    if not os.path.isfile(get_file_dir(METADATA_FILE)):
      return None

    with open(get_file_dir(METADATA_FILE), 'r') as f:
      contents = f.read().strip()
      if len(contents) == 0:
        return None

      session = contents.split(', ')
      if len(session) < 3:
        return None

      return session
