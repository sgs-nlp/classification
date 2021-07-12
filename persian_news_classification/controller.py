from .models import News, StopWord

import pandas
from nvd.embedding import word_vectories


def classification_1():
    reference_title = 'statics_files/HamshahriData.xlsx'
    # load on database
    # ->
    news = News.objects.filter(reference__title=reference_title).all()
    # <-
    # pandas data frame
    # ->
    _data = []
    for itm in news:
        _data.append({'data': f'{itm.titr_string_code} {itm.content_string_code}', 'flag': itm.category.title_code})
    data = pandas.DataFrame(_data, columns=['data', 'flag'])
    # <-
    # load stopwords on database
    # ->
    _stopwords_list = StopWord.objects.filter(reference__title=reference_title).all()
    stopwords_list = []
    for word in _stopwords_list:
        stopwords_list.append(word.word.code)
    # <-
    # word embeding
    # ->
    data_counts = word_vectories(data, stopwords_list)
    # <-
    # calculate tfidf
    # ->
    from sklearn.feature_extraction.text import TfidfTransformer
    tfidf_transformer = TfidfTransformer()
    data_tfidf = tfidf_transformer.fit_transform(data_counts)
    # <-
    # create ml model
    # ->
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(data_tfidf, data.flag, test_size=0.25,
                                                        random_state=42)
    clf = MultinomialNB().fit(X_train, y_train)
    # <-
