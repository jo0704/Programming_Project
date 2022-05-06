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
British National Corpus (BNC) https://www.swisstransfer.com/d/0c7c1bbd-3fac-48c7-8df0-0f8d58388f95 (temporary link, expires in 30 days)\
**Preprocessing:**  tokenization, lowercasing \
**Levenshtein distance:** deletion, insertion, substitution, transpose \
Transpose: rare, but improves result by 1% \
Threshold set for known words to appear at least x times in the BNC, as results initially had a very low score (38% on dev set) due to Historical English words present in the BNC (thus these words would not be corrected to resent-day English. Threshold set to 19 - it doesn't improve beyond/below that on dev set

To get the results of the Norvig Spelling Corrector, run: \
```python3 norvig_spelling.py``` 

#### Evaluation metrics: accuracy, recall and precision
evaluation with ICAMET, and ARCHER (years 1600-1700) \
```evaluation_results.txt``` \
confusion matrix: \
<img width="539" alt="confusion_matrix" src="https://user-images.githubusercontent.com/56045665/155241341-60a0bc04-fad7-4596-9134-54baa25dc801.png"> \
Precision: TP/TP+FP \
ratio of correctly predicted positive samples to the total predicted positive samples (normalized) \
Accuracy: TP+TN/TP+FP+FN+TN \
ratio of correctly predicted translations to the total translations \
Recall: TP/TP+FN \
ratio of positive samples correctly classified as positive to the total positive samples \
The file ```results_common.txt``` contains the historical English words that are spelled like today

## 2. Character-level recurrent sequence-to-sequence model (seq2seq) 

See Jupyter Notebook: ```seq2seq.ipynb```

**ICAMET Corpus**: The files were already separated into dev, train and test set  \
```But train_test_split from sklearn.model_selection``` will be used for evaluation. \
Therefore the following shell commands were executed to concatenate the input and output files into 1 file each: 

```cat icamet_en-hs_train_hs.txt icamet_en-hs_dev_hs.txt icamet_en-hs_test_hs.txt >concatenated_input.txt ``` for the input (Historical English words) \
```cat icamet_en-hs_train_en.txt icamet_en-hs_dev_en.txt icamet_en-hs_test_en.txt >concatenated_output.txt ``` for the output (Normalized English words) 

-**step 1: preprocessing the data** \
-**step 2: building the encoder-decoder LSTM model with set parameters** \
-**step3: training the model** \
-**step 4: testing the model** make predictions and see how well it performs \
evaluation with ICAMET, and ARCHER (years 1600-1700) 

**evaluation metrics**
accuracy: compare with the number of words that don't need to be changed \
precision and recall -> for words that the algorithm changed something / gold standard cases 

Task could not be completed: problems while training and testing

## 3. State-of-the-art neural approach: Nematus

Nematus is an attention-based encoder-decoder model for NMT implemented in
Python and built in Tensorflow (Sennrich et al. 2017). 

**Requirements:** \
Python 3 \
Install environment: ```conda create --name tf_gpu tensorflow-gpu=2.2.0 python=3.7 cudatoolkit=10``` \
```conda activate tf_gpu``` and install all requirements in environment \
If SacreBLEU is not installed: ```pip install sacrebleu``` \
Install Tensorflow: ```pip install --upgrade tensorflow``` \
Download Nematus: ```git clone https://github.com/EdinburghNLP/nematus``` \
Build and install Sentencepiece (if not done yet): ```pip install sentencepiece``` \
All other requirements for Sentencepiece are explained in https://github.com/google/sentencepiece#build-and-install-sentencepiece-command-line-tools-from-c-source \
Sentencepiece is the BPE technique applied in Nematus for preprocessing and postprocessing

-**step 1: preprocessing the data:**  \
inputs: icamet train, dev and test files (one word per line, end of sentences marked by empty line) turned into sentences with ```process.py```\
note: the training files contained (encoding) errors that had to be manually corrected: \
Entire sentences were skipped due to some lines containing errors such as /000/000 probably due to some weird characters - these were deleted and the correct sentences were added manually

The files we get with the script:
train.src.raw \
train.trg.raw \
```cat train.src.raw train.trg.raw > train.src.trg.raw``` : to create joint vocab with Sentencepiece (spm) \
dev.src.raw \
dev.trg.raw \
test.src.raw \
test.trg.raw 

run ```./preprocess.sh``` : the script prepares the data files for training and creates a shared vocabulary between training source and target (as we are working with a small amount of data, this is done so that the model learns better) and applied spm splits on all the data files (train, dev and test) \
-**step 2: training:** on university's server rattle with one GPU (note: scripts and data files are not on rattle anymore) \
```./train.sh GPU_ID``` \
Training uses the preprocessed data files obtained in step 1 \
Training uses early stop, which is based on the evaluated metric on the validation
set at training time, in that case the character n-gram F-score (chrF) \
log file of training process is stored in ```Nematus\scripts\log.out``` \
-**step 3: generate translations** \
run ```./evaluate.sh GPU_ID``` 

translations are generated for both dev and test and are stored in : ```Nematus\translations\dev.post``` and ```Nematus\translations\test.post```

-**step 4: compute evaluation scores** \
chrf: Character-level n-gram F-score (Popovic 2015) \
run ```./validate.sh dev.post``` and ```./validate.sh test.post``` \
OR ```sacrebleu dev.ref -i dev.post --force -w 2 -m chrf``` & ```sacrebleu test.ref -i test.post --force -w 2 -m chrf``` \
(test.ref is the file test.trg.raw)
chrF dev: **88.88** \
chrF test: **89.30** \
to compute both BLEU and chrf scores: ```sacrebleu dev.ref -i dev.post --force -w 2 -m bleu chrf``` & ```sacrebleu test.ref -i test.post --force -w 2 -m bleu chrf``` \
this also gives us information about BLEU:
BLEU dev: **78.11**
BLEU test: **78.68** 

