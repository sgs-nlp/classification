from .models import News, StopWord, Category
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import pandas
import pandas
import glob

import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.neural_network import MLPClassifier
from sklearn import svm
import numpy as np

from nvd.normalizer import matrix_scale_matrix
from nvd.embedding import GDoc2Vec


def classification():
    reference_title = 'staticfiles/HamshahriData.xlsx'

    # load categories on database
    # ->
    _category_list = Category.objects.filter(reference__title=reference_title).all()
    category_list = []
    for category in _category_list:
        category_list.append(category.title_code)
    # <-
    # load on database
    # ->
    news = News.objects.filter(reference__title=reference_title).all()
    # <-
    # pandas data frame
    # ->
    x_data = []
    y_data = []
    for itm in news:
        tmp = [int(itm.category.title_code)]
        for word in itm.titr_words_without_stopword_code[0]:
            tmp.append(int(word))
        x_data.append(tmp)
        y_data.append(category_list.index(itm.category.title_code))
    gensim_d2v_model = GDoc2Vec(x_data)
    x_data = gensim_d2v_model.vectors
    print(f"multinomial naive baise model error: {multinomial_naive_baise_model(x_data, y_data)}")
    print(f'mlp model error: {multi_layer_perseptron_model(x_data, y_data)}')
    print(f'svm model error: {suport_vector_machine_model(x_data, y_data)}')


def classification_2():
    reference_title = 'staticfiles/HamshahriData.xlsx'

    # load categories on database
    # ->
    _category_list = Category.objects.filter(reference__title=reference_title).all()
    category_list = []
    for category in _category_list:
        category_list.append(category.title_code)
    # <-
    # load on database
    # ->
    news = News.objects.filter(reference__title=reference_title).all()
    # <-
    # pandas data frame
    # ->
    _data = []
    for itm in news:
        _data.append({
            'data': f'{itm.titr_string_code} {itm.content_string_code}',
            'flag': category_list.index(itm.category.title_code)
        })
    # print(_data)
    training_data = pandas.DataFrame(_data, columns=['data', 'flag'])
    # print(data)
    # <-
    # load stopwords on database
    # ->
    _stopwords_list = StopWord.objects.filter(reference__title=reference_title).all()
    stopwords_list = []
    for word in _stopwords_list:
        stopwords_list.append(word.word.code)
    # <-

    training_data.to_csv("train_data.csv", sep=',', encoding='utf-8')
    # print(training_data.data.shape)

    # %%

    # GET VECTOR COUNT
    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(training_data.data)
    # SAVE WORD VECTOR
    pickle.dump(count_vect.vocabulary_, open("count_vector.pkl", "wb"))

    # %%

    # TRANSFORM WORD VECTOR TO TF IDF
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
    # SAVE TF-IDF
    pickle.dump(tfidf_transformer, open("tfidf.pkl", "wb"))

    # %%

    print(
        f"multinomial naive baise model error: "
        f"{multinomial_naive_baise_model(X_train_tfidf, training_data, category_list)}")

    # confusion_mat = confusion_matrix(y_test, predicted)
    # print(confusion_mat)

    # print(f'mlp model error: {mlp_model(X_train_tfidf, training_data, category_list)}')
    # print(f'svm model error: {svm_model(X_train_tfidf, training_data, category_list)}')


def multinomial_naive_baise_model(x_data, y_data):
    x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.15, random_state=42)
    nb_model = MultinomialNB().fit(x_train, y_train)
    predicted = nb_model.predict(x_test)
    result_bayes = pandas.DataFrame({'true_labels': y_test, 'predicted_labels': predicted})
    print(result_bayes)
    number_of_err = 0
    total = 0
    for predicted_item, result in zip(predicted, y_test):
        total += 1
        if predicted_item != result:
            number_of_err += 1
    return 100 - ((number_of_err / total) * 100)



