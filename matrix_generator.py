import scipy
from collections import Counter
import numpy as np
from sklearn.preprocessing import normalize
from sklearn.decomposition import TruncatedSVD
from tools import DataLoader,Transformator
import nltk


class MatrixGenerator:

    def __init__(self,file_name,k) -> None:
        self.contents = None
        self.svd = None
        self._loader = DataLoader(file_name)
        self._file_name = file_name
        self._tranformator = Transformator()
        self._tokens_dict = self.__create_tokens_dict()
        self.number_of_articles = self.__count_articles()
        self.matrix = self.__create_matrix()
        self.matrix = self.__idf()
        self.matrix = self.__normalize()
        self.matrix = self._svd(k)

    def __create_tokens_dict(self):
        file = open(self._file_name,encoding = 'utf8')
        text = file.read()
        tokens = set(self._tranformator.transform(text))
        tokens_dict = {token:nr for nr,token in enumerate(tokens)}
        return tokens_dict
    
    def __count_articles(self):
        file = open(self._file_name,encoding = 'utf8')
        text = file.readlines()
        number_of_articles = text.count('\n')
        return number_of_articles + 1
    
    def __create_matrix(self):
        matrix = scipy.sparse.lil_matrix((len(self._tokens_dict),self.number_of_articles))
        stemer = nltk.stem.PorterStemmer()
        gen = DataLoader('./resources/data/corpus.txt')
        stop_words = set(nltk.corpus.stopwords.words('english'))
        for i in range(self.number_of_articles):
            tokens = nltk.tokenize.WordPunctTokenizer().tokenize(gen.next())
            list = [stemer.stem(token) for token in tokens if len(token) > 3 and token.lower() not in stop_words ]
            counter = Counter(list)
            for word in counter:
                matrix[self._tokens_dict[word],i] = counter[word]
        self.contents = gen.contents
        return matrix
    
    def __idf(self):
        accidents = scipy.sparse.linalg.norm(self.matrix,ord = 0, axis = 1)
        idf = np.log(self.number_of_articles/accidents)
        return self.matrix.T.multiply(idf).T

    def __normalize(self):
        return normalize((self.matrix),axis = 0)

    def _svd(self,k):
        self.svd = TruncatedSVD(n_components = k).fit(self.matrix.T)
        return self.svd.transform(self.matrix.T)

    def get_tokens(self):
        return self._tokens_dict
    
    def get_svdc(self):
        return self.svd.components_