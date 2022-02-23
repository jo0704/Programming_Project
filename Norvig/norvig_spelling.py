#! /usr/bin/python3
# -*- coding: utf-8 -*-
#Author: Joëlle Gasser
#Norvig Spelling Corrector Historical English to Normalized English

import re
from collections import Counter
from sklearn.metrics import accuracy_score, precision_score, recall_score

dev = open('dev.txt', 'r', encoding='utf8')
test = open('test.txt', 'r', encoding='utf8')
icamet_dev= open('icamet_en-hs_dev_hsen.txt', 'r', encoding='utf8')
icamet_test = open('icamet_en-hs_test_hsen.txt', 'r', encoding='utf8')
output = open('evaluation_results.txt', 'w', encoding = 'utf8')
output_common = open('results_common.txt', 'w', encoding = 'utf8')

def lower_text(text): 
    """
    returns the text tokenized into words
    and as lower case characters in a list
    """
    return re.findall(r'\w+', text.lower())

#dict counting the number of each word in the text file
tokenized_words = Counter(lower_text(open('bncwwri_untag.txt').read()))
#threshold for known words to appear at least x times
known_words = Counter({k: c for k, c in tokenized_words.items() if c >=19})

#print(tokenized_words)
#print(known_words)
#print(len(tokenized_words)) 
#print(sum(tokenized_words.values()))
#print(tokenized_words.most_common(10)) 

def P(word, N=sum(known_words.values())): 
    "Probability of `word`."
    return known_words[word] / N

def correction(word): 
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def edits1(word):
    "All edits that are one edit away from `word`"
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

def known(words): 
    "The subset of `words` that appear in the dictionary of words"
    return set(w for w in words if w in known_words)

def unit_tests():
    assert correction('dresed') == 'dressed'                # insert
    assert correction('korrectud') == 'corrected'           # replace 2
    assert correction('hauing') == 'having'                 # replace
    assert correction('smoothe') == 'smooth'                # delete
    assert correction('peotry') =='poetry'                  # transpose
    assert correction('peotryy') =='poetry'                 # transpose + delete
    assert correction('word') == 'word'                     # known
    assert correction('quintessential') == 'quintessential' # unknown
    assert lower_text('This is a TEST.') == ['this', 'is', 'a', 'test']
    assert Counter(lower_text('This is a test. 123; A TEST this is.')) == (
           Counter({'123': 1, 'a': 2, 'is': 2, 'test': 2, 'this': 2}))
    assert len(tokenized_words) == 376715
    assert sum(tokenized_words.values()) == 89376867
    assert known_words.most_common(10) == [
     ('the', 5647035),
     ('of', 2877671),
     ('to', 2371089),
     ('and', 2365752),
     ('a', 1977507),
     ('in', 1814307),
     ('that', 893692),
     ('is', 887134),
     ('for', 814558),
     ('it', 802975)]
    assert known_words['the'] == 5647035
    assert 0.06 < P('the') < 0.07
    return 'unit_tests pass'
# print(unit_tests())

def spelltest(tests):
    "Run correction(hist) on all (normalized, hist) pairs"
    #good, unknown = 0, 0
    predicted = []
    norm = []  
    #n = len(tests)
    for normalized, hist in tests:
        #w = correction(hist)
        norm.append(normalized)
        predicted.append(correction(hist))
        # good += (w == normalized)
        # if w != normalized:
        #     unknown += (normalized not in known_words)
    # with open('results_norvig.txt', 'w') as f:
    #     f.write('Accuracy: {:.0%} of {} correct ({:.0%} unknown) '
    #       .format(good / n, n, unknown / n, n))
    return norm, predicted

def Testset(lines):
    "ARCHER: Parse 'normalized: hist1 hist2' lines into [('normalized', 'hist1'), ('normalized', 'hist2')] pairs."
    return [(normalized, hist)
            for (normalized, hists) in (line.split(':') for line in lines)
            for hist in hists.split()]

def Testset2(lines):
    "ICAMET:Parse 'normalized: hist1 hist2' lines into [('normalized', 'hist1'), ('normalized', 'hist2')] pairs."
    return [(normalized, hist)
            for (normalized, hists) in (line.split('\t') for line in lines)
            for hist in hists.split()]


def common_el(list_norm, list_hist):
    "common elements in normalized/historical English lists"
    return [el for el in list_norm if el in list_hist]

