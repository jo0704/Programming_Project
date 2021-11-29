# Programming Project: Spelling normalisation of historical English to English
Comparing 3 different approaches: which one performs better?

1. Norvig Spelling Corrector

edit distance approach.
works with a language model -> British National Corpus
what makes sense? small letters only, capitalization, etc, tokenization

2. VARD2: rule-based preprocessing
-Run VARD2: run.bat on Windows (requirement to have JAVA installed)/ run.sh on Linux
-Select User Interface: 1st one -> single text (interactive). open -> file: xml also possible
-->unnormalized version 
Advances --> rule list manager
batch mode ->xml input and output
normalized and unnormalized versions next to each other 


Reference corpus: British National Corpus -> check for spelling (gold standard)
Corpus for evaluation/training: ARCHER Corpus -> 1600-1700

3. Character-level recurrent sequence-to-sequence model (seq2seq)
See seq2seq.ipynb

ICAMET Corpus: separated into dev, train and test set -> one word per line without context
-input: historical English words / target: modern English words
-preprocessing the data
-building the encoder-decoder LSTM model with set parameters
-training the model
-testing the model by making predictions and see how well it performs
evaluation with ICAMET, and ARCHER (first century 1600-1700)

evaluation metrics
accuracy: compare with the number of words that don't need to be changed
precision and recall -> for words that the algorithm changed something / gold standard cases 


