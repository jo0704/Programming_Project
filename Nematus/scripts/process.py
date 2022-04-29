#!/bin/sh
#author: Joëlle Gasser
#process files one word per line, whitespaces marking end of sentences
#outputs sentences line by line

#change infile and outfile with desired files
infile = open ('seq2seq/icamet-datasets/icamet.en-hs.train.hs', 'r', encoding = 'utf8')
outfile = open('seq2seq/icamet-datasets/train.src.raw', 'w', encoding = 'utf8')
sentence = []
lines = infile.readlines()

for line in lines:
    line = line.strip('\n')
    # at empty lines we can write previous tokens to the output file as a sentence
    if line == '': 
        print(k)
        outfile.write(f'{" ".join(sentence)}\n')
        sentence = []     
    else:
        sentence.append(line)

    lines = infile.readlines()


infile.close()
outfile.close()
