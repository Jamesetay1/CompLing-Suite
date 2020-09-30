def m(root):
    root = root.lower()
    vowels = "aeiou" #consider y a consonant, handle in first if statement of for loop
    m=0
    #looking for cases of VC or yC
    for c in range(len(root)-1):
        if root[c] == 'y' and root[c+1] not in vowels:
            m+=1
        if root[c] in vowels and root[c+1] not in vowels:
            m+=1
        
    return m 

def step1(word):
    
    return word

def step2(word):
    old_suffix_list = ["ational", "tional", "enci", "anci", "izer", "abli", "alli", "entli", "eli",
                       "ousli", "ization", "ation", "ator", "alism", "iveness", "fulness", "ousness",
                       "aliti", "iviti", "biliti"]
    new_suffix_list = ["ate", "tion", "ence", "ance", "ize", "able", "al", "ent", "e", 
                       "ous", "ize", "ate", "ate", "al", "ive", "ful", "ous", 
                       "al", "ive", "ble"]
    
    #Find all matching suffixes
    matching_suffixes = []
    for i in range(len(old_suffix_list)):
        if word.endswith(old_suffix_list[i]):
            matching_suffixes.append(old_suffix_list[i])
            
    print(matching_suffixes)
    longest_suffix = max(matching_suffixes, key=len)
    suffix_len = len(longest_suffix)
    root = word[:-suffix_len]
    if(m(root)>0):
        root += new_suffix_list[old_suffix_list.index(longest_suffix)]
        
    return root
#STEP 2 TESTS:
print(step2("relational"))

def step3(word):
    
    return word

def step4(word):
    
    return word

def step5(word):
    
    return word

def stem_word(word):
    word = step1(word)
    word = step2(word)
    word = step3(word)
    word = step4(word)
    word = step5(word)
    return word