# def classification_2():
#     reference_title = 'staticfiles/HamshahriData.xlsx'
#
#     # load categories on database
#     # ->
#     _category_list = Category.objects.filter(reference__title=reference_title).all()
#     category_list = []
#     for category in _category_list:
#         category_list.append(category.title_code)
#     # <-
#     # load on database
#     # ->
#     news = News.objects.filter(reference__title=reference_title).all()
#     # <-
#     # pandas data frame
#     # ->
#     _data = []
#     for itm in news:
#         _data.append({
#             'data': f'{itm.titr_string_code} {itm.content_string_code}',
#             'flag': category_list.index(itm.category.title_code)
#         })
#     # print(_data)
#     training_data = pandas.DataFrame(_data, columns=['data', 'flag'])
#     # print(data)
#     # <-
#     # load stopwords on database
#     # ->
#     _stopwords_list = StopWord.objects.filter(reference__title=reference_title).all()
#     stopwords_list = []
#     for word in _stopwords_list:
#         stopwords_list.append(word.word.code)
#     # <-
#
#     training_data.to_csv("train_data.csv", sep=',', encoding='utf-8')
#     # print(training_data.data.shape)
#
#     # %%
#
#     # GET VECTOR COUNT
#     count_vect = CountVectorizer()
#     X_train_counts = count_vect.fit_transform(training_data.data)
#     # SAVE WORD VECTOR
#     pickle.dump(count_vect.vocabulary_, open("count_vector.pkl", "wb"))
#
#     # %%
#
#     # TRANSFORM WORD VECTOR TO TF IDF
#     tfidf_transformer = TfidfTransformer()
#     X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
#     # SAVE TF-IDF
#     pickle.dump(tfidf_transformer, open("tfidf.pkl", "wb"))
#
#     # %%
#
#     print(
#         f"multinomial naive baise model error: "
#         f"{multinomial_naive_baise_model(X_train_tfidf, training_data, category_list)}")
#
#     # confusion_mat = confusion_matrix(y_test, predicted)
#     # print(confusion_mat)
#
#     # print(f'mlp model error: {mlp_model(X_train_tfidf, training_data, category_list)}')
#     # print(f'svm model error: {svm_model(X_train_tfidf, training_data, category_list)}')
#
#
# def multinomial_naive_baise_model(x_data, y_data):
#     # x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.15, random_state=42)
#     nb_model = MultinomialNB().fit(x_train, y_train)
#     # predicted = nb_model.predict(x_test)
#     return predicted, y_test
#     # number_of_err = 0
#     # total = 0
#     # for predicted_item, result in zip(predicted, y_test):
#     #     total += 1
#     #     if predicted_item != result:
#     #         number_of_err += 1
#     # return 100 - ((number_of_err / total) * 100)


# def multi_layer_perseptron_model(x_data, y_data):
#     mlp_model = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(15,), random_state=1)
#     X_train, X_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.25,
#                                                         random_state=42)
#     mlp_model.fit(X_train, y_train)
#     # pickle.dump(mlp_model, open("softmax.pkl", "wb"))
#     predicted = mlp_model.predict(X_test)
#     result_softmax = pandas.DataFrame({'true_labels': y_test, 'predicted_labels': predicted})
#     # result_softmax.to_csv('res_softmax.csv', sep=',')
#     print(result_softmax)
#     number_of_err = 0
#     total = 0
#     for predicted_item, result in zip(predicted, y_test):
#         total += 1
#         if predicted_item != result:
#             number_of_err += 1
#     return 100 - ((number_of_err / total) * 100)
#
#
# def suport_vector_machine_model(x_data, y_data):
#     svm_model = svm.LinearSVC()
#     x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.25,
#                                                         random_state=42)
#     svm_model.fit(x_train, y_train)
#     # pickle.dump(svm_model, open("svm.pkl", "wb"))
#
#     predicted = svm_model.predict(x_test)
#     result_svm = pandas.DataFrame({'true_labels': y_test, 'predicted_labels': predicted})
#     # result_svm.to_csv('res_svm.csv', sep=',')
#     print(result_svm)
#     number_of_err = 0
#     total = 0
#
#     for predicted_item, result in zip(predicted, y_test):
#         total += 1
#         if predicted_item != result:
#             number_of_err += 1
#     return 100 - ((number_of_err / total) * 100)
