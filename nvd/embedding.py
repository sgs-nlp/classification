def word_vectories(data, stopwords_list):
    from sklearn.feature_extraction.text import CountVectorizer
    count_vect = CountVectorizer(stop_words=stopwords_list)
    counts = count_vect.fit_transform(data.data)
    return counts
