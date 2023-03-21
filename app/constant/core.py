from typing import List, Union, Dict
from app.types import ListOfDict
from app.constant.color import LIGHT_RED, END
from app.utils.formatting import format_str

LOG_FILE: str = 'inlife.log'
LOG_MAX_BYTES: int = 1024 * 1024 * 10
BACKUP_COUNT: int = 5

TRASH_CATEGORIES: ListOfDict[Union[str, List[str]]] = [
  {
    'name': 'Household',
    'items': [
      'Newspapers',
      'Cardboards',
      'Plastic Bags',
      'Glass Bottles',
      'Metal Cans',
    ]
  },
  {
    'name': 'Hazardous',
    'items': [
      'Batteries',
      'Light Bulbs',
      'Fluorescent Tubes',
      'Paint',
      'Oil',
    ]
  },
  {
    'name': 'Medical',
    'items': [
      'Bandages',
      'Syringes',
      'Gloves',
      'Pills',
      'Needles',
    ]
  },
  {
    'name': 'Electrical',
    'items': [
      'Old Computers',
      'Old Laptops',
      'Old Mobile Phones',
      'Old Printers',
      'Old Printers',
    ]
  },
  {
    'name': 'Construction',
    'items': [
      'Bricks',
      'Gypsum',
      'Sawdust',
      'Steel',
      'Broken Windows',
    ]
  },
  {
    'name': 'Organic',
    'items': [
      'Fruits',
      'Vegetables',
      'Leaves',
      'Grass',
      'Flowers',
    ]
  },
]

SHOP_LIST: Dict[str, int] = {
  'Inlife Shopping Bag (1000 tokens)': 1000,
  'Inlife Reusable Water Bottle (3000 tokens)': 3000,
  'Inlife Reusable Straw (500 tokens)': 500,
  'Inlife Reusable Coffee Cup (2000 tokens)': 2000,
  'Inlife T-Shirt (5000 tokens)': 5000,
  'Inlife Lunch Box (10000 tokens)': 10000,
}

BANNER_TEXT: str = format_str('''    ____            __   _    ____
   /  _/  ____     / /  (_)  / __/  ___
   / /   / __ \   / /  / /  / /_   / _ \\
 _/ /   / / / /  / /  / /  / __/  /  __/
/___/  /_/ /_/  /_/  /_/  /_/     \___/''', LIGHT_RED)
