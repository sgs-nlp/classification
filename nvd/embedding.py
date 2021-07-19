from gensim.test.utils import common_texts
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.test.utils import get_tmpfile
from os import path
from nvd.normalizer import matrix_scale_matrix


class GDoc2Vec:
    def __init__(
            self,
            data=None,
            file_name='model.gensim.d2v',
            vector_size=100,
            dm_mean=None,
            dm=1,
            dbow_words=0,
            dm_concat=0,
            dm_tag_count=1,
            dv=None,
            dv_mapfile=None,
            comment=None,
            trim_rule=None,
            callbacks=(),
            window=5,
            epochs=10
    ):
        self.vector_size = vector_size
        self.dm_mean = dm_mean
        self.dm = dm
        self.dbow_words = dbow_words
        self.dm_concat = dm_concat
        self.dm_tag_count = dm_tag_count
        self.dv = dv
        self.dv_mapfile = dv_mapfile
        self.comment = comment
        self.trim_rule = trim_rule
        self.callbacks = callbacks
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
                dv=self.dv,
                dv_mapfile=self.dv_mapfile,
                comment=self.comment,
                trim_rule=self.trim_rule,
                callbacks=self.callbacks,
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
        return matrix_scale_matrix(self.model.docvecs.vectors)

    def d2v(self, document):
        pass
