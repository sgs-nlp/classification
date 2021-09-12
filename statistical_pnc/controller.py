import os
from pathlib import Path
import multiprocessing
import logging
import pickle
import random
from tqdm import tqdm

from django.conf import settings

# import nltk
# from nltk.corpus import stopwords
from scipy.spatial.distance import cosine
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
# from gensim.test.utils import common_texts
from sklearn.metrics import accuracy_score, f1_score
from sklearn.linear_model import LogisticRegression
# from sklearn.model_selection import train_test_split
from sklearn import utils

from nvd.converter import bag_of_word2one_hot
from nvd.pre_processing import tokenizer
from nvd.extractor import Keywords
from nvd.classification import Classification

from extra_settings.models import File as my_file_models
from .models import *
from .dataset2database import add2database


def index_default_data() -> dict:
    res = {'categories_list_name': categories_list()}
    return res


def prerequisites() -> dict:
    performance_result_key = {'type': 'performance_result'}
    performance_result_value = BASE_DICT.get_item(performance_result_key)
    if performance_result_value is not None:
        return performance_result_value
    logging.info('Started storing dataset in the database.')
    file_name = 'HamshahriData.xlsx'
    from_which_row = 1
    up_to_which_row = 10990
    file = my_file_models(file_name)
    if not file.is_complate(from_which_row, up_to_which_row):
        file.save(file_path=Path('staticfiles', file_name))
        res, header = file.load(to_be_continued=False, from_which_row=from_which_row,
                                up_to_which_row=up_to_which_row)
        add2database(file_name=file_name, part_of_data=res, part_of_data_header=header)
        file.save(complate=True, from_which_row=from_which_row, up_to_which_row=up_to_which_row)
    logging.info('Data storage in the database is complete.')

    save_news_classification_by_gensim_obj()
    save_news_classification_by_statistical_obj()
    return performance_result()


def performance_result() -> dict:
    performance_result_key = {'type': 'performance_result'}
    performance_result_value = BASE_DICT.get_item(performance_result_key)
    if performance_result_value is not None:
        return performance_result_value
    nc_by_g = load_news_classification_by_gensim_obj()
    nc_by_s = load_news_classification_by_statistical_obj()
    response = {
        'RESULT': True,
        'word2vec_word_embeding__svm__precision_score': round(nc_by_g.classify.svm.precision_score * 10000) / 100,
        'word2vec_word_embeding__svm__recall_score': round(nc_by_g.classify.svm.recall_score * 10000) / 100,
        'word2vec_word_embeding__svm__accuracy_score': round(nc_by_g.classify.svm.accuracy_score * 10000) / 100,
        'word2vec_word_embeding__svm__f1_score': round(nc_by_g.classify.svm.f1_score * 10000) / 100,

        'word2vec_word_embeding__mlp__precision_score': round(nc_by_g.classify.mlp.precision_score * 10000) / 100,
        'word2vec_word_embeding__mlp__recall_score': round(nc_by_g.classify.mlp.recall_score * 10000) / 100,
        'word2vec_word_embeding__mlp__accuracy_score': round(nc_by_g.classify.mlp.accuracy_score * 10000) / 100,
        'word2vec_word_embeding__mlp__f1_score': round(nc_by_g.classify.mlp.f1_score * 10000) / 100,

        'word2vec_word_embeding__lr__precision_score': round(nc_by_g.classify.lr.precision_score * 10000) / 100,
        'word2vec_word_embeding__lr__recall_score': round(nc_by_g.classify.lr.recall_score * 10000) / 100,
        'word2vec_word_embeding__lr__accuracy_score': round(nc_by_g.classify.lr.accuracy_score * 10000) / 100,
        'word2vec_word_embeding__lr__f1_score': round(nc_by_g.classify.lr.f1_score * 10000) / 100,

        'one_hot_word_embeding__svm__precision_score': round(nc_by_s.classify.svm.precision_score * 10000) / 100,
        'one_hot_word_embeding__svm__recall_score': round(nc_by_s.classify.svm.recall_score * 10000) / 100,
        'one_hot_word_embeding__svm__accuracy_score': round(nc_by_s.classify.svm.accuracy_score * 10000) / 100,
        'one_hot_word_embeding__svm__f1_score': round(nc_by_s.classify.svm.f1_score * 10000) / 100,

        'one_hot_word_embeding__mlp__precision_score': round(nc_by_s.classify.mlp.precision_score * 10000) / 100,
        'one_hot_word_embeding__mlp__recall_score': round(nc_by_s.classify.mlp.recall_score * 10000) / 100,
        'one_hot_word_embeding__mlp__accuracy_score': round(nc_by_s.classify.mlp.accuracy_score * 10000) / 100,
        'one_hot_word_embeding__mlp__f1_score': round(nc_by_s.classify.mlp.f1_score * 10000) / 100,

        'one_hot_word_embeding__lr__precision_score': round(nc_by_s.classify.lr.precision_score * 10000) / 100,
        'one_hot_word_embeding__lr__recall_score': round(nc_by_s.classify.lr.recall_score * 10000) / 100,
        'one_hot_word_embeding__lr__accuracy_score': round(nc_by_s.classify.lr.accuracy_score * 10000) / 100,
        'one_hot_word_embeding__lr__f1_score': round(nc_by_s.classify.lr.f1_score * 10000) / 100,
    }
    BASE_DICT.set_item(performance_result_key, response)
    return response


