#Importing libraries
import nltk
nltk.download('treebank')
nltk.download('universal_tagset')
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import random
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import pprint, time
from nltk.tokenize import word_tokenize

from collections import Counter

#Get some sample data (will update to get our own data later)
# reading the Treebank tagged sentences
nltk_data = list(nltk.corpus.treebank.tagged_sents(tagset='universal'))

nltk_data = nltk_data[0:5]

#USING OWN DATA
my_data = list()

# Using readlines() 
file1 = open('WORD CLASS 520.txt', 'r') 
Lines = file1.readlines() 
  
count = 0
# Strips the newline character 
my_sent = list()
for line in Lines: 
    to_add = tuple(line.replace("\n", "").replace(" ", "") .split("/"))
    #print(to_add)
    my_sent.append(to_add)
    if(to_add[0] == "."):
        my_data.append(my_sent)
        my_sent = list()
    
# Splitting into train and test
random.seed(1234)
# validation set is 5% of the total dataset
train_set,test_set = train_test_split(my_data,random_state = 123,test_size=0.1)

print("Training Sentences: " + str(len(train_set)))
print("Testing Sentences: " + str(len(test_set)))

#put all words together from the sentences
train_tagged_words = [tup for sent in train_set for tup in sent]
print("Tagged Training Tokens: " + str(len(train_tagged_words)))

#separate out words and tags
tokens = [pair[0] for pair in train_tagged_words]

#Make a vocabulary (turn into set, meaning all elements are unique)
V = set(tokens)
print("\nVocab Set Size: " + str(len(V)))

#Make a tag set
T = set([pair[1] for pair in train_tagged_words])
print("Tag Set Size:" + str(len(T)) + ", Set:" + str(T))

#Done reconfiguring, start Viterbi


        
# compute word given tag: Emission Probability
def word_given_tag(word, tag, train_bag):
    tag_list = [pair for pair in train_bag if pair[1]==tag]
    count_tag = len(tag_list)
    w_given_tag_list = [pair[0] for pair in tag_list if pair[0]==word]
    count_w_given_tag = len(w_given_tag_list)
    
    return (count_w_given_tag, count_tag)

# compute tag given tag: tag2(t2) given tag1 (t1), i.e. Transition Probability

def t2_given_t1(t2, t1, train_bag):
    tags = [pair[1] for pair in train_bag]
    count_t1 = len([t for t in tags if t==t1])
    count_t2_t1 = 0
    for index in range(len(tags)-1):
        if tags[index]==t1 and tags[index+1] == t2:
            count_t2_t1 += 1
    return (count_t2_t1, count_t1)


# Viterbi Heuristic
def Viterbi(words, train_bag):
    state = []
    T = list(set([pair[1] for pair in train_bag]))
    
    for key, word in enumerate(words):
        #initialise list of probability column for a given observation
        p = [] 
        for tag in T:
            if key == 0:
                transition_p = tags_df.loc['Z', tag]
            else:
                transition_p = tags_df.loc[state[-1], tag]
                
            # compute emission and state probabilities
            emission_p = word_given_tag(words[key], tag, train_tagged_words)[0]/word_given_tag(words[key], tag, train_tagged_words)[1]
            state_probability = emission_p * transition_p    
            p.append(state_probability)
            
        pmax = max(p)
        # getting state for which probability is maximum
        state_max = T[p.index(pmax)] 
        state.append(state_max)
    return list(zip(words, state))
#RULE BASED VERSION
def rule_based(words, state):
    
    # specify patterns for tagging
    # example from the NLTK book
    patterns = [
        (r'.*ing$', 'VB'),              # gerund
        (r'.*ed$', 'VB'),               # past tense
        (r'.*es$', 'VB'),               # 3rd singular present
        (r'.*ould$', 'AUX'),              # modals
        (r'.*\'s$', 'N'),              # possessive nouns
        (r'.*s$', 'N'),                # plural nouns
        (r'.*\*.*', 'N'),                # plural nouns 
        (r'.*', 'N')                    # nouns
    ]
    
    regexp_tagger = nltk.RegexpTagger(patterns)
    
    for i,j in enumerate(state):
        #Rule-based tagging done only for new 'unknown' words.
        if j == "unknown":
            state[i] = regexp_tagger.tag([words[i]])[0][1]
    return words,state

# Modified Viterbi Heuristic with Rule Based
def Viterbi_rule_based(words, train_bag):
    state = []
    T = list(set([pair[1] for pair in train_bag]))
    
    for key, word in enumerate(words):
        #initialise list of probability column for a given observation
        p = [] 
        for tag in T:
            if key == 0:
                transition_p = tags_df.loc['Z', tag]
            else: 
                #If previous tag is 'unknown' make transition_p = 1, so that emission_p alone decides the tag. 
                if (state[-1] == 'unknown'):
                    transition_p = 1
                else:             
                    transition_p = tags_df.loc[state[-1], tag]
                
           
            emission_p = word_given_tag(words[key], tag, train_bag)[0]/word_given_tag(words[key], tag, train_bag)[1]
            state_probability = emission_p * transition_p
            p.append(state_probability)   
        pmax = max(p)

        if pmax == 0:
            #if pmax = 0, means the the word is a new word, in such case mark the word tag as "unknown".
            state_max = "unknown"
        else:
            state_max = T[p.index(pmax)]
        state.append(state_max)
    
    word, state = rule_based(words, state) #Rule-based function called for all 'unknown' new words.
    return list(zip(words, state))
def measure_accuracy(predicted, real):
    check = [i for i, j in zip(predicted, real) if i == j] 
    accuracy = len(check)/len(predicted)
    return accuracy

def find_incorrect_tags(predicted, real):
    incorrect_tags = [[real[i-1],j] for i, j in enumerate(zip(predicted, real)) if j[0]!=j[1]]
    return incorrect_tags

# computing P(w/t) and storing in T x V matrix
t = len(T)
v = len(V)
w_given_t = np.zeros((t, v))

# creating t x t transition matrix of tags
# each column is t2, each row is t1
# thus M(i, j) represents P(tj given ti)
tags_matrix = np.zeros((len(T), len(T)), dtype='float32')
for i, t1 in enumerate(list(T)):
    for j, t2 in enumerate(list(T)): 
        tags_matrix[i, j] = t2_given_t1(t2, t1, train_tagged_words)[0]/t2_given_t1(t2, t1, train_tagged_words)[1]
tags_df = pd.DataFrame(tags_matrix, columns = list(T), index=list(T))

#NOW RUN IT
test_run_base = [tup for sent in test_set for tup in sent]
test_tagged_words = [tup[0] for sent in test_set for tup in sent]

# tagging the test sentences
start = time.time()
tagged_seq = Viterbi_rule_based(test_tagged_words, train_tagged_words)
end = time.time()
difference = end-start
print("\nTime taken in seconds: ", difference)

acc = measure_accuracy(tagged_seq,test_run_base)
print("Accuracy with  Viterbi \t\t{:0.2f} %".format(acc*100))

print("\nIncorrect Tags as: Previous Tag, Incorrect Tag, Correct Tag")
print(*find_incorrect_tags(tagged_seq, test_run_base), sep ="\n")
#print(tagged_seq)



