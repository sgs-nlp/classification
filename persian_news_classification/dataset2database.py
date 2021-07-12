from .models import Reference, add_reference, add_category, add_news, add_stopword, add_word
from nvd.loader import xlsx2dict
from nvd.pre_processing import normilizer, tokenizer, without_stopword
import json


def symbols2database():
    from nvd.symbols import LIST as PERSIAN_SYMBOLS
    for word in PERSIAN_SYMBOLS:
        add_word(word)


def add2database(file_name: str):
    if Reference.objects.filter(title=file_name).first():
        return
    # todo
    symbols2database()
    reference_id = add_reference(file_name)
    stop_word_list_name = f'{file_name}.persian.stopword.json'
    with open(stop_word_list_name, 'r', encoding='utf-8') as file:
        stopwords_list = file.read()
        stopwords_list = json.loads(stopwords_list)
    for word in stopwords_list:
        add_stopword(word, reference_id)
    data = xlsx2dict(file_name)
    _category_list = []
    for _data in data:
        if _data['Category'] not in _category_list:
            _category_list.append(_data['Category'])
    category_list = {}
    for category_name in _category_list:
        category_list[category_name] = add_category(category_name, reference_id)

    for _data in data:
        titr_string = normilizer(_data['Titr'])
        content_string = normilizer(_data['Content'])
        add_news(
            titr_string=titr_string,
            content_string=content_string,
            category_id=category_list[_data['Category']],
            reference_id=reference_id,
        )

    return
