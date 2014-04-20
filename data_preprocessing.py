import collections
import math
import re
from nltk import bigrams
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import word_tokenize

#input: path for file
#return: a list of speech
#in text file, speeches are seperated by "###" mark.
def data_preprocessing(file_path):
    f = open(file_path,'r')
    speech_list = f.read().split("###")   # read speeches, split with ###, and save them into list.
    del speech_list[-1]
    f.close()
    #print len(speech_list)
    f = open(file_path,'r')
    speeches = f.read().lower()    #set all letters lower case
    speeches = re.sub('http://[a-zA-Z0-9|/|.]*',' ',speeches)
    speeches = re.sub('%[0-9|.]*', ' ', speeches)
    speeches = re.sub('$[0-9|.]*',' ', speeches)
    #speeches = re.sub('\\\\xe2\\\\x80\\\\x[a-zA-Z0-9]*',' ',speeches)
    #print speeches
    for ch in " \"$!'@#%&()*+,-./:;<=>?[\\]^_`{|}~ ":
        speeches = speeches.replace(ch,' ')

    tokens = speeches.split()
    
    #word lemmatization
    lmtzr = WordNetLemmatizer()
    tokens = [lmtzr.lemmatize(token) for token in tokens]
    tokens = [lmtzr.lemmatize(token,'v') for token in tokens]

    #tokens = bigrams(tokens)                    # uncomment this line, we can use bigram as

    total_tokens_count = len(tokens)
    unique_tokens_dict = collections.Counter(tokens)   #key is word, value is the count,
                                                       #also default value 0 for non-exsit key.

    result = [ speech_list, unique_tokens_dict, total_tokens_count ]
    return result
