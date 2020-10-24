import re
import sys

V = '[aeiouY]+'
C = '[^aeiouY]+'
#This function replaces all vowels and consonants with V's and C's. It is not elegant to have changed the vowels first to o's, but it works.
def change_to_VCs(word):
    changed_to_VCs = word
    changed_to_VCs = re.sub(V, "o", changed_to_VCs)
    changed_to_VCs = re.sub(C, "C", changed_to_VCs)
    changed_to_VCs = re.sub(r'o', "V", changed_to_VCs)
    return changed_to_VCs


#This function calculates the "m" value, which is the number of times V+C+ repeats in a string.
#This "m" value roughly equates to the number of syllables in a word.
#The reason this is a function is because the paper indicates that the VC needs to be calculated
#AFTER the suffix is removed.
def count_VCs(word, suffix):
    word = re.sub(suffix + r'\b', '', word)
    word = change_to_VCs(word)
    num_of_VCs = re.findall(r'VC', word)
    return len(num_of_VCs)


#This is the function which determines if the stem ends in CVC, where the second C is not w, x or y
#The paper was ambiguous about whether this meant a literal 3-string CVC, or C+V+C+
#This function finds C+V+C+
def ends_cvc(word):
    VC_word = word
    VC_word = change_to_VCs(VC_word)
    if re.search(r'CVC\b', VC_word) is not None:
        if re.search(r'[^wxy]\b', word) is not None:
            return True
    else:
        return False

# This is the main function of the program. The original word (which may have gone through some modifications)
# is called "stem". "suffix1" is the suffix to remove, "suffix2" is the suffix to add, "mincount_VCs" is the minimum
# "m" value.
def do_to_suffix(stem, suffix1, suffix2, mincount_VCs):
    stem_length = count_VCs(stem, suffix1)
    if stem_length >= mincount_VCs:
        if re.search(r'\w' + suffix1 + r'\b', stem) is not None:
            stem = re.sub(suffix1 + r'\b', suffix2, stem)
            return(stem, True)
    return(stem, False)

def step1(stem):
    #step 1a
    #sses -> ss
    if re.search(r'sses\b', stem) is not None:
        stem = re.sub(r'sses\b', 'ss', stem)
    #ies -> i
    elif re.search(r'ies\b', stem) is not None:
        stem = re.sub(r'ies\b', 'i', stem)
    #ss -> ss
    elif re.search(r'ss\b', stem) is not None:
        pass
    #s ->
    elif re.search(r's\b', stem) is not None:
        stem = re.sub(r's\b', '', stem)
    
    step1_2=False #Safter to set these to false ahead of setting them to True
    step1_3=False
    #step 1b
    #(m>0) eed -> ee
    stem, did_replace_suffix = do_to_suffix(stem, "eed", "ee", 1)
    if not did_replace_suffix:
        # (*v*) ed ->
        stem, did_replace_suffix = do_to_suffix(stem, "ed", "", 0)
        step1_2 = True
        if not did_replace_suffix:
            # (*v*) ing ->
            stem, did_replace_suffix = do_to_suffix(stem, "ing", "", 0)
            step1_3 = True

    step1_2_3_suffixes = [("at", "ate"), ("bl", "ble"), ("iz", "ize")]
    if step1_2 or step1_3:
        for suffix_pair in step1_2_3_suffixes:
            # at -> ate
            # bl -> ble
            # iz -> ize
            # (*d and not (*L or *S or *Z) -> single letter
            stem, did_replace_suffix = do_to_suffix(stem, suffix_pair[0], suffix_pair[1], 1)
            if did_replace_suffix:
                break
        if len(stem)>1 and stem[-1] == stem[-2] and re.search(r'[^aeiouYlsz]', stem[-1]) is not None:
            stem = stem[:-1]
        if count_VCs(stem, '') == 1 and ends_cvc(stem):
            # (m=1 and *o) -> e
            stem = stem + 'e'

    #step 1c
    #(*v*) y-> i
    #I set this to 1 because of the example "sky". The paper did not explicitly say to do this.
    stem, did_replace_suffix = do_to_suffix(stem, "Y", "i", 1) 
    return stem

def step2(stem):
    #step 2
    #see examples in paper
    step_2_suffixes = [("ational", "ate"), ("tional", "tion"), ("enci", "ence"), ("anci", "ance"), ("izer", "ize"),
                       ("abli", "able"), ("alli", "al"), ("entli", "ent"), ("eli", "e"), ("ousli", "ous"), ("ization", "ize"),
                       ("ation", "ate"), ("ator", "ate"), ("ator", "ate"), ("alism", "al"), ("iveness", "ive"), ("fulness", "ful"),
                       ("ousness", "ous"), ("aliti", "al"), ("iviti", "ive"), ("biliti", "ble")]
    for suffix_pair in step_2_suffixes:
        stem, did_replace_suffix = do_to_suffix(stem, suffix_pair[0], suffix_pair[1], 1)
        if did_replace_suffix:
            break
            
    return stem

