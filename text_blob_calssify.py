from textblob.classifiers import NaiveBayesClassifier

cl = NaiveBayesClassifier("train.csv", format="csv")
# print detect("train.csv")