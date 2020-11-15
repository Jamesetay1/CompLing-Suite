import stanza
#stanza.download('en')
nlp = stanza.Pipeline('en', processors = "tokenize, pos, lemma, depparse", batch_size = "100")

with open('testsentences.txt', 'r') as file:
    data = file.read()
doc = nlp(data)

nsubj_Agreement_dict = {
                "VB": [],
                "VBD": ["NN", "NNS", "NNP", "NNPS", "PRP_1", "PRP_2", "DT_1", "DT_2"],
                "VBG": ["NN", "NNS", "NNP", "NNPS", "PRP_1", "PRP_2", "DT_1", "DT_2"],
                "VBN": ["NN", "NNS", "NNP", "NNPS", "PRP_1", "PRP_2", "DT_1", "DT_2"],
                "VBZ": ["NN", "NNP", "PRP_2", "DT_1"],
                "VBP": ["NNS", "NNPS", "PRP_1", "DT_2"],
}

grouping_dict = {
                "PRP_1": ["i", "you", "they", "we", "she", "it", "his", "hers", "theirs"],
                "PRP_2": ["he", "she"],
                "DT_1": ["this", "that"],
                "DT_2": ["these", "those"],
}
def error(dep, gov):
    print(dep.text + "," + gov.text)
    if dep.xpos in nsubj_Agreement_dict[gov.xpos]:
        return False;

    for key in grouping_dict:
        if dep.text.lower() in grouping_dict[key] and key in nsubj_Agreement_dict[gov.xpos]:
            return False;

    return True;

# ACCEPTABLE COMBINATIONS HERE
correct = []
incorrect = []
compounds = []
for sent in doc.sentences:
    for word in sent.words:
        dep = word
        dep_pos = word.xpos

        gov = sent.words[word.head - 1]
        gov_pos = gov.xpos

        if word.deprel == "nsubj":
            if gov_pos not in nsubj_Agreement_dict:
                continue

            if error(dep, gov):
                incorrect.append(word.text + "(" + word.xpos + ") " + "<--nsubj--- " + sent.words[word.head-1].text + "(" + gov_pos + ")")
            else:
                correct.append(word.text + "(" + word.xpos + ") " + "<--nsubj--- " + sent.words[word.head-1].text + "(" + gov_pos + ")")

        if word.deprel == "compound":
            if gov_pos == dep_pos:
                compounds.append(word.text + "(" + word.xpos + ") " + "<--compound--- " + sent.words[word.head-1].text + "(" + gov_pos + ")")



total_num = len(correct) + len(incorrect)
correct_percent = len(correct)/total_num * 100
incorrect_percent = len(incorrect)/total_num * 100
print("\nGeneral Statistics:")
print("# of nsubj dependencies considered: " + str(total_num))
print("# and percent of correct uses: " + str(len(correct)) + ", " + str(correct_percent))
print("# and percent of correct uses: " + str(len(incorrect)) + ", " + str(incorrect_percent))

print("\nThe following nsubj dependencies were found to be incorrect:")
print(*incorrect,sep='\n')

print("\nThe following nsubj dependencies were found to be correct:")
print(*correct,sep='\n')

print("\nThe following compound nouns were found and could actually be subject verb agreement errors:")
print(*compounds,sep='\n')