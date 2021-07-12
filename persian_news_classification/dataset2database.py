from .models import Reference, add_reference, add_category, add_news
from nvd.loader import xlsx2dict
from nvd.pre_processing import normilizer, tokenizer, without_stopword


def add2database(file_name):
    if Reference.objects.filter(title=file_name).first():
        return
    reference_id = add_reference(file_name)
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
