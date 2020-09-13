import re
import numpy as np

#Import 3 files
file1 = open("textfiles/James_DrSuess.txt","r+")
file2 = open("textfiles/Sondoss_SentToken_DrSuess.txt","r+")
file3 = open("textfiles/Laura_DrSuess.txt","r+")

file1str = file1.read()
file2str = file2.read()
file3str = file3.read()

#Create Function to create matrix from string
def parse_to_vector(filexstr):
    wordList = re.findall("\s?\S*\s?", filexstr)[:-1]
    wordcount = len(wordList)

    vector = np.zeros(wordcount, dtype=int)
    for i in range(len(vector)):
        if '|' in wordList[i]:
            vector[i]=1

    return(vector)

#Get vectors and combine 3 vectors into matrix
vector1 = parse_to_vector(file1str)
vector2 = parse_to_vector(file2str)
vector3 = parse_to_vector(file3str)

matrix = np.stack((vector1, vector2, vector3), axis = 0)
print(matrix)

#Run Krippendorfs Alpha on matrix
import krippendorff
ka_value = krippendorff.alpha(matrix)
print(ka_value)
