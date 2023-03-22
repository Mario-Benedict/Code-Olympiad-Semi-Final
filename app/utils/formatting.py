from app.constant.color import END

def printf(text: str, color: str, end: str = '\n') -> None:
  print(format_str(text, color), end)

def format_str(text: str, color: str) -> str:
  return f'{color}{text}{END}'
