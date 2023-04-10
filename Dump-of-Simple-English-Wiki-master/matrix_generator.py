import scipy
from collections import Counter
import numpy as np
from sklearn.preprocessing import normalize
from sklearn.decomposition import TruncatedSVD
from tools import DataLoader,Transformator

class MatrixGenerator:
    def __init__(self,file_name) -> None:
        self._loader = DataLoader(file_name)
        self._file_name = file_name
        self._tranformator = Transformator()
        self._tokens_dict = self.__create_tokens_dict()
        self.number_of_articles = self.__count_articles()
        self.matrix = self.__create_matrix()
        self.contents = None
        self.svd = None

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
        matrix = scipy.sparse.lil_matrix((self.number_of_articles,len(self._tokens_dict)))
        for i in range(self.number_of_articles):
            list = self._tranformator.transform(self._loader.next())
            counter = Counter(list)
            for word in counter:
                matrix[i,self._tokens_dict[word]] = counter[word]
        self.contents = self._loader.contents
        return matrix
    
    def __idf(self):
        accidents = scipy.sparse.linalg.norm(self.matrix,ord = 0, axis = 1)
        idf = np.log(self.number_of_articles/accidents)
        self.matrix = (self.matrix.T.multiply(idf)).T

    def __normalize(self):
        self.matrix = normalize(self.matrix,axis=0)

    def _svd(self,k):
        self.svd = TruncatedSVD(n_components = k).fit(self.matrix.T)
        self.matrix = self.svd.transform(self.matrix.T)

    
