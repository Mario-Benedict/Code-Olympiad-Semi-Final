from time import strptime
from app.constant.file import METADATA_FILE
from app.constant.database import USERS_TABLE
from app.controllers.base_controller import BaseController
from app.types.session import Session
from app.utils.helper import get_file_dir, remove_file_home_dir
from app.utils.password import hash_password, check_password

from datetime import datetime, timedelta
from typing import Union

import sys
import os

_SESSION_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

class AuthException(Exception):
  pass

class AuthController(BaseController):
  def register(self, username: str, password: str, password_confirmation: str) -> None:
    if password != password_confirmation:
      raise AuthException('Password doesn\'t match')

    sql = f'SELECT COUNT(id) AS count FROM {USERS_TABLE} WHERE username = ?'
    user_count = self._db.fetch_one(sql, username)['count']

    if user_count > 0:
      raise AuthException('Username already taken')

    hashed_password = hash_password(password)
    sql = f'INSERT INTO {USERS_TABLE} (username, password) VALUES (?, ?)'

    self._db.query(sql, username, hashed_password)

  def login(self, username: str, password: str) -> None:
    sql = f'SELECT id, username, password FROM {USERS_TABLE} WHERE username = ?'
    user = self._db.fetch_one(sql, username)

    if user is None:
      raise AuthException('Invalid username or password')

    if check_password(password, user['password']):
      expiration_date = datetime.now() + timedelta(30)
      self.__write_session(user['id'], user['username'], expiration_date)

  def logout(self) -> None:
    remove_file_home_dir(METADATA_FILE)
    sys.exit(1)

  def get_session(self) -> Union[None, Session]:
    if not os.path.isfile(get_file_dir(METADATA_FILE)):
      return None

    with open(get_file_dir(METADATA_FILE), 'r') as f:
      contents = f.read().strip()
      if len(contents) == 0:
        return None

      session = contents.split(', ')
      if len(session) < 3:
        return None

      return Session(
        uid=session[0],
        username=session[1],
        expiration_date=strptime(session[2], _SESSION_DATE_FORMAT)
      )

  def __write_session(self, uid: str, username: str, expiration_date: datetime) -> None:
    with open(get_file_dir(METADATA_FILE), 'w+') as f:
      expiration_date_str = expiration_date.strftime(_SESSION_DATE_FORMAT)
      f.write(f'{uid}, {username}, {expiration_date_str}')
