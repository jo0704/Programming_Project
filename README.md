# Programming Project: Spelling normalisation of historical English to English
Comparing 3 different approaches to normalize Historical English words from ARCHER Corpus (1600-1700)

## 1. Norvig Spelling Corrector: edit distance approach

**Data:** xml files from the ARCHER corpus for years 1600-1700: \
https://drive.switch.ch/index.php/s/DdWK9EtCxQkePuo (public access) \
The files mentioned below are stored in the folder **Norvig** 

To read the xml files, run:
```python3 xml_parser.py``` 

It outputs the text file ```1600_1700_2.txt``` in the following format: \
Normalised English word (translation): one or multiple Historical English words \
To get dev and test set, run the following UNIX commands to separate the output file into 2: \
```head -n 2975 1600_1700_2.txt > dev.txt``` \
```tail -n +2976 1600_1700_2.txt > test.txt``` 

Code from: https://norvig.com/spell-correct.html \
Language model for Norvig Spelling Corrector script : \
British National Corpus (BNC) https://www.swisstransfer.com/d/0b954f85-1805-4499-a32c-c1ea86cf6bef (temporary link, expires in 30 days)\
**Preprocessing:**  tokenization, lowercasing \
**Levenshtein distance:** deletion, insertion, substitution, transpose \
Transpose: rare, but improves result by 1% \
Threshold set for known words to appear at least x times in the BNC, as results initially had a very low score (38% on dev set) due to Historical English words present in the BNC (thus these words would not be corrected to resent-day English. Threshold set to 19 - it doesn't improve beyond/below that on dev set

To get the results of the Norvig Spelling Corrector, run: \
```python3 norvig_spelling.py``` 

#### Results: 51% of 4541 correct on dev


## 2. VARD2: rule-based preprocessing
-Run VARD2: ```run.bat``` on Windows (requirement to have JAVA installed)/ ```run.sh``` on Linux \
-Select User Interface: 1st one -> single text (interactive). open -> file: xml also possible
-->unnormalized version \
Advances --> rule list manager \
batch mode ->xml input and output \
normalized and unnormalized versions next to each other 


Reference corpus: British National Corpus -> check for spelling (gold standard) \
Corpus for evaluation/training: ARCHER Corpus -> 1600-1700 

## 3. Character-level recurrent sequence-to-sequence model (seq2seq) 

See Jupyter Notebook: ```seq2seq.ipynb```

**ICAMET Corpus**: The files were already separated into dev, train and test set  \
```But train_test_split from sklearn.model_selection``` will be used for evaluation. \
Therefore the following shell commands were executed to concatenate the input and output files into 1 file each: \

```cat icamet_en-hs_train_hs.txt icamet_en-hs_dev_hs.txt icamet_en-hs_test_hs.txt >concatenated_input.txt ``` for the input (Historical English words) \
```cat icamet_en-hs_train_en.txt icamet_en-hs_dev_en.txt icamet_en-hs_test_en.txt >concatenated_output.txt ``` for the output (Normalized English words) \

-**step 1: preprocessing the data** \
-**step 2: building the encoder-decoder LSTM model with set parameters** \
-**step3: training the model** \
-**step 4: testing the model** by making predictions and see how well it performs \
evaluation with ICAMET, and ARCHER (years 1600-1700) 

**evaluation metrics**
accuracy: compare with the number of words that don't need to be changed \
precision and recall -> for words that the algorithm changed something / gold standard cases 


