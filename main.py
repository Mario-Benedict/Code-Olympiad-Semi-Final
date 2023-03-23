import sys

try:
  import pretty_errors
except ImportError:
  pass

if sys.version_info.major < 3:
  print('This application requires Python 3. Please install Python 3 and try again.')
  sys.exit(0)

from app import InLifeInterpreter

def main() -> None:
  interpreter = InLifeInterpreter()
  interpreter.start()

if __name__ == '__main__':
  main()
