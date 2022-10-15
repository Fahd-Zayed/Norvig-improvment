# The problem is that In original Norvig model:
# 1)only one word can be corrected at a time 
# 2)only one suggestion/word appear
#   so..
# I made a modified model that can detect and correct more than one word at the same time,
# and for each word there will be more than one suggestion based on probapilities


import re
from collections import Counter


def Get_Words(corpus: str):  # Create a list of words from the dataset
    Dataset = set(re.findall(r'\w+', corpus.lower()))
    return Dataset  # done


def Calculate_probabilities(
        corpus: str):  # create a probabilities dictionary that contains the probability of each word
    counter = Counter(re.findall(r'\w+', corpus.lower()))
    total = sum(counter.values())
    probabilities = {w: (count / total) for w, count in counter.items()}
    return probabilities


# not edited
def edits1(word):
    "All edits that are one edit away from `word`."
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)


def edits2(word):
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))


def correct_These_Sentence(Complete_sentence: str):  # not completed
    def Correct_words(wrong_word, Dataset, probabilities_dictionary, n=2):  # bool default false but can be true
        recommendations_List = []
        Top_Matching = []

        if wrong_word in Dataset:
            return wrong_word  # it is already correct

        recommendations_List = list(
            edits1(wrong_word).intersection(Dataset) or edits2(wrong_word).intersection(Dataset))  # suggestion List
        Top_Matching = [(word, probabilities[word]) for word in list(reversed(recommendations_List))]  # Best match
        # put all words in the recomendation list with their probabilities to sort them and return the best 2 words

        print("suggestions = ", recommendations_List)

        # print("Best 2 choices before sort : ",Top_Matching[:n])#display the probability of the bset n(2)
        Top_Matching.sort(key=lambda x: x[1], reverse=True)  # sort by greatest probapility
        print("Best 2 choices: ", Top_Matching[:n])  # display the probability of the bset n(2)
        return Top_Matching[:n]

    # start
    with open('big.txt') as file:
        dataset = file.read()

    Dataset = Get_Words(dataset)  # build list of words
    print("Vocab List: ", Dataset)  # Print list of words

    probabilities = Calculate_probabilities(dataset)  # build probs
    print("probability List: ", probabilities)  # print probs
    print("")

    words_in_sentence = Complete_sentence.split(' ')  # split the sentence that we input to check by space
    print("list of words in sentence ", words_in_sentence)  # print the List that carry each word in the input sentence

    Need_Correction = [w for w in words_in_sentence if w.lower() not in Dataset]  # list of wrong words
    print("List of words that need to be corrected", Need_Correction)
    print("")

    After_correction = [Correct_words(wrong_word, Dataset, probabilities)[0][0] for wrong_word in
                        Need_Correction]  # take the first word from top matching list
    print("List of words After correction ", After_correction)  # list of corrected words
    # return vocab #will be changed


# correct_These_Sentence("wng wrd word")
print("---------------------------------------------------------------------------------------------")
correct_These_Sentence("welome to the new mdel")
print("---------------------------------------------------------------------------------------------")
# correct_These_Sentence("all is correct")
print("---------------------------------------------------------------------------------------------")




