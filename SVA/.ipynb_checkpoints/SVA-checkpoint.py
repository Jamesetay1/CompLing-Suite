import stanza
#stanza.download('en')
nlp = stanza.Pipeline('en', processors = "tokenize, pos, lemma, depparse", batch_size = "100")

with open('testsentences.txt', 'r') as file:
    data = file.read()
print(data)

doc = nlp(data)

#https://stanfordnlp.github.io/stanza/depparse.html
fileString = ""
#for j, sentence in enumerate(doc.sentences):
    
doc.sentences[0].print_dependencies()