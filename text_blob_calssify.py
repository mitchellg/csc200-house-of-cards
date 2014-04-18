from textblob.classifiers import NaiveBayesClassifier
from text.blob import TextBlob

cl = NaiveBayesClassifier("train.csv", format="csv")

# Classify some text
# print(cl.classify("Their burgers are amazing."))  # "pos"
# print(cl.classify("I don't like their pizza."))   # "neg"
 
# Classify a TextBlob
blob = TextBlob("The President's budget makes these investments while reducing the deficit by raising revenues from millionaires, billionaires, and corporations that are not paying their fair share.The President's budget would restore unemployment compensation to the long-term unemployed who are struggling to find work and to make ends meet. Due to Congress's inaction more than 2 million Americans (including more than 112,000 Illinoisans) have lost long-term unemployment insurance benefits.His budget also takes common-sense, long overdue steps that will boost our economy:  increasing the federal minimum wage and moving forward with comprehensive immigration reform.These proposals would truly help Americans succeed and build an economy that works for everyone. Congress should embrace them and expand opportunities for all Americans.I am very thankful that President Barack Obama has named March 2014 National Colorectal Cancer Awareness Month. All types of cancer continue to claim too many lives in our country and around the world.", classifier=cl)
print(blob)
print(blob.classify())
 
for sentence in blob.sentences:
    print(sentence)
    print(sentence.classify())
 
# Compute accuracy
print("Accuracy: {0}".format(cl.accuracy("test.csv", format="csv")))
 
# Show 5 most informative features
cl.show_informative_features(10)