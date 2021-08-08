from json import loads
from math import log as logarithm
import os
from classification.settings import BASE_DIR

STOP_WORDS_PATH = os.path.join(BASE_DIR, 'nvd', 'persian.stopword.json')


class Stopwords:
    def __init__(self, stopwords_list: list = None) -> None:
        """
        in kelas baraye modiriyate stop word ha sakhte shude ast k mitavanad list stop word ha ra daryaft konad,
         ya list pishfarz khod ra stefade konad va ya
        bar asase ferekanse kalamat dar corpus, list stop word ra besazad.
        :param stopwords_list: yek listre paythoni shamele stop word haye farsi
        """
        if stopwords_list is not None:
            self.STOPWORDSLIST = stopwords_list
        else:
            with open(STOP_WORDS_PATH, 'r', encoding='utf-8') as file:
                s = file.read()
                s = loads(s)
            self.STOPWORDSLIST = s

    def is_stopword(self, word: str) -> bool:
        """
        dar in tabe bar asase stop word haye tarif shude dar in class moshakas mikonad k
        kalameye vorodi stop word ast ya na.
        :param word: kalameye farsi - reshteye pythoni
        :return: meghdare bargashtiy in tabe be sorate boolean mibashad va moshakhas mikonad k
         kalameye vorodi stopword ast ya kheyr
        """
        if word in self.STOPWORDSLIST:
            return True
        return False

    def stopword_extractor_by_ferquency(self, corpus: list) -> list:
        """
        in tabe liste pythoniye stopword ra bar asase ferquency kalamat darone corpus moshakhas mikonad.
        :param corpus: listi shamele tamame document haye mojod
        :return: list pythoni shamele stopword ha.
        """
        pass

    def without_stopwords(self, document: list, sents=1) -> list:
        """
        in tabe yek document ra k shamele listi az jomalat va har jomle shamele listi az kalamat mibashad va dar nahayat
        stopwords hara hazf mikonad va dar ghalebe yek list az kalamat an ra bar migardanad.
        dar sorati k sents barabare ba sefr bashad kalamate daron yek document faregh az jomle darnazar gerefte khahad
        shod.

        :param document:
        :return:
        """
        res = []
        if sents:
            for sent in document:
                tmp = []
                for wrd in sent:
                    if not self.is_stopword(wrd):
                        tmp.append(wrd)
                res.append(tmp)
            return res
        else:
            for wrd in document:
                if not self.is_stopword(wrd):
                    res.append(wrd)
            return [res]


class Keywords:
    def __init__(self, stopwords_list: list = None, minimum_frequency: float = 0,
                 maximum_frequency: float = 1, keywords_number: int = -1, fre=False) -> None:
        """
        in kelas modiriyate keyword ha ra anjam midahad.
        :param stopwords_list: list paythoni az stopword ha.
        :param minimum_frequency: adadi beyene sefr va yek,
         kamtarin frquency ehtemali baraye shenasayi kalamate ba arzeshe bishtar.
        :param maximum_frequency: adadi beyene sefr va yek,
         bishtarin frquency ehtemali baraye shenasayi kalamate ba arzeshe bishtar.
        """
        self.fre = fre
        self.keywords_number = keywords_number
        if stopwords_list is not None:
            self.stopwords_list = stopwords_list

        self.minimum_frequency = minimum_frequency
        self.maximum_frequency = maximum_frequency

        fry = Frequency(self.stopwords_list)
        self.frequency_func = fry.normal_tfidf

    stopwords_list = []

    def by_frequency(self, document: list, stopword=0, sents=1, func=None) -> list:
        """
        estekhraje keyword ha bar asase bedast avardane ferekanse kalamat dar yek matn
        :param document: yek liste pythoni shamele kalamate darone document(b in sorat document = ['w1','w2', ...]).
        :param func: dar inja shuma mitavanid tabe mohasebeye ferekans more taeid khod ra entekhab konid,
        dar hale hazer pishfarz ma az tabe Frequency.normal_tfidf ast.
        :return: liste pythoni shamele kywords ha.
        """
        if stopword == 0:
            return self._by_fre(document, func)
        if stopword == 1:
            stpw = Stopwords()
            document = stpw.without_stopwords(document, sents=sents)
            return self._by_fre(document, func)

    def _by_fre(self, document: list, func=None) -> list:
        """
        estekhraje keyword ha bar asase bedast avardane ferekanse kalamat dar yek matn
        :param document: yek liste pythoni shamele kalamate darone document(b in sorat document = ['w1','w2', ...]).
        :param func: dar inja shuma mitavanid tabe mohasebeye ferekans more taeid khod ra entekhab konid,
        dar hale hazer pishfarz ma az tabe Frequency.normal_tfidf ast.
        :return: liste pythoni shamele kywords ha.
        """
        if func is None:
            func = self.frequency_func
        keywords = []
        res = func(document)
        res = dict(sorted(res.items(), key=lambda item: item[1], reverse=True))
        if self.fre:
            for (word, value) in res.items():
                if self.minimum_frequency <= value <= self.maximum_frequency:
                    keywords.append({'word': word, 'frequency': value})
            return keywords[:self.keywords_number]

        for (word, value) in res.items():
            if self.minimum_frequency <= value <= self.maximum_frequency:
                keywords.append(word)

        return keywords[:self.keywords_number]


