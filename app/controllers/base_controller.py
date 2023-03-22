from app.database import Database

class BaseController():
  def __init__(self, db: Database) -> None:
    self._db = db
