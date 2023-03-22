from dataclasses import dataclass
from datetime import datetime

@dataclass
class Session:
  uid: str
  username: str
  expiration_date: datetime
