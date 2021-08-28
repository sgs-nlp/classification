import logging
from pathlib import Path
from scipy.spatial.distance import cosine
from random import sample
from .dataset2database import add2database
from .models import Category, news2db, News, Word, Keyword, categories_list, Reference
# from nvd.classification import Classification
from nvd.converter import bag_of_word2one_hot


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
    # corpus_file_path = Path('staticfiles', 'HamshahriData.xlsx')
    # add2database(corpus_file_path)
    logging.info('Data storage in the database is complete.')


def news_classification(reference: Reference, content: str, titr: str = None) -> Category:
    news = news2db(
        content_string=content,
        titr_string=titr,
    )
    news_vector = news2vector(news)
    cats_list = categories_list(reference=reference, vector=True)
    minimum_value = 100
    minimum_index = ''
    for cat_key, cat_val in cats_list.items():
        dist = cosine(news_vector, cat_val)
        if minimum_value > dist:
            minimum_value = dist
            minimum_index = cat_key
    near_category = Category.objects.get(pk=minimum_index)
    return near_category


def news2vector(news: News) -> list:
    vector_len = Word.objects.last()
    vector_len = int(vector_len.pk)
    vector = [0] * (vector_len + 1)
    kwrds = Keyword.objects.filter(news=news).all()
    for kw in kwrds:
        vector[int(kw.word.pk)] = kw.frequency
    return vector


class NewsClassification:
    def __init__(self):
        data = News.objects.filter(category__isnull=False).all()
        data_len = len(data) - 1
        data_test_len = round(data_len / 6)
        test_ary_list = sample(range(1, data_len), data_test_len)
        _data = []
        for i in test_ary_list:
            _data.append(data[i])
        self.data_for_test = _data
        self.categories_list = None
        self.categories_list_pk = None

    def _clist(self):
        self.categories_list = categories_list(vector=True)
        self.categories_list_pk = self.categories_list.keys()

    def _classification(self, news):
        news_vector = news.vector
        self._clist()
        cats_list = self.categories_list
        minimum_value = 100
        minimum_index = ''
        for cat_key, cat_val in cats_list.items():
            dist = cosine(news_vector, cat_val)
            if minimum_value > dist:
                minimum_value = dist
                minimum_index = cat_key
        near_category = Category.objects.get(pk=minimum_index)
        news.category = near_category
        news.save()
        return near_category
    news_for_classification = None


    def classification(self, content: str, titr: str = None) -> Category:
        news = news2db(
            content_string=content,
            titr_string=titr,
        )
        self.news_for_classification = news
        return self._classification(news)

    def performance(self):
        y_test = []
        predicted = []
        for itm in self.data_for_test:
            y_test.append(itm.category.pk)
            predicted.append(self._classification(itm).pk)
        from nvd.measure import true_or_false, precision, recall, accuracy
        false_negative, true_positive, true_negative, false_positive = true_or_false(predicted, y_test,
                                                                                     self.categories_list_pk)
        _precision = precision(true_positive, false_positive)
        _recall = recall(false_negative, true_positive)
        _accuracy = accuracy(false_negative, true_positive, true_negative, false_positive)
        return _precision, _recall, _accuracy

    def feedback(self):
        pass

    def print_d(self):
        print(self.performance())