class Frequency:
    def __init__(self, stopwords_list: list = None):
        """
        mohasebeye ferekanse kalamat dar matn bar asase algorithm haye mokhtalef.
        :param stopwords_list: ba estefade az in vorodi mitavanid ferekanse kalamate gheyere stopword dar matn ra
        mohasebe konid.
        agar in moteghayr ra meghdar dehi nakonid tabe be sorate pishfarz fekanse tamae kalamate mojod dar matn ra
        mohasebe mikonad.
        """
        if stopwords_list is not None:
            self._stopwords_list = stopwords_list

    _stopwords_list = []

    def tfidf(self, document: list) -> dict:
        """
        in tabe az raveshe marofe tfidf baraye bedast avardane ferekanse kalamat estefade mikonad.
        :param document: documenti k be sorate yek string pythoni ast va mikhahim kalamte ba arzeshe an ra estekhraj
            konim.

        :return: yek dictionary pythoni bar migardanad k keyword haye an kalamate darone document ast va value an
        barabarast ba meghdare tfidf mohasebe shude.
        """
        sum_all_fre = 0
        for sent in document:
            sum_all_fre += len(sent)

        document_term_frequency = {}
        for sent in document:
            for word in sent:
                if word not in self._stopwords_list:
                    if word not in document_term_frequency:
                        document_term_frequency[word] = 1 / sum_all_fre
                    else:
                        document_term_frequency[word] += 1 / sum_all_fre

        document_tfidf = {}

        for (word, tf) in document_term_frequency.items():
            document_tfidf[word] = tf * (logarithm(1 / tf))

        return document_tfidf

    def normal_tfidf(self, document: list) -> dict:
        """
        in tabe az raveshe tfidf baraye pyda kardane ferekanse kalamat estefade mikonad va dar nahayat ba
        mohasebeye bishtarin ferekanse va kamatarin ferekanse ferekanse kalamat dar matn ra b adadi
         beyne sefr va yek negasht midahad.
        :param document: documenti k be sorate yek string pythoni ast va mikhahim kalamte ba arzeshe an ra estekhraj
            konim.


        :return: yek dictionary pythoni bar migardanad k keyword haye an kalamate darone document ast va value an
        barabarast ba meghdare tfidf mohasebe shude.
        """
        document_tfidf = self.tfidf(document)

        values = document_tfidf.values()
        maximum_frequency = max(values)
        minimum_frequency = min(values)
        for (word, value) in document_tfidf.items():
            if minimum_frequency == maximum_frequency:
                document_tfidf[word] = 1
                continue
            document_tfidf[word] = (value - minimum_frequency) / (maximum_frequency - minimum_frequency)
        return document_tfidf
