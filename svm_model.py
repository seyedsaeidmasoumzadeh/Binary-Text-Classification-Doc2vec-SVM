from sklearn.svm import SVC
from sklearn.externals import joblib


def run(X,y):
    print("SVM training started...")
    clf = SVC()
    svm_model = clf.fit(X, y)
    joblib.dump(svm_model, 'Models/svm.pkl')
    print("SVM model saved into the disk")