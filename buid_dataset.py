import gensim
import os
import nltk
import collections


def run(training_folder, label_file):
    doc2vec_model = gensim.models.Doc2Vec.load("Models/doc2vec.model")
    file_names = os.listdir(training_folder)
    label_dict = {}
    X = []
    y = []
    with open(label_file, "r") as label_file:
        lines = label_file.readlines()
        for line in lines:
            key, value = line.split(" ")
            label_dict[key] = str(value).replace("\r", "").replace("\r\n", "").replace("\n", "")
    labels = [item for item, count in collections.Counter(list(label_dict.values())).items() if count >= 1]
    for file_name in file_names:
        with open(training_folder + file_name, 'r') as f:
            lines = f.read()
        words = nltk.word_tokenize(lines)
        X.append(doc2vec_model.infer_vector(words))
        if label_dict[file_name.split("_")[0]] == labels[1]:
            y.append(1)
        else:
            y.append(-1)

    return X, y
