from maskpass import askpass
from typing import Any

def ask_password(prompt: str, mask: str = '*') -> str | Any:
  return askpass(prompt, mask)
