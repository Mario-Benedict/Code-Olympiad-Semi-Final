import sqlite3
import sys
from app.config import DATABASE_FILE
from app.utils.logging import logger
from typing import Any, Union

class Database:
  def __init__(self) -> None:
    try:
      self.__db = sqlite3.connect(DATABASE_FILE)

      def row_dict_factory(cursor: sqlite3.Cursor, row: list) -> dict:
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

      self.__db.row_factory = row_dict_factory
      self.__setup_tables()

    except sqlite3.Error as e:
      logger.error(e)
      sys.exit(0)

  def close(self) -> None:
    self.__db.close()

  def fetch_one(self, query: str, *params: Union[Any, None]) -> Any:
    result = self.__db.execute(query, params)
    return result.fetchone()

  def fetch_all(self, query: str, *params: Union[Any, None]) -> list:
    result = self.__db.execute(query, params)
    return result.fetchall()

  def query(self, query: str, *params: Union[Any, None]) -> None:
    self.__db.execute(query, params)
    self.__db.commit()

  def __setup_tables(self) -> None:
    sql = '''
      CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY NOT NULL UNIQUE DEFAULT (lower(hex(randomblob(16)))),
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        token INTEGER NOT NULL DEFAULT 0
      )
    '''

    self.query(sql)
