from .stopword import LIST as STOPWORD_LIST
from .symbols import LIST as SYMBOLS_LIST

from hazm import Normalizer

hazm_normilizer = Normalizer(
    remove_extra_spaces=True,
    persian_style=True,
    persian_numbers=True,
    remove_diacritics=True,
    affix_spacing=True,
    token_based=True,
    punctuation_spacing=True
)


def normilizer(string: str) -> str:
    _str = ''
    for c in string:
        if c in SYMBOLS_LIST:
            _str += f' {c} '
            continue
        _str += c
    string = _str
    string = hazm_normilizer.normalize(string)
    return string


def tokenizer(string: str) -> list:
    from hazm import SentenceTokenizer, WordTokenizer
    hazm_sent_tokenizer = SentenceTokenizer().tokenize
    word_tokenizer = WordTokenizer().tokenize
    sentences_list = hazm_sent_tokenizer(string)
    _sents = []
    for sent in sentences_list:
        words = word_tokenizer(sent)
        _sents.append(words)
    sentences_list = _sents
    return sentences_list


def without_stopword(string: list) -> list:
    _string = []
    for itm in string:
        if itm not in STOPWORD_LIST:
            _string.append(itm)
    return _string
