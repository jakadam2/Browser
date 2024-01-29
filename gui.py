from PyQt6.QtWidgets import QApplication,QWidget, QPushButton, QLabel ,QLineEdit
from PyQt6.QtGui import QPixmap, QFont, QFontDatabase
from PyQt6 import QtCore
from browser import Browser
from tools import ArticleFinder

class ResultWindow(QWidget):
    def __init__(self,result,name,finder) -> None:
        super().__init__()
        self.result = result
        self.name = name
        self.finder = finder
        self.ans = ''
        self.nr_of_article = 0
        self.content_label = None
        print(result[:20])
        self.setup()
        
    def setup(self):
        width = 400
        height = 700
        self.setFixedSize(width,height)
        self.setWindowTitle('Result')
        self.setStyleSheet("background-color: white;")

        pix_label = QLabel(self)
        pix_map = QPixmap('D:\Studia\mownit\wyszukiwarka\img2.png')
        pix_label.setPixmap(pix_map)
        pix_label.move((width - 193)/2,0)
        	
        name_label = QLabel(self)
        name_font = QFont()
        name_font.setBold(True)
        name_font.setStyleName('Times')
        name_font.setPointSize(12)
        name_label.setFont(name_font)
        name_label.setFixedSize(390,40)
        name_label.setText('Wyniki wyszukiwania dla zapytania "' + self.name + '"') 
        name_label.move(10,70)

        self.rate_label = QLabel(self)
        rate_font = QFont()
        rate_font.setStyleName('Times')
        rate_font.setPointSize(12)
        self.rate_label.setFont(rate_font)
        self.rate_label.setFixedSize(390,40) 
        self.rate_label.move(10,113)
        self.rate_label.setText(str(self.nr_of_article + 1) +'. Współczynnik dopasowania: ' + str(round(self.result[self.nr_of_article][1],3)))


        self.content_label  = QLabel(self)
        self.content_label.setFixedSize(390,600)
        self.content_label.move(10,150)
        self.content_label.setWordWrap(True)
        self.content_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.content_label.setText(self.finder.get((self.result[self.nr_of_article][0])))


        next_btn = QPushButton('Next',self)
        next_btn.setFixedSize(80,30)
        next_btn.move(width - 80,670)        
        next_btn.setStyleSheet("background-color: white ;border-style: outset;border-width: 2px;border-radius: 10px;border-color: black ;font: bold 14px ; padding: 6px;")  

        prev_btn = QPushButton('Previous',self)
        prev_btn.setFixedSize(80,30)
        prev_btn.move(0,670)
        prev_btn.setStyleSheet("background-color: white ;border-style: outset;border-width: 2px;border-radius: 10px;border-color: black ;font: bold 14px ; padding: 6px;")    

        # conecting
        prev_btn.clicked.connect(self.prev_btn_action)
        next_btn.clicked.connect(self.next_btn_action)

        self.show()

    def quit(self):
        QApplication.instance().quit

    def next_btn_action(self):
        if self.nr_of_article < len(self.result) - 1:
            self.nr_of_article += 1
        self.content_label.setText(self.finder.get((self.result[self.nr_of_article][0])))
        self.rate_label.setText(str(self.nr_of_article + 1) +'. Współczynnik dopasowania: ' + str(round(self.result[self.nr_of_article][1],3)))

    def prev_btn_action(self):
        if self.nr_of_article > 0: 
            self.nr_of_article -= 1
        self.content_label.setText(self.finder.get((self.result[self.nr_of_article][0])))
        self.rate_label.setText(str(self.nr_of_article + 1) +'. Współczynnik dopasowania: ' + str(round(self.result[self.nr_of_article][1],3)))
        

class StartWindow(QWidget):
    def __init__(self,browser,finder) -> None:
        super().__init__()
        self.results = []
        self.browser = browser
        self.finder = finder
        self.search_line_edit = None
        self.setup()
        
    def setup(self):
        width = 800
        height = 500
        self.setFixedSize(width,height)
        self.setWindowTitle('Browser')
        self.setStyleSheet("background-color: white;")
        self.dialogs = []

        pix_label = QLabel(self)
        pix_map = QPixmap('D:\Studia\mownit\wyszukiwarka\img.png')
        pix_label.setPixmap(pix_map)
        pix_label.move(260,100)

        search_btn = QPushButton('Wyszukaj',self)
        search_btn.setFixedSize(100,40)
        search_btn.move((width - 200)/2,280)
        search_btn.setStyleSheet("background-color: white ;border-style: outset;border-width: 2px;border-radius: 10px;border-color: black ;font: bold 14px ;min-width: 10em; padding: 6px;")

        self.search_line_edit = QLineEdit(self,placeholderText = 'Wpisz zapytanie')
        self.search_line_edit.setFixedSize(400,60)
        self.search_line_edit.move((width - 400)/2,200)
        self.search_line_edit.setStyleSheet("background-color: white ;border-style: outset;border-width: 2px;border-radius: 10px;border-color: black ;font: bold 14px ;min-width: 10em; padding: 6px;")
        
        #connecting
        search_btn.clicked.connect(self.search_btn_action)


        self.show()
    
    def search_btn_action(self):
        name = self.search_line_edit.text()
        result = self.browser.search(name)
        self.results.append(ResultWindow(result,name,finder))
        self.search_line_edit.clear()
  
        
        pass


if __name__ == '__main__':
    browser = Browser('corpus.txt')
    finder = ArticleFinder('corpus.txt')
    app = QApplication([])
    start_window = StartWindow(browser,finder)
    app.exec()

