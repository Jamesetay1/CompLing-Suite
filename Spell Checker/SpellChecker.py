import LD

#word1 = "Python"
#word2 = "Peithen"
#print("MED between " + word1 + " and " + word2 + " is: " + str(LD.LD_Iter(word1, word2, 1, 1, 1)))
#print("MED between " + word1 + " and " + word2 + " is: " + str(LD.LD_Recursive(word1, word2)))


from nltk.corpus import words
from nltk.corpus import brown
from nltk import FreqDist

sentence = "I ama noto maad"
words = sentence.split()

frequency_list = FreqDist(i.lower() for i in brown.words())
k_dict_freq = frequency_list.most_common()[:1000]
k_dict = [i[0] for i in k_dict_freq]
#print(k_dict)

corrected = []
for w in words:
    if w.lower() not in k_dict:
        lowestLD = 1000
        for k in k_dict:
            curLD = LD.LD_Iter(w.lower(), k, 1, 1, 1)
            if(curLD < lowestLD):
                lowestLD = curLD 
                correct_word = k
                print(w+ ":" + correct_word + str(lowestLD))
        corrected.append(correct_word)
    else:
        corrected.append(w)
            
print(corrected)