def classification_result(content: str, titr: str) -> dict:
    response = {'TEXT': True}
    if content is None or len(content) == 0:
        response['TEXT'] = False
        response['ERROR_MESSAGE'] = 'Please enter the news you want to categorize in this section.'
        return response

    news_c = load_news_classification_by_gensim_obj()

    news = news2db(
        content_string=content,
        titr_string=titr,
    )
    news_words = []
    for n in news.words_tokenize.all():
        news_words.append(str(n.pk))
    news_vector = news_c.gmodel.infer_vector(news_words, steps=20)

    svm_category_id = news_c.classify.svm.document_category(news_vector)

    category = Category.objects.filter(pk=svm_category_id).first()
    if category is None:
        response['CATEGORY_TITLE'] = 'None'
        response['CATEGORY_PK'] = 1
    else:
        response['CATEGORY_TITLE'] = category.title
        response['CATEGORY_PK'] = category.pk
    response['NEWS_PK'] = news.pk
    response['CATEGORIES_LIST_NAME'] = categories_list()
    return response


class NewsClassificationByGensim:
    def __init__(self, number_of_train_data=0.85, dm=1, vector_size=300, negative=5, hs=0, min_count=2, sample=0,
                 workers=None, alpha=0.025, min_alpha=0.001, epochs=30):
        # 0 < number_of_train_data < 1
        self.number_of_train_data = number_of_train_data
        # 0 < number_of_test_data < 1
        self.number_of_test_data = 1 - number_of_train_data
        self.dm = dm
        self.vector_size = vector_size
        self.negative = negative
        self.hs = hs
        self.min_count = min_count
        self.sample = sample
        self.workers = workers if workers is not None else multiprocessing.cpu_count()
        self.alpha = alpha
        self.min_alpha = min_alpha
        self.epochs = epochs

    def _data_preparation(self):
        news = News.objects.all()
        documents = []
        categories = {}
        for n in news:
            _words = n.words_tokenize.all()
            words = []
            for wrd in _words:
                words.append(str(wrd.pk))
            if n.category is None:
                tag = '-1'
                categories['-1'] = '-1'
            else:
                tag = str(n.category_id)
                categories[n.category.title] = n.category_id
            documents.append(TaggedDocument(words, [tag]))
        self._tagged_documents = documents
        self._categories = categories

    _tagged_documents = None

    @property
    def tagged_documents(self):
        if self._tagged_documents is None:
            self._data_preparation()
        return self._tagged_documents

    _x_data = None

    @property
    def x_data(self):
        if self._x_data is None:
            documents = utils.shuffle(self.tagged_documents)
            self._y_data, self._x_data = \
                zip(*[(doc.tags[0], self.gmodel.infer_vector(doc.words, steps=20)) for doc in documents])
        return self._x_data

    _y_data = None

    @property
    def y_data(self):
        if self._y_data is None:
            documents = utils.shuffle(self.tagged_documents)
            self._y_data, self._x_data = \
                zip(*[(doc.tags[0], self.gmodel.infer_vector(doc.words, steps=20)) for doc in documents])
        return self._y_data

    _categories = None

    @property
    def categories(self):
        if self._categories is None:
            self._data_preparation()
        return self._categories

    _train_documents = None

    @property
    def train_documents(self):
        if self._train_documents is None:
            self._train_test_split()
        return self._train_documents

    _test_documents = None

    @property
    def test_documents(self):
        if self._test_documents is None:
            self._test_test_split()
        return self._test_documents

    def _train_test_split(self):
        train_documents = []
        test_documents = []
        len_documetns = len(self.tagged_documents)
        train_index = random.sample(range(len_documetns), round(len_documetns * self.number_of_train_data))
        for i in range(len_documetns):
            if i in train_index:
                train_documents.append(self.tagged_documents[i])
            else:
                test_documents.append(self.tagged_documents[i])
        self._train_documents = train_documents
        self._test_documents = test_documents

    _gmodel = None

    @property
    def gmodel(self):
        if self._gmodel is None:
            if os.path.isfile('./uploads/newsModel.d2v'):
                model_dbow = Doc2Vec.load('./uploads/newsModel.d2v')
                self._gmodel = model_dbow
            else:
                train_documents = self.train_documents
                model_dbow = Doc2Vec(
                    dm=self.dm,
                    vector_size=self.vector_size,
                    negative=self.negative,
                    hs=self.hs,
                    min_count=self.min_count,
                    sample=self.sample,
                    workers=self.workers,
                    alpha=self.alpha,
                    min_alpha=self.min_alpha
                )
                model_dbow.build_vocab([x for x in tqdm(train_documents)])
                train_documents = utils.shuffle(train_documents)
                model_dbow.train(train_documents, total_examples=len(train_documents), epochs=30)
                model_dbow.save('./uploads/newsModel.d2v')
                self._gmodel = model_dbow
        return self._gmodel

    _classify = None

    @property
    def classify(self):
        if self._classify is None:
            self._classify = Classification(x_data=self.x_data, y_data=self.y_data, categories_list=self.categories)
        return self._classify

    _one_hot_vectors = None

    def create_all(self):
        if self._tagged_documents is None:
            tmp = self.tagged_documents
        if self._x_data is None:
            tmp = self.x_data

        if self._y_data is None:
            tmp = self.y_data

        if self._categories is None:
            tmp = self.categories

        if self._train_documents is None:
            tmp = self.train_documents

        if self._test_documents is None:
            tmp = self.test_documents

        if self._gmodel is None:
            tmp = self.gmodel

        if self._classify is None:
            tmp = self.classify
            self.classify.create_all()


