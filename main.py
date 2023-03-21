import sys

if sys.version_info.major < 3:
  print('This application requires Python 3. Please install Python 3 and try again.')
  sys.exit(0)

from app.utils.formatting import printf
from app.constant.color import LIGHT_CYAN, END
from app.utils.logging import logger
from app import InLifeInterpreter

def main() -> None:
  InLifeInterpreter()

if __name__ == '__main__':
  try:
    main()
  except (KeyboardInterrupt, SystemExit):
    logger.info('Exiting application...')
    printf('\nExiting application...', LIGHT_CYAN)

    sys.exit(0)
