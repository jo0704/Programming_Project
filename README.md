# Programming Project: Spelling normalisation of historical English to English
Comparing 3 different approaches: which one performs better?

1. Norvig Spelling Corrector
2. VARD2: rule-based preprocessing
-Run VARD2: run.bat on Windows (requirement to have JAVA installed)/ run.sh on Linux
-Select User Interface: Batch process (automatic)

Reference corpus: British National Corpus -> check for spelling
Corpus for evaluation/training: ARCHER Corpus -> 1600-1850

3. Character-level recurrent sequence-to-sequence model (seq2seq)
See seq2seq.ipynb

ICAMET Corpus: separated into dev, train and test set -> one word per line without context
-input: historical English words / target: modern English words
-preprocessing the data
-building the encoder-decoder LSTM model with set parameters
-training the model
-testing the model by making predictions and see how well it performs


