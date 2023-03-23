from ast import List
import sqlite3
import sys
from app.constant.file import DATABASE_FILE
from app.types import Question, TrashCategory
from app.utils.logging import logger
from typing import Any, Dict, Union

class Database:
  def __init__(self) -> None:
    try:
      self.__db = sqlite3.connect(DATABASE_FILE, detect_types=sqlite3.PARSE_COLNAMES | sqlite3.PARSE_DECLTYPES)

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
    users_table = '''
      CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY NOT NULL UNIQUE DEFAULT (lower(hex(randomblob(16)))),
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        token INTEGER NOT NULL DEFAULT 0,
        last_played TIMESTAMP NULL
      )
    '''

    self.query(users_table)

    trash_table = '''
      CREATE TABLE IF NOT EXISTS trash (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
        name TEXT NOT NULL UNIQUE,
        category TEXT CHECK (category IN ("Household", "Hazardous", "Medical", "Electrical", "Construction", "Organic")) NOT NULL
      )
    '''

    self.query(trash_table)

    shop_table = '''
      CREATE TABLE IF NOT EXISTS shop (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
        name TEXT NOT NULL UNIQUE,
        price INTEGER NOT NULL
      )
    '''

    self.query(shop_table)

    _QUESTIONS: List[Question] = [
      {
        'category': TrashCategory.Household,
        'question': 'Newspapers'
      },
      {
        'category': TrashCategory.Household,
        'question': 'Cardboards'
      },
      {
        'category': TrashCategory.Household,
        'question': 'Plastic Bags'
      },
      {
        'category': TrashCategory.Household,
        'question': 'Glass Bottles'
      },
      {
        'category': TrashCategory.Household,
        'question': 'Metal Cans'
      },
      {
        'category': TrashCategory.Hazardous,
        'question': 'Batteries'
      },
      {
        'category': TrashCategory.Hazardous,
        'question': 'Light Bulbs'
      },
      {
        'category': TrashCategory.Hazardous,
        'question': 'Fluorescent Tubes'
      },
      {
        'category': TrashCategory.Hazardous,
        'question': 'Paint'
      },
      {
        'category': TrashCategory.Hazardous,
        'question': 'Oil'
      },
      {
        'category': TrashCategory.Medical,
        'question': 'Bandages'
      },
      {
        'category': TrashCategory.Medical,
        'question': 'Syringes'
      },
      {
        'category': TrashCategory.Medical,
        'question': 'Gloves'
      },
      {
        'category': TrashCategory.Medical,
        'question': 'Pills'
      },
      {
        'category': TrashCategory.Medical,
        'question': 'Needles'
      },
      {
        'category': TrashCategory.Electrical,
        'question': 'Old Computers'
      },
      {
        'category': TrashCategory.Electrical,
        'question': 'Old Laptops'
      },
      {
        'category': TrashCategory.Electrical,
        'question': 'Old Mobile Phones'
      },
      {
        'category': TrashCategory.Electrical,
        'question': 'Old Printers'
      },
      {
        'category': TrashCategory.Electrical,
        'question': 'Old Printers'
      },
      {
        'category': TrashCategory.Construction,
        'question': 'Bricks'
      },
      {
        'category': TrashCategory.Construction,
        'question': 'Gypsum'
      },
      {
        'category': TrashCategory.Construction,
        'question': 'Sawdust'
      },
      {
        'category': TrashCategory.Construction,
        'question': 'Steel'
      },
      {
        'category': TrashCategory.Construction,
        'question': 'Broken Windows'
      },
      {
        'category': TrashCategory.Organic,
        'question': 'Fruits'
      },
      {
        'category': TrashCategory.Organic,
        'question': 'Vegetables'
      },
      {
        'category': TrashCategory.Organic,
        'question': 'Leaves'
      },
      {
        'category': TrashCategory.Organic,
        'question': 'Grass'
      },
      {
        'category': TrashCategory.Organic,
        'question': 'Flowers'
      },
    ]

    insert_trash = 'INSERT OR IGNORE INTO trash (name, category) VALUES (?, ?)'

    for question in _QUESTIONS:
      self.query(insert_trash, question['question'], question['category'].value)

    _SHOP_LIST: Dict[str, int] = {
      'Inlife Shopping Bag': 1000,
      'Inlife Reusable Water Bottle': 3000,
      'Inlife Reusable Straw': 500,
      'Inlife Reusable Coffee Cup': 2000,
      'Inlife T-Shirt': 5000,
      'Inlife Lunch Box': 10000,
    }

    for item, price in _SHOP_LIST.items():
      self.query('INSERT OR IGNORE INTO shop (name, price) VALUES (?, ?)', item, price)
