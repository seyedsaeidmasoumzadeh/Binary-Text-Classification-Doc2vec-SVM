from os import listdir
import gensim
import doc_iterator as DocIt



def run():
    docLabels = [f for f in listdir("Data/processed-training-data/") if f.endswith('.txt')]
    data = []
    for doc in docLabels:
        f = open("Data/processed-training-data/" + doc, 'r')
        data.append(f)
        f.close()
    it = DocIt.DocIterator(data, docLabels)
    model = gensim.models.Doc2Vec(size=300, window=8, min_count=5, workers=4, alpha=0.025, min_alpha=0.025, dm = 0, dbow_words=1) # use fixed learning rate
    model.build_vocab(it)
    print ("-----Doc2vec Training Started----")
    for epoch in range(10):
        print("epoch is: " + str(epoch))
        model.train(it)
        model.alpha -= 0.0025   # decrease the learning rate
        model.min_alpha = model.alpha   # fix the learning rate, no deca

    model.save("Models/doc2vec.model")
    print("Doc2vec model saved into the disk")