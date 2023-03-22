import sys
from app.config import DATABASE_FILE, METADATA_FILE
from app.constant.color import LIGHT_YELLOW, WHITE, LIGHT_CYAN
from app.constant.core import BANNER_TEXT
from app.controllers.auth_controller import AuthController
from app.database import Database
from app.utils.formatting import printf, format_str
from app.utils.logging import logger
from app.utils.helper import remove_file_home_dir, file_checker, clear
import enquiries
from app.controllers import game_controller, shop_controller
from app.views.auth_view import AuthView

class InLifeInterpreter:
  def __init__(self) -> None:
    file_checker(DATABASE_FILE, lambda: remove_file_home_dir(METADATA_FILE))

    self.__db = Database()
    self.__auth_controller = AuthController(self.__db)

  def start(self) -> None:
    try:
      while True:
        clear()

        self.session = self.__auth_controller.get_session()
        self.__start_app() if self.session is not None else self.__start_auth()
    except (KeyboardInterrupt, SystemExit):
      logger.info('Exiting application...')
      printf('\nExiting application...', LIGHT_CYAN)

      self.__dispose()
      sys.exit(0)

  def __print_banner(self) -> None:
    banner = BANNER_TEXT

    banner += '\n\n'

    banner += format_str('[*] Created By    : ', LIGHT_YELLOW)
    banner += format_str('Mario Benedict\n', WHITE)

    banner += format_str(' |---> GitHub ', LIGHT_YELLOW)
    banner += format_str('https://github.com/Mario-Benedict\n', WHITE)

    banner += format_str('[*] Version       : ', LIGHT_YELLOW)
    banner += format_str('1.0.0\n', WHITE)

    banner += '\n'

    banner += format_str(f'Welcome back, {self.session[1].upper()}!', LIGHT_CYAN)

    print(banner)

  def __start_auth(self) -> None:
    view = AuthView(self.__auth_controller)
    view.start()

    self.session = self.__auth_controller.get_session()

  def __start_app(self) -> None:
    while True:
      self.__print_banner()

      choices = {
        'Minigame': lambda: game_controller(self.__db, self.session),
        'Shop': lambda: shop_controller(self.__db, self.session),
        'Logout': self.__logout,
        'Exit': lambda: sys.exit(1)
      }

      option = enquiries.choose("Choose one of this option", choices)
      choices[option]()

  def __logout(self) -> None:
    printf('Good bye!', LIGHT_CYAN)
    self.__auth_controller.logout()

  def __dispose(self) -> None:
    self.__db.close()
