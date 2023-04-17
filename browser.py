from matrix_generator import MatrixGenerator
from question_loader import QueastionLoader


class Browser:
    def __init__(self,file_name) -> None:
        matrix_gen = MatrixGenerator(file_name,1000)
        self.question_loader = QueastionLoader(matrix_gen.get_svdc(),matrix_gen.get_tokens())
        self.matrix = matrix_gen.matrix
        self.names = matrix_gen.contents

    def search(self,question):
        cors = self.matrix.dot(self.question_loader.load(question))
        ans = []
        for i in range(cors.shape[0]):
            ans.append((self.names[i],cors[i,0]))
        ans.sort(key= lambda x: x[1],reverse= True)
        return ans
