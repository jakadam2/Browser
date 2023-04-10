import numpy as np
from collections import Counter
from sklearn.preprocessing import normalize
import scipy
from tools import Transformator
class QueastionLoader:
    def __init__(self,svdc,tokens_dict) -> None:
        self.svd_components = svdc
        self.