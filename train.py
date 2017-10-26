import data_cleaning
import doc2vec_model
import svm_model
import buid_dataset



print("Data set is building...")
data_cleaning.process("Data/training-data/", "Data/processed-training-data/")
print("Doc2vec is training. Please wait...")
doc2vec_model.run()
print("Data set is building...")
X_train, y = buid_dataset.run("Data/processed-training-data/", "Data/training-class")
svm_model.run(X_train,y)