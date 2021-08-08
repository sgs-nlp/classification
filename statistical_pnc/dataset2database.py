import json
import logging
import openpyxl
import pickle
import os

from nvd.pre_processing import normilizer, tokenizer, without_stopword

from .models import category2db, news2db


def add2database(file_name: str) -> int:
    logging.info('Started storing persian symbols in the database.')
    # if not os.path.isfile('uploads/PERSIAN_SYMBOLS.pkl'):
    #     from nvd.symbols import LIST as PERSIAN_SYMBOLS
    #     logging.info('Started persian symbols pkl file craeted.')
    #     with open('uploads/PERSIAN_SYMBOLS.pkl', 'ab') as pkl_file:
    #         pickle.dump(PERSIAN_SYMBOLS, pkl_file)
    #     logging.info('create persian symbols pkl file complate.')
    #     for word in PERSIAN_SYMBOLS:
    #         add_word(word)
    # logging.info('Persian symbols storage in the database is complete.')
    # logging.info('Started stopwords list loading.')
    # if not os.path.isfile('uploads/stopwords_list.pkl'):
    #     stop_word_list_name = f'{file_name}.persian.stopword.json'
    #     with open(stop_word_list_name, 'r', encoding='utf-8') as file:
    #         stopwords_list = file.read()
    #         stopwords_list = json.loads(stopwords_list)
    #     logging.info('Stopwords list loaded.')
    #     logging.info('Started storing persian stopwords list in the database.')
    #     for word in stopwords_list:
    #         add_stopword(word, reference_id)
    #     logging.info('Started stopwords pkl file craeted.')
    #     with open('uploads/stopwords_list.pkl', 'ab') as pkl_file:
    #         pickle.dump(stopwords_list, pkl_file)
    #     logging.info('create stopwords pkl file complate.')
    #     update_reference(reference_id=reference_id, stopwords_list=stopwords_list)
    # logging.info('Persian stopwords storage in the database is complete.')
    logging.info('Started news file loading.')
    wb_obj = openpyxl.load_workbook(file_name)
    logging.info('News file loaded.')
    sheet = wb_obj.active
    first = True
    column_title_list = []
    row_number = 1
    logging.info('Started storing persian news in the database.')
    for row in sheet.iter_rows(max_row=4):
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

        logging.info(f'Started storing the number {row_number} news item in the database.')
        news2db(
            titr_string=_data['Titr'],
            content_string=_data['Content'],
            category_title=_data['Category']
        )
        logging.info(f'The number {row_number} news item storage in the database is complete.')
    return
