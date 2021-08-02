from gensim.test.utils import common_texts
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.test.utils import get_tmpfile
from os import path
from nvd.normalizer import matrix_scale_matrix
import numpy


class GDoc2Vec:
    def __init__(
            self,
            data=None,
            file_name='model.gensim.d2v',
            vector_size=100,  # todo 2 ** 8,
            dm_mean=1,
            dm=1,
            dbow_words=1,
            dm_concat=1,
            dm_tag_count=1,
            window=3,  # todo 2**4,
            epochs=5  # todo 2**10
    ):
        self.vector_size = vector_size
        self.dm_mean = dm_mean
        self.dm = dm
        self.dbow_words = dbow_words
        self.dm_concat = dm_concat
        self.dm_tag_count = dm_tag_count
        self.window = window
        self.epochs = epochs
        if data is not None:
            documents = [TaggedDocument(itm, [i]) for i, itm in enumerate(data)]
            self.model = Doc2Vec(
                documents=documents,
                vector_size=self.vector_size,
                dm_mean=self.dm_mean,
                dm=self.dm,
                dbow_words=self.dbow_words,
                dm_concat=self.dm_concat,
                dm_tag_count=self.dm_tag_count,
                window=self.window,
                epochs=self.epochs,
            )
        elif path.exists(file_name):
            self.model = Doc2Vec.load(file_name)
        else:
            raise Exception('Error: model is not exist and data is None.')
        fname = get_tmpfile(file_name)
        self.model.save(fname)

    @property
    def vectors(self):
        return self.model.docvecs.vectors

    def d2v(self, document):
        pass


class BOWDoc2vec:
    def __init__(self, data, dictionary):
        self.data = data
        _dictionary = {}
        i = 0
        for itm in dictionary:
            i += 1
            _dictionary[itm.code] = i

        self.dictionary = _dictionary
        self._vectors = None

    @property
    def vectors(self):
        if self._vectors:
            return self._vectors
        _data = self.data
        for i in range(len(_data)):
            for j in range(len(_data[i])):
                _data[i][j] = self.dictionary[_data[i][j]]
        self._vectors = _data
        return self._vectors


class OneHotDoc2vec:
    def __init__(self, data, dictionary):
        self.data = data
        _dictionary = {}
        i = 0
        for itm in dictionary:
            _dictionary[itm.code] = i
            i += 1

        self.dictionary = _dictionary
        self._vectors = None

    @property
    def vectors(self):
        if self._vectors:
            return self._vectors
        len_dictionary = len(self.dictionary)
        _data = []
        for i in range(len(self.data)):
            _doc = numpy.zeros(len_dictionary)
            for j in range(len(self.data[i])):
                _doc[self.dictionary[self.data[i][j]]] = 1
            _data.append(_doc)
        self._vectors = numpy.array(_data)
        return self._vectors
