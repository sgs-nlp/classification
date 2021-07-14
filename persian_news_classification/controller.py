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

    # print(
    #     f"multinomial naive baise model error: "
    #     f"{multinomial_naive_baise_model(X_train_tfidf, training_data, category_list)}")

    # confusion_mat = confusion_matrix(y_test, predicted)
    # print(confusion_mat)

    # print(f'mlp model error: {mlp_model(X_train_tfidf, training_data, category_list)}')
    # print(f'svm model error: {svm_model(X_train_tfidf, training_data, category_list)}')


def multinomial_naive_baise_model(X_train_tfidf, training_data, category_list):
    # Multinomial Naive Bayes

    X_train, X_test, y_train, y_test = train_test_split(X_train_tfidf, training_data.flag, test_size=0.25,
                                                        random_state=42)
    clf = MultinomialNB().fit(X_train, y_train)

    pickle.dump(clf, open("nb_model.pkl", "wb"))

    predicted = clf.predict(X_test)
    result_bayes = pandas.DataFrame({'true_labels': y_test, 'predicted_labels': predicted})
    result_bayes.to_csv('res_bayes.csv', sep=',')

    number_of_err = 0
    total = 0
    for predicted_item, result in zip(predicted, y_test):
        total += 1
        if predicted_item != category_list[result]:
            number_of_err += 1
    return (number_of_err / total) * 100


def mlp_model(X_train_tfidf, training_data, category_list):
    clf_neural = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(15,), random_state=1)
    X_train, X_test, y_train, y_test = train_test_split(X_train_tfidf, training_data.flag, test_size=0.25,
                                                        random_state=42)
    clf_neural.fit(X_train, y_train)
    pickle.dump(clf_neural, open("softmax.pkl", "wb"))
    predicted = clf_neural.predict(X_test)
    result_softmax = pandas.DataFrame({'true_labels': y_test, 'predicted_labels': predicted})
    result_softmax.to_csv('res_softmax.csv', sep=',')

    number_of_err = 0
    total = 0
    for predicted_item, result in zip(predicted, y_test):
        total += 1
        if predicted_item != category_list[result]:
            number_of_err += 1
    return (number_of_err / total) * 100


def svm_model(X_train_tfidf, training_data, category_list):
    clf_svm = svm.LinearSVC()
    X_train, X_test, y_train, y_test = train_test_split(X_train_tfidf, training_data.flag, test_size=0.25,
                                                        random_state=42)
    clf_svm.fit(X_train_tfidf, training_data.flag)
    pickle.dump(clf_svm, open("svm.pkl", "wb"))

    predicted = clf_svm.predict(X_test)
    result_svm = pandas.DataFrame({'true_labels': y_test, 'predicted_labels': predicted})
    result_svm.to_csv('res_svm.csv', sep=',')

    number_of_err = 0
    total = 0
    for predicted_item, result in zip(predicted, y_test):
        total += 1
        if predicted_item != category_list[result]:
            number_of_err += 1
    return (number_of_err / total) * 100
