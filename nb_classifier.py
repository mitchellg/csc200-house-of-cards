"""This is navie bayes classifier to classify the text speech.
1. data preprocessing  --- remove some useless puntuaitons in speech, and tokenize the text. 
2. training            --- train the classifier by using the training data in 
                            left.txt, right.txt, libertarian.txt, statist.txt 
3. validation test     --- not finished yet. validation data will be stored in validation.txt
                            it will calculate the accuracy of classifier. 
"""


import collections
import math
import re
from nltk import bigrams

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
    speeches = re.sub("%[0-9|.]*", ' ', speeches)
    speeches = re.sub("\$[0-9|.]*", ' ', speeches)
    for ch in '$!"@#%&()*+,-./:;<=>?[\\]^_`{|}~':
        speeches = speeches.replace(ch,' ')
    
    tokens = speeches.split()
    #tokens = bigrams(tokens)                    # uncomment this line, we can use bigram as 
    total_tokens_count = len(tokens)
    unique_tokens_dict = collections.Counter(tokens)   #key is word, value is the count, 
                                                    #also default value 0 for non-exsit key.
    
    result = [ speech_list, unique_tokens_dict, total_tokens_count ]
    return result


# input: path for training data file
# return: a dictionray with all training result        
def training(file1_path, file2_path, file3_path, file4_path):
    result1      = data_preprocessing(file1_path)
    result2      = data_preprocessing(file2_path)
    result3      = data_preprocessing(file3_path)
    result4      = data_preprocessing(file4_path)
    
    all_training_speeches = result1[0] + result2[0] + result3[0] + result4[0]
    prob_1 = float( len(result1[0]) ) / len(all_training_speeches) 
    prob_2 = float( len(result2[0]) ) / len(all_training_speeches) 
    prob_3 = float( len(result3[0]) ) / len(all_training_speeches) 
    prob_4 = float( len(result4[0]) ) / len(all_training_speeches)
    

    #write all class's training speeches into text file
    # and do data preprocessing to get the training_unique_words_count
    file5_path = 'all_training_speeches.txt'
    f = open(file5_path,'w')
    for speech in all_training_speeches:
        f.write(speech + ' ###')
    f.close()
    result_total = data_preprocessing(file5_path)
    
    training_result = {'prob_1':prob_1,'prob_2':prob_2,'prob_3':prob_3,'prob_4':prob_4,
            'training_unique_tokens_count':len(result_total[1]),
            'unique_tokens_dict_1':result1[1], 'total_tokens_count_1':result1[2],
            'unique_tokens_dict_2':result2[1], 'total_tokens_count_2':result2[2],
            'unique_tokens_dict_3':result3[1], 'total_tokens_count_3':result3[2],
            'unique_tokens_dict_4':result4[1], 'total_tokens_count_4':result4[2]
            } 

    return training_result



# classify a testing data with training result
def classify(training_result, test_speech):
    
    prob_1 = training_result['prob_1']
    prob_2 = training_result['prob_2']
    prob_3 = training_result['prob_3']
    prob_4 = training_result['prob_4']
    training_unique_tokens_count = training_result['training_unique_tokens_count']
    unique_tokens_dict_1  = training_result['unique_tokens_dict_1']
    unique_tokens_dict_2  = training_result['unique_tokens_dict_2']
    unique_tokens_dict_3  = training_result['unique_tokens_dict_3']
    unique_tokens_dict_4  = training_result['unique_tokens_dict_4']
    total_tokens_count_1  = training_result['total_tokens_count_1']
    total_tokens_count_2  = training_result['total_tokens_count_2']
    total_tokens_count_3  = training_result['total_tokens_count_3']
    total_tokens_count_4  = training_result['total_tokens_count_4']
    test_speech = test_speech.lower()

    for ch in '!"%&()*+,-./:;<=>?[\\]^_`{|}~':
        test_speech = test_speech.replace(ch,' ')
        
    test_speech_tokens = test_speech.split()
    log_prob_1         = math.log(prob_1,2)   # use log for easy addtion, because do multiplicaiton 
    log_prob_2         = math.log(prob_2,2)   # among a lot small values will result in overflow
    log_prob_3         = math.log(prob_3,2)
    log_prob_4         = math.log(prob_4,2)
    

    #calculate every token's probability for each class
    for token in test_speech_tokens:
        # use +1 smoothing to avoid 0 probability. 
        log_prob_1 = log_prob_1 + math.log( float( (unique_tokens_dict_1[token] + 1 )) / (total_tokens_count_1 + training_unique_tokens_count), 2)
        log_prob_2 = log_prob_2 + math.log( float( (unique_tokens_dict_2[token] + 1 )) / (total_tokens_count_2 + training_unique_tokens_count), 2)
        log_prob_3 = log_prob_3 + math.log( float( (unique_tokens_dict_3[token] + 1 )) / (total_tokens_count_3 + training_unique_tokens_count), 2)
        log_prob_4 = log_prob_4 + math.log( float( (unique_tokens_dict_4[token] + 1 )) / (total_tokens_count_4 + training_unique_tokens_count), 2)
        
    
    #choose the class with highest probability 
    if log_prob_1 == max(log_prob_1, log_prob_2, log_prob_3, log_prob_4):
        print('class_left')
        return 'class_left'
    elif log_prob_2 == max(log_prob_1, log_prob_2, log_prob_3, log_prob_4):
        print('class_right')
        return 'class_right'
    elif log_prob_3 == max(log_prob_1, log_prob_2, log_prob_3, log_prob_4):
        print('class_libertarian')
        return 'class_libertarian'
    elif log_prob_4 == max(log_prob_1, log_prob_2, log_prob_3, log_prob_4):  
        print('class_statist')
        return 'class_statist'




# For testing
if __name__ == '__main__':
    file1_path = 'left.txt'
    file2_path = 'right.txt'
    file3_path = 'libertarian.txt'
    file4_path = 'statist.txt'
   
    test_speech = "I am so pleased I had a role in drafting this remarkable document. It embodies the values we hold dear as Democrats and as Americans, and it sets forth our great president's vision for our future where together we will reignite the American Dream for all. Because the reality is: Four years ago, the American Dream had slipped out of reach for too many, and it had turned into a nightmare for millions."

    training_result = training(file1_path, file2_path, file3_path, file4_path)
    classify(training_result, test_speech)


