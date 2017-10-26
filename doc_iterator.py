
import gensim
import nltk
nltk.download('punkt')
class DocIterator(object):
    def __init__(self, doc_list, labels_list):
       self.labels_list = labels_list
       self.doc_list = doc_list
    def __iter__(self):
        for idx, doc in enumerate(self.doc_list):
            f = open(doc.name,'r')
            lines = f.read()
            yield gensim.models.doc2vec.TaggedDocument(words=nltk.word_tokenize(lines),tags=[self.labels_list[idx]])

