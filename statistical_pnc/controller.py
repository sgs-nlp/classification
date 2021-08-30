import logging
from pathlib import Path
from scipy.spatial.distance import cosine
from random import sample

from nvd.converter import bag_of_word2one_hot

from .dataset2database import add2database
from .models import Category, news2db, News, Word, Keyword, categories_list, Reference, StatisticalWordCategory


def prerequisites():
    logging.info('Started storing dataset in the database.')
    from extra_settings.models import File
    file_name = 'HamshahriData.xlsx'
    from_which_row = 1
    up_to_which_row = 50
    file = File(file_name)
    if not file.is_complate(from_which_row, up_to_which_row):
        file.save(file_path=Path('staticfiles', file_name))
        res, header = file.load(to_be_continued=False, from_which_row=from_which_row,
                                up_to_which_row=up_to_which_row)
        add2database(file_name=file_name, part_of_data=res, part_of_data_header=header)
        file.save(complate=True, from_which_row=from_which_row, up_to_which_row=up_to_which_row)
    logging.info('Data storage in the database is complete.')


class NewsClassification:
    def __init__(self):
        pass

    categories_list = None
    categories_list_pk = None

    def _clist(self):
        self.categories_list = categories_list(vector=True)
        self.categories_list_pk = self.categories_list.keys()

    news_for_classification = None

    def performance(self):
        data = News.objects.filter(category__isnull=False).all()
        data_len = len(data) - 1
        data_test_len = round(data_len / 6)
        test_ary_list = sample(range(1, data_len), data_test_len)
        _data = []
        for i in test_ary_list:
            _data.append(data[i])
        data_for_test = _data
        y_test = []
        predicted = []
        for itm in data_for_test:
            y_test.append(itm.category.pk)
            predicted.append(self._classification(itm).pk)
        from nvd.measure import true_or_false, precision, recall, accuracy
        false_negative, true_positive, true_negative, false_positive = true_or_false(predicted, y_test,
                                                                                     self.categories_list_pk)
        _precision = precision(true_positive, false_positive)
        _recall = recall(false_negative, true_positive)
        _accuracy = accuracy(false_negative, true_positive, true_negative, false_positive)
        return _precision, _recall, _accuracy

    def classification(self, content: str, titr: str = None):
        self.news_for_classification = news2db(
            content_string=content,
            titr_string=titr,
        )
        if self.news_for_classification.category is not None:
            return self.news_for_classification.category
        news = self.news_for_classification.vector
        len_news = len(news)
        sswcs = StatisticalWordCategory.objects.all()
        categories = Category.objects.all()

        maximum = -1
        top_cat = None
        for cat in categories:
            c_swcs = sswcs.filter(docs_frequency_stdev__gt=0).filter(category=cat).all()
            cat_score = 0
            w_c = 1
            for swc in c_swcs:
                if swc.word_id <= len_news:
                    w_c += 1
                    dist = self._dist(
                        swc.docs_frequency_mean,
                        news[swc.word_id],
                        swc.docs_frequency_stdev
                    )
                    cat_score += dist
            if cat_score > maximum:
                maximum = cat_score
                top_cat = cat
        return top_cat

    @staticmethod
    def _dist(a, b, variance):
        if a - variance < b < a + variance:
            return 1
        return 0


def feedback(news_id: int, category_id: int) -> News:
    from .models import statistical_word_category2db, word2db
    from nvd.pre_processing import tokenizer
    from nvd.extractor import Keywords
    news = News.objects.filter(pk=news_id).first()
    if news is None:
        return None
    category = Category.objects.filter(pk=category_id).first()
    if category is None:
        return None
    doc = tokenizer(news.string)
    kwrds = Keywords(fre=True)
    keywords = kwrds.by_frequency(document=doc, stopword=1, sents=1)
    for keyword in keywords:
        word = word2db(keyword['word'])
        statistical_word_category2db(word, category, docs_frequency=keyword['frequency'])
    return news
