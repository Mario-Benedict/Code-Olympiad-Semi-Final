import os

def get_home_dir() -> str:
    return os.getenv('HOME') if os.name == 'posix' else os.getenv('USERPROFILE')

def remove_file_dir(file) -> None:
  home_dir = get_home_dir()
  file_dir = f'{home_dir}/{file}'

  if os.path.isfile(file_dir):
    os.system(f'rm {file_dir}') if os.name == 'posix' else os.system(f'del {file_dir}')

def check_file_exists(file_dir, action = None) -> None:
  file_exists =  os.path.exists(file_dir)

  if not file_exists:
    if action is None:
      return file_exists
    else:
      action()

