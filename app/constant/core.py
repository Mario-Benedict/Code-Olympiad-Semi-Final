from typing import List, Union, Dict
from app.types import ListOfDict
from app.constant.color import LIGHT_RED, END
from app.utils.formatting import format_str

LOG_FILE: str = 'inlife.log'
LOG_MAX_BYTES: int = 1024 * 1024 * 10
BACKUP_COUNT: int = 5

BANNER_TEXT: str = format_str('''    ____            __   _    ____
   /  _/  ____     / /  (_)  / __/  ___
   / /   / __ \   / /  / /  / /_   / _ \\
 _/ /   / / / /  / /  / /  / __/  /  __/
/___/  /_/ /_/  /_/  /_/  /_/     \___/''', LIGHT_RED)
