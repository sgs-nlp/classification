from json import loads
from pathlib import Path

STOP_WORDS_PATH = Path('nvd', 'persian.stopword.json')

with open(STOP_WORDS_PATH, 'r', encoding='utf-8') as file:
    s = file.read()
    s = loads(s)
LIST = s
