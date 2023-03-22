from typing import Dict
from app.controllers.base_controller import BaseController
from app.constant.database import USERS_TABLE

_SHOP_LIST: Dict[str, int] = {
  'Inlife Shopping Bag': 1000,
  'Inlife Reusable Water Bottle': 3000,
  'Inlife Reusable Straw': 500,
  'Inlife Reusable Coffee Cup': 2000,
  'Inlife T-Shirt': 5000,
  'Inlife Lunch Box': 10000,
  'Inlife Lifely Wife': 999999999,
}

class ShopException(Exception):
  pass

class ShopController(BaseController):
  def get_products(self) -> Dict[str, int]:
    return _SHOP_LIST

  def purchase(self, uid: str, product_name: str) -> None:
    price = _SHOP_LIST[product_name]
    balance = self.get_balance(uid)

    if balance < price:
      raise ShopException('You don\'t have enough tokens to buy the item')

    sql = f'UPDATE {USERS_TABLE} SET token = token - ? WHERE id = ?'
    self._db.query(sql, price, uid)

  def get_balance(self, uid: str) -> int:
    sql = f'SELECT token FROM {USERS_TABLE} WHERE id = ?'
    return self._db.fetch_one(sql, uid)['token']
