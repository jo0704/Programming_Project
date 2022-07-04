#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Program to evaluate MT systems: computes the BLEU score of a translated text

import nltk
import re

reference_lines= open("test.trg.raw").readlines()
hypothesis_lines = open("test.post").readlines()

def tokenizer(tokens):
    '''finds all tokens and returns list of tokens'''
    pattern = r'(?x)\w+(?:-\w+)*|(?:[A-Z]\.)'
    tokens_list = nltk.regexp_tokenize(str(tokens), pattern)
    print(tokens_list)
    return tokens_list
    
def ngram_precision(hypothesis_lines, reference_lines):
    '''
    compute ngram precision for any ngram order
    return ngram precision
    '''
    #initialize variables
    correct_ngrams=0
    all_ngrams=0
    for hypothesis_line,reference_line in zip(hypothesis_lines,reference_lines):
        #print("hyp: " ,hypothesis_line)
        #print("ref: " ,reference_line)
        if hypothesis_line==reference_line:
            correct_ngrams+=1
        all_ngrams+=1
    
    
    print(all_ngrams)
    print(correct_ngrams)

    #calculate ngram precision of order 1 with clipping
    precision_unigram = correct_ngrams/all_ngrams
    print('precision for unigrams: ', precision_unigram)
    

def main():

    texts = [hypothesis_lines, reference_lines]

    #tokenize the texts
    tokens_list_hyp =tokenizer(texts[0])
    tokens_list_ref =tokenizer(texts[1])

    #print("hyp: " ,tokens_list_hyp)
    #print("ref: " ,tokens_list_ref)
    #calculate ngram precision
    precision = ngram_precision(tokens_list_hyp, tokens_list_ref)
  
if __name__ == '__main__':   
        main()

