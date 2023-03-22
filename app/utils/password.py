import bcrypt

def hash_password(password: str) -> str:
  salt = bcrypt.gensalt()
  return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def check_password(to_check: str, hashed_pwd: str) -> bool:
  return bcrypt.checkpw(to_check.encode('utf-8'), hashed_pwd.encode('utf-8'))
