#Author: Joëlle Gasser
#python script to extract xml tags in Archer Corpus
#and store pairs of Historical / Normalized English translations in a file
import xml.etree.ElementTree as ET
import os
from os import listdir, path
import collections

#path where xml files are stored
mypath = os.chdir("./ARCHER1600_1700")

lst_orig = []
lst_normalised = []
lst_pairs = []

for file in os.listdir():
    #read all xml files
    if file.endswith(".xml"):
        root_node = ET.parse(file).getroot()
        #print(root_node)
        
        for tag in root_node.findall('body/normalised'):
            orig = tag.attrib['orig'] #extract historical English word
            orig = orig.lower()
            normalised = tag.text #extract its normalisation
            normalised = normalised.lower() 
            lst_orig.append(orig)
            lst_normalised.append(normalised)   
"""
with open('1600_1700.txt', 'w') as f:
    for el in range(len(lst_normalised)):
        f.write(lst_normalised[el] + ": " +lst_orig[el] + '\n')
"""
#create list with all pairs of normalised and Historical English words
for el in range(len(lst_normalised)):
    lst_pairs.append((lst_normalised[el], lst_orig[el]))
#print(lst_pairs)

#create dict with all Historical English words for one normalised word
dict_norm_origs = collections.defaultdict(list)
for k, v in lst_pairs:
    dict_norm_origs[k].append(v)
#print(sorted(dict_norm_origs.items()))
#print(len(dict_norm_origs.keys()))

#delete Historical English duplicates in dict_norm_orig.values()
dict_final = {}
for k, v in dict_norm_origs.items():
    uniq=set(v)
    uniq_v= list(uniq)
    dict_final[k] = uniq_v
    #print(uniq)
    #print(uniq_v)
#print(len(uniq_v))
#print(dict_final.items())
#print(len(dict_final.values()))
    #print(len(list(uniq)))

#write output file 
with open('1600_1700_2.txt', 'w') as f:
    for k,v in dict_final.items():
        f.write('{}: '.format(k))
        for i in v:
            f.write('{} '.format(i))
        f.write('\n')
          



  