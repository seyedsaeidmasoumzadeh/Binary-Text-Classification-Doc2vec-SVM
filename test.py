
from sklearn.externals import joblib
from sklearn.metrics import recall_score, precision_score, confusion_matrix
import buid_dataset


def metrics(y, y_pred):
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    for index, element_y in enumerate(y):
        if element_y == 1:
            if y_pred[index] == -1:
                fn+= 1
            else:
                tp+= 1
        else:
            if y_pred[index] == -1:
                tn+= 1
            else:
                fp+= 1
    return tp, tn, fp, fn


print("Data set is building...")
X_train, y_train = buid_dataset.run("Data/processed-training-data/", "Data/training-class")
X_test, y_test = buid_dataset.run("Data/processed-test-data/", "Data/test-class")
loaded_model = joblib.load('Models/svm.pkl')
y_test_pred = loaded_model.predict(X_test[0:])
y_train_pred = loaded_model.predict(X_train[0:])
print("---- Train Results ----")
tp, tn, fp, fn = metrics(y_train, y_train_pred)
print ("True Positive = " + str(tp))
print ("False Positive  = " + str(fp))
print ("True Negative = " + str(tn))
print ("False Negative = " + str(fn))
print("---- Test Results ----")
tp, tn, fp, fn = metrics(y_test, y_test_pred)
print ("True Positive = " + str(tp))
print ("False Positive  = " + str(fp))
print ("True Negative = " + str(tn))
print ("False Negative = " + str(fn))
