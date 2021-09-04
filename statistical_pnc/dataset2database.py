import json
import logging
import os
import openpyxl

from .models import news2db, reference2db, symbol2db, stopword2db, categories_list, word2db, category2db, News,Word


def add2database(corpus_file_path: str = None, file_name: str = None, symbols_list_file_path: str = None,
                 stopwords_list_file_path: str = None, part_of_data: list = None,
                 part_of_data_header: list = None) -> int:
    if corpus_file_path is not None:
        file_name = os.path.basename(corpus_file_path)
        reference = reference2db(file_name)
    elif file_name is not None:
        reference = reference2db(file_name)
    else:
        raise Exception('Enter corpus_file_path or file_name.')

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
            sym_wrd = word2db(string=string)
            symbol2db(reference=reference, word=sym_wrd)
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
            stpwrd_wrd = word2db(string=string)
            stopword2db(word=stpwrd_wrd, reference=reference)
        reference.load_stopwords_list = True
        reference.save()
        logging.info('Persian stopwords storage in the database is complete.')

    if not reference.load_complate:
        if part_of_data is None:
            logging.info('Started news file loading... .')
            wb_obj = openpyxl.load_workbook(corpus_file_path)
            logging.info('News file loaded.')
            sheet = wb_obj.active
            first = True
            column_title_list = []
            row_number = 1
            logging.info('Started storing persian news in the database.')
            for row in sheet.iter_rows():
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
                    category=category2db(title=_data['Category'], reference=reference)
                )
                logging.info(f'The number {row_number} news item storage in the database is complete.')
            reference.load_complate = True
            reference.save()
        else:
            logging.info('Started news file loading... .')
            logging.info('News file loaded.')
            column_title_list = part_of_data_header
            row_number = 1
            logging.info('Started storing persian news in the database.')
            for row in part_of_data:
                col = []
                for cell in row:
                    col.append(cell)
                _data = {}
                for i in range(len(column_title_list)):
                    _data[column_title_list[i]] = col[i]

                logging.info(f'Started storing the number {row_number} news item in the database.')

                news2db(
                    reference=reference,
                    titr_string=_data['Titr'],
                    content_string=_data['Content'],
                    category=category2db(title=_data['Category'], reference=reference)
                )
                logging.info(f'The number {row_number} news item storage in the database is complete.')
            reference.save()

    duplicate_words = News.words.through.objects.all()
    len_duplicate_words = len(duplicate_words)
    words = Word.objects.all()
    print('$$$$$$$$$$$$$$$$$$$$$$$$')
    for wrd in words:
        num_wrd = len(duplicate_words.filter(word_id=wrd.pk).all())
        wrd._number_of_repetitions = num_wrd
        wrd.save()
    words = Word.objects.all().order_by('_number_of_repetitions')
    print('RRRRRRRRRRRRRRRR')
    for wrd in words:
        if wrd.number_of_repetitions < 10:
            continue
        threshold = wrd.number_of_repetitions / len_duplicate_words
        if 0.0009 < threshold:
            stopword2db(wrd)
    return reference