def main():

    #save lists for calculating accuracy, recall and precision, and for calculating similar words between the lists
    normalized_dev, predicted_dev = spelltest(Testset(dev))
    normalized_test, predicted_test = spelltest(Testset(test))
    icamet_normalized_dev, icamet_predicted_dev = spelltest(Testset2(icamet_dev))
    icamet_normalized_test, icamet_predicted_test = spelltest(Testset2(icamet_test))

    set_normalized_dev = set(normalized_dev)
    set_predicted_dev = set(predicted_dev)
    common_dev = common_el(set_normalized_dev, set_predicted_dev)
    common_dev_perc = (len(set(set_predicted_dev).intersection(set(set_normalized_dev))))/len(set_predicted_dev) 

    set_normalized_test = set(normalized_test)
    set_predicted_test = set(predicted_test)
    common_test = common_el(set_normalized_test, set_predicted_test)
    common_test_perc = (len(set(set_predicted_test).intersection(set(set_normalized_test))))/len(set_predicted_test) 

    set_icamet_normalized_dev = set(icamet_normalized_dev)
    set_icamet_predicted_dev = set(icamet_predicted_dev)
    icamet_common_dev = common_el(set_icamet_normalized_dev, set_icamet_predicted_dev)
    icamet_common_dev_perc = (len(set(set_icamet_predicted_dev).intersection(set(set_icamet_normalized_dev))))/len(set_icamet_predicted_dev) 

    set_icamet_normalized_test = set(icamet_normalized_test)
    set_icamet_predicted_test = set(icamet_predicted_test)
    icamet_common_test = common_el(set_icamet_normalized_test, set_icamet_predicted_test)
    icamet_common_test_perc = (len(set(set_icamet_predicted_test).intersection(set(set_icamet_normalized_test))))/len(set_icamet_predicted_test) 
    
    #Historical English words that are spelled like today
    output_common.write("What are the historical English words that are spelled like today?" + '\n' + "ARCHER" + '\n' + "DEV SET" + '\n' + '-------------------------------------' +'\n')
    for el in common_dev:
        output_common.write(el +'\n')
    output_common.write('-------------------------------------' +'\n' + "TEST SET" + '\n' + '-------------------------------------' +'\n')
    for el in common_test:
        output_common.write(el +'\n')
    output_common.write('-------------------------------------' +'\n' + "ICAMET" + '\n' + "DEV SET" + '\n' + '-------------------------------------' +'\n')
    for el in icamet_common_dev:
        output_common.write(el +'\n')
    output_common.write('-------------------------------------' +'\n' + "TEST SET" + '\n' + '-------------------------------------' +'\n')
    for el in icamet_common_test:
        output_common.write(el +'\n')
    
    output_common.close()

    #calculate evaluation metrics with sklearn
    #archer
    recall_dev = recall_score(normalized_dev, predicted_dev, average="micro")
    precision_dev = precision_score(normalized_dev, predicted_dev, average="micro")
    accuracy_dev = accuracy_score(normalized_dev, predicted_dev) 
    recall_test = recall_score(normalized_test, predicted_test, average="micro") 
    precision_test = precision_score(normalized_test, predicted_test, average="micro") 
    accuracy_test = accuracy_score(normalized_test, predicted_test) 
    #icamet
    icamet_recall_dev = recall_score(icamet_normalized_dev, icamet_predicted_dev, average="micro")
    icamet_precision_dev = precision_score(icamet_normalized_dev, icamet_predicted_dev, average="micro")
    icamet_accuracy_dev = accuracy_score(icamet_normalized_dev, icamet_predicted_dev) 
    icamet_recall_test = recall_score(icamet_normalized_test, icamet_predicted_test, average="micro") 
    icamet_precision_test = precision_score(icamet_normalized_test, icamet_predicted_test, average="micro") 
    icamet_accuracy_test = accuracy_score(icamet_normalized_test, icamet_predicted_test) 

    #write evaluation metrics in output file
    output.write("ARCHER" + '\n' + '-------------------------------------' +'\n')
    output.write("Recall dev:" + '\t' + '{:.2%}'.format(recall_dev) + '\n')
    output.write("Precision dev:" + '\t' + '{:.2%}'.format(precision_dev) + '\n')
    output.write("Accuracy dev:"  + '\t'+ '{:.2%}'.format(accuracy_dev) +'\n' + '-------------------------------------' + '\n')
    output.write("Recall test:" + '\t' + '{:.2%}'.format(recall_test) + '\n')
    output.write("Precision test:" + '\t' + '{:.2%}'.format(precision_test) + '\n')
    output.write("Accuracy test:" + '\t' + '{:.2%}'.format(accuracy_test) +'\n' + '-------------------------------------' +'\n')
    output.write("How many historical English words are spelled like today?" + '\n')
    output.write("DEV SET" + '\t' + '{:.2%}'.format(common_dev_perc) + '\n')
    output.write("TEST SET" + '\t' + '{:.2%}'.format(common_test_perc) + '\n' + '-------------------------------------' +'\n')
    
    output.write("ICAMET" + '\n' + '-------------------------------------' +'\n')
    output.write("Recall dev:" + '\t' + '{:.2%}'.format(icamet_recall_dev) + '\n')
    output.write("Precision dev:" + '\t' + '{:.2%}'.format(icamet_precision_dev) + '\n')
    output.write("Accuracy dev:"  + '\t'+ '{:.2%}'.format(icamet_accuracy_dev) +'\n' + '-------------------------------------' + '\n')
    output.write("Recall test:" + '\t' + '{:.2%}'.format(icamet_recall_test) + '\n')
    output.write("Precision test:" + '\t' + '{:.2%}'.format(icamet_precision_test) + '\n')
    output.write("Accuracy test:" + '\t' + '{:.2%}'.format(icamet_accuracy_test) +'\n' + '-------------------------------------' +'\n')
    output.write("How many historical English words are spelled like today?" + '\n')
    output.write("DEV SET" + '\t' + '{:.2%}'.format(icamet_common_dev_perc) + '\n')
    output.write("TEST SET" + '\t' + '{:.2%}'.format(icamet_common_test_perc) + '\n' + '-------------------------------------' +'\n')

    output.close()


if __name__ == '__main__':
	main()
