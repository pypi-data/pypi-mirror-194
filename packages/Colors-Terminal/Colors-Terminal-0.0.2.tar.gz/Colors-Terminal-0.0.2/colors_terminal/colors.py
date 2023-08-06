class Colors:
  black = '\033[30m'
  orange = '\033[33m'
  blue = '\033[34m'
  purple = '\033[35m'
  red = '\033[31m'
  yellow = '\033[93m'
  green = '\033[32m'
  white = '\033[0m'

  def print(self, text, colored=True):
    if colored:
      for i, c in enumerate(text):
        if i == len(text) - 1:
          print(c + self.white, end='')
        else:
          print(c, end='')
    else:
      print(text, end='')