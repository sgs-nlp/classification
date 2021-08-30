from hashlib import sha224
from nvd.pre_processing import tokenizer, normilizer


def string_hash(string: str):
    string = normilizer(string)
    return sha224(string.encode('utf-8')).hexdigest()