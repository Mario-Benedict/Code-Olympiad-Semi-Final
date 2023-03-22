import os
from app.constant.color import UNDERLINE, END
from typing import Union

def get_home_dir() -> str:
  return os.getenv('HOME') if os.name == 'posix' else os.getenv('USERPROFILE')

def get_file_dir(file_name: str) -> str:
  home_dir = get_home_dir()
  return f'{home_dir}/{file_name}'

def remove_file_home_dir(file_name: str) -> None:
  file_dir = get_file_dir(file_name)

  if os.path.isfile(file_dir):
    os.system(f'rm {file_dir}') if os.name == 'posix' else os.system(f'del {file_dir}')

def file_checker(file_dir, action = None) -> Union[bool, None]:
  file_exists =  os.path.exists(file_dir)

  if not file_exists and action is not None:
    action()

  return file_exists

def clear() -> None:
  os.system('clear') if os.name == 'posix' else os.system('cls')
