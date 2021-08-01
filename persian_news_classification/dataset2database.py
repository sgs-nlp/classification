import json
import logging
import openpyxl

from nvd.pre_processing import normilizer, tokenizer, without_stopword

from .models import Reference, add_reference, add_category, add_news, add_stopword, add_word


def add2database(file_name: str):
    reference_id = Reference.objects.filter(title=file_name).first()
    if reference_id is not None:
        logging.info('The desired datset is available in the database.')
        return
    logging.info('Started storing persian symbols in the database.')
    from nvd.symbols import LIST as PERSIAN_SYMBOLS
    for word in PERSIAN_SYMBOLS:
        add_word(word)
    logging.info('Persian symbols storage in the database is complete.')
    reference_id = add_reference(file_name)
    logging.info('Started stopwords list loading.')
    stop_word_list_name = f'{file_name}.persian.stopword.json'
    with open(stop_word_list_name, 'r', encoding='utf-8') as file:
        stopwords_list = file.read()
        stopwords_list = json.loads(stopwords_list)
    logging.info('Stopwords list loaded.')
    logging.info('Started storing persian stopwords list in the database.')
    for word in stopwords_list:
        add_stopword(word, reference_id)
    logging.info('Persian stopwords storage in the database is complete.')
    logging.info('Started news file loading.')
    wb_obj = openpyxl.load_workbook(file_name)
    logging.info('News file loaded.')
    sheet = wb_obj.active
    first = True
    column_title_list = []
    row_number = 1
    category_dict = {}
    logging.info('Started storing persian news in the database.')
    for row in sheet.iter_rows(max_row=50):
        col = []
        for cell in row:
            col.append(cell.value)
        if first:
            column_title_list = col
            first = False
            continue
        _data = {}
        for i in range(len(column_title_list)):
            _data[column_title_list[i]] = col[i]

        logging.info(f'Started storing category title in the database.')
        if _data['Category'] not in category_dict:
            category_id = add_category(_data['Category'], reference_id)
            category_dict[_data['Category']] = category_id
        category_id = category_dict[_data['Category']]
        logging.info(f'Category title storage in the database is complete.')

        logging.info(f'Started text normalisering')
        titr_string = normilizer(_data['Titr'])
        content_string = normilizer(_data['Content'])
        logging.info(f'Text normalisering complate.')

        logging.info(f'Started storing the number {row_number} news item in the database.')
        add_news(
            titr_string=titr_string,
            content_string=content_string,
            category_id=category_id,
            reference_id=reference_id,
        )
        logging.info(f'The number {row_number} news item storage in the database is complete.')
        row_number += 1