def save_news_classification_by_gensim_obj() -> None:
    nc_key = {'type': 'NewsClassificationByGensim'}
    news_c = BASE_DICT.get_item(nc_key)
    if news_c is None:
        pkl_file_name = settings.NEWS_CLASSIFICATION_BY_GENSIM_FILE_ROOT
        if not os.path.exists(pkl_file_name):
            news_c = NewsClassificationByGensim()
            news_c.create_all()
            with open(pkl_file_name, 'wb') as pkl_file:
                pickle.dump(news_c, pkl_file)
            BASE_DICT.set_item(nc_key, news_c)


def load_news_classification_by_gensim_obj() -> NewsClassificationByGensim:
    nc_key = {'type': 'NewsClassificationByGensim'}
    nc = BASE_DICT.get_item(nc_key)
    if nc is None:
        pkl_file_name = settings.NEWS_CLASSIFICATION_BY_GENSIM_FILE_ROOT
        with open(pkl_file_name, 'rb') as pkl_file:
            nc = pickle.load(pkl_file)
    return nc


# class NewsClassification_2:
#     def __init__(self, minimum_number_of_sample_repetitions=0.3):
#         self.minimum_number_of_sample_repetitions = minimum_number_of_sample_repetitions
#
#     categories_list = None
#     categories_list_pk = None
#
#     def _clist(self):
#         self.categories_list = categories_list(vector=True)
#         self.categories_list_pk = self.categories_list.keys()
#
#     news_for_classification = None
#
#     def performance(self):
#         data = News.objects.filter(category__isnull=False).all()
#         data_len = len(data) - 1
#         data_test_len = round(data_len / 6)
#         test_ary_list = random.sample(range(1, data_len), data_test_len)
#         _data = []
#         for i in test_ary_list:
#             _data.append(data[i])
#         data_for_test = _data
#         y_test = []
#         predicted = []
#         for itm in data_for_test:
#             y_test.append(itm.category.pk)
#             predicted.append(self._classification(itm).pk)
#         from nvd.measure import true_or_false, precision, recall, accuracy
#         false_negative, true_positive, true_negative, false_positive = true_or_false(predicted, y_test,
#                                                                                      self.categories_list_pk)
#         _precision = precision(true_positive, false_positive)
#         _recall = recall(false_negative, true_positive)
#         _accuracy = accuracy(false_negative, true_positive, true_negative, false_positive)
#         return _precision, _recall, _accuracy
#
#     def classification(self, content: str, titr: str = None):
#         self.news_for_classification = news2db(
#             content_string=content,
#             titr_string=titr,
#         )
#         if self.news_for_classification.category is not None:
#             return self.news_for_classification.category
#         news = self.news_for_classification.vector
#         news_word = self.news_for_classification.words
#         len_news = len(news)
#         sswcs = StatisticalWordCategory.objects.all()
#         categories = Category.objects.all()
#
#         maximum = -1
#         top_cat = None
#         for cat in categories:
#             c_swcs = sswcs.filter(docs_frequency_stdev__gt=0).filter(category=cat).all()
#
#             # minimum_number_of_sample_repetitions_per_category
#             m_per_c = self.minimum_number_of_sample_repetitions * len(News.objects.filter(category=cat).all())
#
#             cat_score = 0
#             w_c = 1
#             kwords = []
#             for swc in c_swcs:
#                 true_word = news_word.filter(pk=swc.word_id).first()
#                 if true_word is not None:
#                     # tag = settings.TAGGER.tag([true_word.string])
#                     # if tag[0][1] == 'V' or tag[0][1] == 'ADV' or tag[0][1] == 'PR' or tag[0][1] == 'PRO' \
#                     #         or tag[0][1] == 'AJ' or tag[0][1] == 'NUM' or tag[0][1] == 'AJe' or tag[0][1] == 'RES':
#                     #     continue
#
#                     m_per_c_swc = len(swc.all_docs_frequency)
#                     if m_per_c_swc >= m_per_c:
#                         # print(m_per_c_swc, m_per_c)
#                         if swc.word_id <= len_news:
#                             w_c += 1
#                             dist = self._dist(
#                                 swc.docs_frequency_mean,
#                                 news[swc.word_id],
#                                 swc.docs_frequency_stdev
#                             )
#                             cat_score += dist
#             print(cat_score, cat, kwords)
#             if cat_score > maximum:
#                 maximum = cat_score
#                 top_cat = cat
#         return top_cat
#
#     @staticmethod
#     def _dist(a, b, variance):
#         if a - variance < b < a + variance:
#             return 1
#         return 0
#
#
# def feedback(news_id: int, category_id: int) -> News:
#     news = News.objects.filter(pk=news_id).first()
#     if news is None:
#         return None
#     category = Category.objects.filter(pk=category_id).first()
#     if category is None:
#         return None
#     doc = tokenizer(news.string)
#     kwrds = Keywords(fre=True)
#     keywords = kwrds.by_frequency(document=doc, stopword=1, sents=1)
#     for keyword in keywords:
#         word = word2db(keyword['word'])
#         statistical_word_category2db(word, category, docs_frequency=keyword['frequency'])
#     return news

