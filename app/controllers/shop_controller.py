from typing import Dict
from app.controllers.base_controller import BaseController
from app.constant.database import USERS_TABLE
class ShopException(Exception):
  pass

class ShopController(BaseController):
  def get_products(self) -> Dict[str, int]:
    return self._db.fetch_all('SELECT name, price FROM shop')

  def __get_product(self, name: str) -> Dict[str, int]:
    return self._db.fetch_one('SELECT name, price FROM shop WHERE name = ?', name)

  def purchase(self, uid: str, product_name: str) -> None:
    price = self.__get_product(product_name)['price']
    balance = self.get_balance(uid)

    if balance < price:
      raise ShopException('You don\'t have enough tokens to buy the item')

    sql = f'UPDATE {USERS_TABLE} SET token = token - ? WHERE id = ?'
    self._db.query(sql, price, uid)

  def get_balance(self, uid: str) -> int:
    sql = f'SELECT token FROM {USERS_TABLE} WHERE id = ?'
    return self._db.fetch_one(sql, uid)['token']
