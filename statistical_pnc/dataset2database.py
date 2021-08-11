import json
import logging
import openpyxl
import pickle
import os

from django.contrib.auth.views import LoginView

from nvd.pre_processing import normilizer, tokenizer, without_stopword

from .models import category2db, news2db, reference2db, symbol2db, stopword2db, categories_list


def add2database(corpus_file_path: str, symbols_list_file_path: str = None,
                 stopwords_list_file_path: str = None) -> int:
    file_name = os.path.basename(corpus_file_path)

    reference = reference2db(file_name)

    if not reference.load_symbols_list:
        logging.info('Started symbols list loading... .')
        if symbols_list_file_path is None:
            logging.info('loading from nvd.symbols.')
            from nvd.symbols import LIST as nvd_symbols_list
            symbols_list = nvd_symbols_list
        else:
            logging.info(f'loading from {symbols_list_file_path}.')
            with open(symbols_list_file_path) as file:
                symbols_list_file = file.read()
                symbols_list = json.loads(symbols_list_file)
        logging.info('Symbols list loaded.')
        logging.info('Started storing persian symbols in the database.')
        for string in symbols_list:
            symbol2db(reference=reference, string=string)
        reference.load_symbols_list = True
        reference.save()
        logging.info('Persian symbols storage in the database is complete.')

    if not reference.load_stopwords_list:
        logging.info('Started stopwords list loading... .')
        if stopwords_list_file_path is None:
            logging.info('loading from nvd.stopwords.')
            from nvd.stopword import LIST as nvd_stopwords_list
            stopwords_list = nvd_stopwords_list
        else:
            logging.info(f'loading from {stopwords_list_file_path}.')
            with open(stopwords_list_file_path) as file:
                stopwords_list_file = file.read()
                stopwords_list = json.loads(stopwords_list_file)
        logging.info('Stopwords list loaded.')
        logging.info('Started storing Persian stopwords in the database.')
        for string in stopwords_list:
            stopword2db(reference=reference, string=string)
        reference.load_stopwords_list = True
        reference.save()
        logging.info('Persian stopwords storage in the database is complete.')

    if not reference.load_complate:
        logging.info('Started news file loading... .')
        wb_obj = openpyxl.load_workbook(corpus_file_path)
        logging.info('News file loaded.')
        sheet = wb_obj.active
        first = True
        column_title_list = []
        row_number = 1
        logging.info('Started storing persian news in the database.')
        for row in sheet.iter_rows(max_row=2):
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
                reference=reference,
                titr_string=_data['Titr'],
                content_string=_data['Content'],
                category_title=_data['Category']
            )
            logging.info(f'The number {row_number} news item storage in the database is complete.')
        reference.load_complate = True
        reference.save()
    print(categories_list(reference=reference, vector=True))
    return reference
