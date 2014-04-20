import collections
import re
import random
from sklearn import svm
from nltk import bigrams
from nltk.stem.wordnet import WordNetLemmatizer
from data_preprocessing import data_preprocessing as dp


def feature_extraction(unique_tokens_dict1, unique_tokens_dict2):
    most_common_tokens_dict1 = dict( unique_tokens_dict1.most_common()[:500] )
    most_common_tokens_dict2 = dict( unique_tokens_dict2.most_common()[:500] )
    features =  [ token for token in set(most_common_tokens_dict1) | set(most_common_tokens_dict2) ]
    #print features 
    return features


def convert_speeches_into_matrix(features,speech_list,label):    
    sample_matrix = []
    label_vector  = []
    #print len(features)
    for speech in speech_list:
        sample = []
        speech = re.sub('http://[a-zA-Z0-9|/|.]*',' ',speech)
        speech = re.sub('%[0-9|.]*', ' ', speech)
        speech = re.sub('$[0-9|.]*',' ', speech)
        for ch in " \"$!'@#%&()*+,-./:;<=>?[\\]^_`{|}~ ":
            speech = speech.replace(ch,' ')

        tokens = speech.split()
        
        #word lemmatization
        lmtzr = WordNetLemmatizer()
        tokens = [lmtzr.lemmatize(token) for token in tokens]
        tokens = [lmtzr.lemmatize(token,'v') for token in tokens]

        #tokens = bigrams(tokens)                    # uncomment this line, we can use bigram as
        unique_tokens_dict = collections.Counter(tokens)

        for fea in features:
            if fea in unique_tokens_dict:
                sample.append(unique_tokens_dict[fea])
            else:
                sample.append(0)
       
        #print(sample)
        sample_matrix.append(sample)
        label_vector.append(label)
    
    return sample_matrix,label_vector
                

def svm_training(file1_path,file2_path):
    result1 = dp(file1_path)
    result2 = dp(file2_path)
    speech_list1 = result1[0]
    speech_list2 = result2[0]
    unique_tokens_dict1 = result1[1]
    unique_tokens_dict2 = result2[1]

    features = feature_extraction(unique_tokens_dict1, unique_tokens_dict2)
    left_sample_matrix, left_label_vector   = convert_speeches_into_matrix(features, speech_list1, label = 0)   # left  == 0
    right_sample_matrix, right_label_vector = convert_speeches_into_matrix(features, speech_list2, label = 1)   # right == 1
    X_matrix = left_sample_matrix + right_sample_matrix
    Y_vector = left_label_vector  + right_label_vector
    #print features 
    clf = svm.SVC()
    
    #clf.fit(X_matrix[:-2],Y_vector[:-2])
    #print clf.predict(X_matrix[-1])
    #length_of_fold = len(X_matrix) / 5
    average_accuracy = 0
    for i in range(10):
        X_matrix_clone = list(X_matrix)
        Y_vector_clone = list(Y_vector)
        X_matrix_test  = []
        Y_vector_test  = []
        for j in range(10):
            length = len(X_matrix_clone)
            #print "matrix_len", length
            random_num     = random.randint(0,length-1)
            X_matrix_test.append(X_matrix_clone[random_num])
            Y_vector_test.append(Y_vector_clone[random_num])
            del X_matrix_clone[random_num]
            del Y_vector_clone[random_num]
        
        #print X_matrix_test
        #print Y_vector_clone
        #print X_matrix_test
        clf.fit(X_matrix_clone,Y_vector_clone)
        Y_test_predict = clf.predict(X_matrix_test)
        #print Y_test_predict
        Y_test_predict = list(Y_test_predict)

        #print "Y_vector_test", Y_vector_test
        #print "Y_test_predict", Y_test_predict
        #print "\n"
        count = 0
        for k in range(10):
            if Y_vector_test[k] == Y_test_predict[k]:
                count += 1
        accuracy = float(count) / len(Y_vector_test)
        #print 'accuracy', accuracy
        average_accuracy += accuracy 
    print "average_accuracy", average_accuracy/10

if __name__ == '__main__':
    file1_path = 'left.txt'
    file2_path = 'right.txt'
    clf = svm_training(file1_path,file2_path)

