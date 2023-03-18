import sqlite3
import sys
from app.config import DATABASE_FILE
from app.utils.logging import logger
from typing import Any

class Database:
  def __init__(self) -> None:
    self.__db = None
    self.__cur = None

    try:
      self.__db = sqlite3.connect(DATABASE_FILE)
      self.__cur = self.__db.cursor()

      self.__cur.execute('''
      CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY NOT NULL UNIQUE DEFAULT (lower(hex(randomblob(16)))),
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        token INTEGER NOT NULL DEFAULT 0
      )
      ''')
      self.__db.commit()
    except sqlite3.Error as e:
      logger.error(e)
      sys.exit(0)
    except sqlite3.OperationalError as e:
      logger.error(e)
      sys.exit(0)

  def fetch_one(self, query) -> Any:
    result = self.__cur.execute(query)

    return self.__cur.fetchone()

  def query(self, query) -> None:
    self.__cur.execute(query)
    self.__db.commit()
