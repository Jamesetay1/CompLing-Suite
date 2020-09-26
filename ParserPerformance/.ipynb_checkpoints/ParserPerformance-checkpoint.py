import numpy as np
import re

file1 = open("James_DrSuess.txt","r+") #GOLD STANDARD
file2 = open("Program_Parsed_DrSuess.txt","r+")

file1str = file1.read()
file2str = file2.read()

def parse_to_vector(filexstr):
    wordList = re.findall("\s?\S*\s?", filexstr)[:-1]
    wordcount = len(wordList)

    vector = np.zeros(wordcount, dtype=int)
    for i in range(len(vector)):
        if '|' in wordList[i]:
            vector[i]=1
        
    #print(vector)
    return(vector)

#Get vectors and combine 2 vectors into matrix
gold_standard = parse_to_vector(file1str)
vector = parse_to_vector(file2str)

true_positive = 0
true_negative = 0
false_positive = 0
false_negative = 0

for i in range(len(gold_standard)):
    if(gold_standard[i]==1 and vector[i]==1):
        true_positive+=1
    if(gold_standard[i]==0 and vector[i]==0):
        true_negative+=1
    if(gold_standard[i]==0 and vector[i]==1):
        false_positive+=1
    if(gold_standard[i]==1 and vector[i]==0):
        false_negative+=1


print("True positives:" + str(true_positive))
print("True negative:" + str(true_negative))
print("False positives:" + str(false_positive))
print("False negatives:" + str(false_negative) + "\n")

precision = true_positive/(true_positive + false_positive)
recall = true_positive/(true_positive + false_negative)
F1 = 2 * ((precision * recall)/(precision + recall))
accuracy = (true_positive + true_negative) / len(gold_standard)

print("precision:" + str(precision))
print("recall: " + str(recall))
print("F1 score: " + str(F1))
print("accuracy:" + str(accuracy))
