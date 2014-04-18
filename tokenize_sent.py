# import nltk.data

# tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
# fp = open("right.txt")
# data = fp.read()
# print '\n----\n'.join(tokenizer.tokenize(data))

from textblob import TextBlob

fp = open("right.txt")
zen = TextBlob(fp.read())
zen.sentences

for sentence in zen.sentences:
	print "\"" + str(sentence) + "\"" + ",right"