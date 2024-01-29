import nltk

class DataLoader:
    def __init__(self,file_name) -> None:
        self.file = open(file_name,encoding = 'utf8')
        self.contents = []

    def next(self):
        ans = ''
        line = self.file.readline()
        self.contents.append(line[:-1])
        while line != '\n' and line != '':
            ans += line
            line = self.file.readline()
        return ans
    

class Transformator:
    def __init__(self) -> None:
        self.stemer = nltk.stem.PorterStemmer()
        self.stop_words = set(nltk.corpus.stopwords.words('english'))

    def transform(self,text):
        tokens = set(nltk.tokenize.WordPunctTokenizer().tokenize(text))
        stemed_tokens = [self.stemer.stem(token) for token in tokens if len(token) > 3 and token.lower() not in self.stop_words]
        return stemed_tokens
    
class ArticleFinder:
    def __init__(self,name) -> None:
        self.name = name
        self.name_dict = self.create_dict(name)

    def create_dict(self,name):
        file = open(name,encoding = 'utf8')
        name_dict = {}
        while True:
            ans = ''
            line = file.readline()
            name = line[:-1]
            while line != '\n' and line != '':
                ans += line
                line = file.readline()
            if ans == '':
                break
            name_dict[name] = ans
        return name_dict
    
    def get(self,name):
        return self.name_dict[name]
        