def step3(stem):
    #step 3
    # see examples in paper
    step_3_suffixes = [("icate", "ic"), ("ative", ""), ("alize", "al"), ("iciti", "ic"), ("ical", "ic"), ("ful", ""), ("ness", "")]
    for suffix_pair in step_3_suffixes:
        stem, did_replace_suffix = do_to_suffix(stem, suffix_pair[0], suffix_pair[1], 1)
        if did_replace_suffix:
            break
    return stem

def step4(stem):
    #step 4
    # see examples in paper
    step_4_suffixes = ["al", "ance", "ence", "er", "ic", "able", "ible", "ant", "ement", "ment", "ent", "sion", "tion", "ou", "ism", "ate", "iti", "ous", "ive", "ize"]
    for suffix in step_4_suffixes:
        stem, did_replace_suffix = do_to_suffix(stem, suffix, "", 2)
        if did_replace_suffix:
            break
        else:
            continue
            
    return stem

def step5(stem):
    #step 5a
    # (m>1) e ->
    stem, did_replace_suffix = do_to_suffix(stem, "e", "", 2)
    if not did_replace_suffix and count_VCs(stem, 'e') == 1 and not ends_cvc(stem) and stem[-1] == "e":
        #(m=1 and not *o) e ->
        stem = stem[:-1]
    # rate -> rat is changed here. I think it's supposed to do this. The paper is quite confusing about this.

    #step 5b
    #(m > 1 and *d and *L) -> single letter
    if count_VCs(stem, '') > 1:
        if stem[-2:] == 'll':
            stem = stem[:-1]
            
    return stem
def print_results(test_name, original, expected, results):
    print("\n***********************\nUnit Test Results for " + test_name + "\n***********************")
    for i in range(len(original)):
        success_string = "PASSED" if expected[i]==results[i] else "#### FAILED ####"
        print("Original: " + original[i] + ", Expected: " + expected[i] + ", Results: " + results[i] + ". " + success_string)
    
def run_tests():
    step1_original = ["caresses", "ponies", "ties", "caress", "cats", "feed", "agreed", "plastered", "bled", "motoring", "sing",
                      "conflated" , "troubled", "sized", "hopping", "tanned", "falling", "hissing", "fizzed", "failing", "filing",
                      "happy", "sky"]
    step1_expected = ["caress", "poni", "ti", "caress", "cat", "feed", "agree", "plaster", "bled", "motor", "sing",
                   "conflate", "trouble", "size", "hop", "tan", "fall", "hiss", "fizz", "fail", "file",
                   "happi", "sky"]
    step1_results = list(map(step1, step1_original))
    print_results("Step 1", step1_original, step1_expected, step1_results)
    
    step2_original = ["relational", "conditional", "rational", "valenci", "hesitanci", "digitizer", "conformabli", "radicalli", 
                      "differentli", "vileli", "analogousli", "vietnamization", "predication", "operator", "feudalism", "decisiveness",
                     "hopefulness", "callousness", "formaliti", "sensitiviti", "sensibiliti"]
    step2_expected = ["relate", "condition", "rational", "valence", "hesitance", "digitize", "conformable", "radical", "different", "vile",
                     "analogous", "vietnamize", "predicate", "operate", "feudal", "decisive", "hopeful", "callous", "formal", "sensitive",
                     "sensible"]
    step2_results = list(map(step2, step2_original))
    print_results("Step 2", step2_original, step2_expected, step2_results)
    
    step3_original = ["triplicate", "formative", "formalize", "electriciti", "electrical", "hopeful", "goodness"]
    step3_expected = ["triplic", "form", "formal", "electric", "electric", "hope", "good"]
    step3_results = list(map(step3, step3_original))
    print_results("Step 3", step3_original, step3_expected, step3_results)
    
    step4_original = ["revival", "allowance", "inference", "airliner", "gyroscopic", "adjustable", "defensible", "irritant", "replacement", 
                      "adjustment", "dependent", "adoption", "homologou", "communism", "activate", "angulariti", "homologous", "effective", "bowdlerize"]             
    step4_expected = ["reviv", "allow", "infer", "airlin", "gyroscop", "adjust", "defens", "irrit", "replac", "adjust", "depend", "adopt", "homolog",
                      "commun", "activ", "angular", "homolog", "effect", "bowdler"]
    step4_results = list(map(step4, step4_original))
    print_results("Step 4", step4_original, step4_expected, step4_results)
    
    step5_original = ["probate", "rate", "cease", "controll", "roll"]
    step5_expected = ["probat", "rate", "ceas", "control", "roll"]
    step5_results = list(map(step5, step5_original))
    print_results("Step 5", step5_original, step5_expected, step5_results)
    
    #Once all tests are done, will print out
    
def stem(original_word):
    # vowel is Y, consonant is y. At the end, everything reverts to lowercase.
    stem = re.sub(r'([^aeiou])y', r"\1Y", original_word)
    stem = step1(stem)
    stem = step2(stem)
    stem = step3(stem)
    stem = step4(stem)
    stem = step5(stem)
    
    return stem

original_word = input("Give me a word.\nOr type \"%test\" to run tests.\n")
original_word = original_word.lower()

if(original_word=="%test"):
    run_tests()
    sys.exit()
    
stem = stem(original_word)
print("Original: " + original_word.lower())
print("Stemmed: " + stem.lower()) #I solved "gyroscopic" by putting this all to lowercase (i.e. undoing my notation)