def classification_feedback(news_id: int, category_id: int) -> News:
    news = news_update(news_id, category_id=category_id)
    return news


# def db2one_hot_vectors():
#     corpus = News.objects.all()
#     vector_len = Word.objects.last().pk
#     documents = []
#     for doc in corpus:
#         _doc_vector = [0] * (vector_len + 1)
#         for wrd in doc.words_tokenize.all():
#             _doc_vector[wrd.pk] += 1
#         documents.append(TaggedDocument(_doc_vector, [str(doc.category.pk)]))
#     return documents


class NewsClassificationByStatistical:
    def __init__(self):
        self.one_hot_vector_len = Word.objects.last().pk + 1

    def _data_preparation(self):
        corpus = News.objects.all()
        documents = []
        categories = []
        for doc in corpus:
            _doc_vector = [0] * self.one_hot_vector_len
            for wrd in doc.words_tokenize.all():
                _doc_vector[wrd.pk] += 1
            tag = str(doc.category.pk if doc.category is not None else -1)
            documents.append(TaggedDocument(_doc_vector, [tag]))
            categories.append(tag)

        self._tagged_documents = documents
        self._categories = categories

    _tagged_documents = None

    @property
    def tagged_documents(self):
        if self._tagged_documents is None:
            self._data_preparation()
        return self._tagged_documents

    _x_data = None

    @property
    def x_data(self):
        if self._x_data is None:
            documents = utils.shuffle(self.tagged_documents)
            self._y_data, self._x_data = \
                zip(*[(doc.tags[0], doc.words) for doc in documents])
        return self._x_data

    _y_data = None

    @property
    def y_data(self):
        if self._y_data is None:
            documents = utils.shuffle(self.tagged_documents)
            self._y_data, self._x_data = \
                zip(*[(doc.tags[0], doc.words) for doc in documents])
        return self._y_data

    _categories = None

    @property
    def categories(self):
        if self._categories is None:
            self._data_preparation()
        return self._categories

    _classify = None

    @property
    def classify(self):
        if self._classify is None:
            self._classify = Classification(x_data=self.x_data, y_data=self.y_data, categories_list=self.categories)
        return self._classify

    def create_all(self):
        if self._tagged_documents is None:
            tmp = self.tagged_documents
        if self._x_data is None:
            tmp = self.x_data

        if self._y_data is None:
            tmp = self.y_data

        if self._categories is None:
            tmp = self.categories

        if self._classify is None:
            tmp = self.classify
            self.classify.create_all()


def save_news_classification_by_statistical_obj() -> None:
    nc_key = {'type': 'NewsClassificationByStatistical'}
    news_c = BASE_DICT.get_item(nc_key)
    if news_c is None:
        pkl_file_name = settings.NEWS_CLASSIFICATION_BY_STATISTICAL_FILE_ROOT
        if not os.path.exists(pkl_file_name):
            news_c = NewsClassificationByStatistical()
            news_c.create_all()
            with open(pkl_file_name, 'wb') as pkl_file:
                pickle.dump(news_c, pkl_file)
            BASE_DICT.set_item(nc_key, news_c)


def load_news_classification_by_statistical_obj() -> NewsClassificationByStatistical:
    nc_key = {'type': 'NewsClassificationByStatistical'}
    nc = BASE_DICT.get_item(nc_key)
    if nc is None:
        pkl_file_name = settings.NEWS_CLASSIFICATION_BY_STATISTICAL_FILE_ROOT
        with open(pkl_file_name, 'rb') as pkl_file:
            nc = pickle.load(pkl_file)
    return nc
