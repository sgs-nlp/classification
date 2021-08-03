import pickle
import pandas
import glob
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn import svm as support_vector_machine
from sklearn.naive_bayes import MultinomialNB
from sklearn.neural_network import MLPClassifier

from .models import News, StopWord, Category, Word, code2word

from nvd.normalizer import matrix_scale_matrix
from nvd.embedding import GDoc2Vec, BOWDoc2vec, OneHotDoc2vec
from nvd.measure import true_or_false, precision, recall, accuracy
from nvd.classification import Classification


def classification(reference_title: str = 'staticfiles/HamshahriData.xlsx'):
    # load categories on database
    # ->
    _category_list = Category.objects.filter(reference__title=reference_title).all()
    category_list = []
    category_index_list = []
    i = 0
    for category in _category_list:
        category_list.append(category.title_code)
        category_index_list.append(i)
        i += 1
    # <-

    # load on database
    # ->
    news = News.objects.filter(reference__title=reference_title).all()
    # <-

    # data -> input: x_data, output: y_data
    # ->
    x_data = []
    y_data = []
    for itm in news:
        tmp = []
        for word in itm.content_words_without_stopword_code[0]:
            tmp.append(str(word))
        x_data.append(tmp)
        y_data.append(itm.category.pk)
    # <-

    # create word vector with gensim w2v
    # ->
    gensim_d2v_model = GDoc2Vec(x_data)
    x_data2gv = gensim_d2v_model.vectors
    # <-

    # create word vector with one-hot encoding
    # ->
    dictionary = Word.objects.all()
    ohe_d2v_model = OneHotDoc2vec(x_data, dictionary)
    x_data2ov = ohe_d2v_model.vectors
    # <-

    # classification
    # ->
    g_w2v_classifier = Classification(x_data2gv, y_data, category_index_list)
    o_w2v_classifier = Classification(x_data2ov, y_data, category_index_list)

    # <-
    # set template parameter
    res = {
        'word2vec_word_embeding__svm__precision_score': g_w2v_classifier.svm.precision_score,
        'word2vec_word_embeding__svm__recall_score': g_w2v_classifier.svm.recall_score,
        'word2vec_word_embeding__svm__accuracy_score': g_w2v_classifier.svm.accuracy_score,

        'word2vec_word_embeding__mlp__precision_score': g_w2v_classifier.mlp.precision_score,
        'word2vec_word_embeding__mlp__recall_score': g_w2v_classifier.mlp.recall_score,
        'word2vec_word_embeding__mlp__accuracy_score': g_w2v_classifier.mlp.accuracy_score,

        'word2vec_word_embeding__mnb__precision_score': g_w2v_classifier.mnb.precision_score,
        'word2vec_word_embeding__mnb__recall_score': g_w2v_classifier.mnb.recall_score,
        'word2vec_word_embeding__mnb__accuracy_score': g_w2v_classifier.mnb.accuracy_score,

        'one_hot_encoding_word_embeding__svm__precision_score': o_w2v_classifier.svm.precision_score,
        'one_hot_encoding_word_embeding__svm__recall_score': o_w2v_classifier.svm.recall_score,
        'one_hot_encoding_word_embeding__svm__accuracy_score': o_w2v_classifier.svm.accuracy_score,

        'one_hot_encoding_word_embeding__mlp__precision_score': o_w2v_classifier.mlp.precision_score,
        'one_hot_encoding_word_embeding__mlp__recall_score': o_w2v_classifier.mlp.recall_score,
        'one_hot_encoding_word_embeding__mlp__accuracy_score': o_w2v_classifier.mlp.accuracy_score,

        'one_hot_encoding_word_embeding__mnb__precision_score': o_w2v_classifier.mnb.precision_score,
        'one_hot_encoding_word_embeding__mnb__recall_score': o_w2v_classifier.mnb.recall_score,
        'one_hot_encoding_word_embeding__mnb__accuracy_score': o_w2v_classifier.mnb.accuracy_score,
    }
    # <-
    return res
