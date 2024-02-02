import numpy as np
from collections import Counter
from sklearn.preprocessing import normalize
import scipy
from tools import Transformator


class QueastionLoader:

    def __init__(self,svdc,tokens_dict) -> None:
        self.svd_components = svdc
        self.tokens_dict = tokens_dict
        self.tr = Transformator()

    def create_vector(self,sentence):
        list = self.tr.transform(sentence)
        q = scipy.sparse.lil_matrix((len(self.tokens_dict),1))
        counter = Counter(list)
        for word in counter:
            q[self.tokens_dict[word],0] = counter[word]
        q = normalize(q,axis = 0)
        return q

    def rebase_vector(self,vector):
        return self.svd_components.dot(vector.todense())
    
    def load(self,sentence):
        vec = self.create_vector(sentence)
        return self.rebase_vector(vec)