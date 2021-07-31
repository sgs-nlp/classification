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
from sklearn import svm as support_vector_machine
import numpy as np

from nvd.normalizer import matrix_scale_matrix
from nvd.embedding import GDoc2Vec
from nvd.measure import true_or_false, precision, recall, accuracy


def classification():
    reference_title = 'staticfiles/HamshahriData.xlsx'

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
    # <-
    # train test split
    # ->
    x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.15, random_state=42)
    # <-
    res = {}
    # multinomial naive baise
    # ->
    mnb_model = MultinomialNB().fit(x_train, y_train)
    mnb_predicted = mnb_model.predict(x_test)
    fns, tps, tns, fps = true_or_false(mnb_predicted, y_test, category_index_list)
    per_mnb = precision(true_positives=tps, false_positives=fps)
    rec_mnb = recall(false_negatives=fns, true_positives=tps)
    acc_mnb = accuracy(false_negatives=fns, true_positives=tps, true_negatives=tns, false_positives=fps)
    mnb_scores = {
        'precision': per_mnb,
        'recall': rec_mnb,
        'accuracy': acc_mnb,
    }
    res['Multinomial_Naive_Baise'] = mnb_scores
    # <-
    # Multi Layer Perseptron
    # ->
    mlp_model = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(15,), random_state=1).fit(x_train,
                                                                                                        y_train)
    mlp_predicted = mlp_model.predict(x_test)
    fns, tps, tns, fps = true_or_false(mlp_predicted, y_test, category_index_list)
    per_mlp = precision(true_positives=tps, false_positives=fps)
    rec_mlp = recall(false_negatives=fns, true_positives=tps)
    acc_mlp = accuracy(false_negatives=fns, true_positives=tps, true_negatives=tns, false_positives=fps)
    mlp_scores = {
        'precision': per_mlp,
        'recall': rec_mlp,
        'accuracy': acc_mlp,
    }
    res['Multi_Layer_Perseptron'] = mlp_scores
    # <-

    # Support Vector Machine
    # ->
    svm_model = support_vector_machine.LinearSVC().fit(x_train, y_train)
    svm_predicted = svm_model.predict(x_test)
    fns, tps, tns, fps = true_or_false(svm_predicted, y_test, category_index_list)
    per_svm = precision(true_positives=tps, false_positives=fps)
    rec_svm = recall(false_negatives=fns, true_positives=tps)
    acc_svm = accuracy(false_negatives=fns, true_positives=tps, true_negatives=tns, false_positives=fps)
    svm_scores = {
        'precision': per_svm,
        'recall': rec_svm,
        'accuracy': acc_svm,
    }
    res['Support_Vector_Machine'] = svm_scores
    # <-
    return res


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
