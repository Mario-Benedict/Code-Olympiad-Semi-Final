from app.constant.color import BOLD, LIGHT_CYAN, LIGHT_GREEN, LIGHT_YELLOW
from app.controllers.auth_controller import AuthController, AuthException
from app.utils.formatting import format_str, printf
from app.utils.input import ask_password

class AuthView:
  def __init__(self, controller: AuthController) -> None:
    self.__controller = controller

  def start(self) -> None:
    choices = [
      ('Login', self.__login),
      ('Register', self.__register),
    ]

    while True:
      printf('You are not authenticated. Please login to continue or register if you don\'t have an account.', BOLD)

      for idx, (name, _) in enumerate(choices, start=1):
        print(format_str(f'  [{idx}]', LIGHT_GREEN), name, sep=' ')

      choice = input('Choice: ')

      try:
        idx = int(choice) - 1
        choices[idx][1]()

        break
      except (ValueError, IndexError):
        printf('Invalid choice.', LIGHT_YELLOW)

  def __login(self) -> None:
    while True:
      printf('Login to your account', BOLD)
      username = input('Username: ')
      password = ask_password('Password: ')

      try:
        self.__controller.login(username, password)
        break
      except AuthException as e:
        printf(e, LIGHT_YELLOW)

  def __register(self) -> None:
    while True:
      printf('Register your account', BOLD)

      username = input('Username: ')
      password = ask_password('Password: ')
      confirm_password = ask_password('Confirm Password: ')

      try:
        self.__controller.register(username, password, confirm_password)
        break
      except AuthException as e:
        printf(e, LIGHT_YELLOW)
