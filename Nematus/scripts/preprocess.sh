#!/bin/sh

vocab_size="3000"

script_dir="../scripts_copy" # path to scripts directory
data_dir="../norm" # path to data directory

# train BPE models
#sentencepiece/build/src/ should be installed 
spm_train --input=$data_dir/train.src.trg.raw \
		  --model_prefix=$data_dir/spm.joint \
		  --vocab_size=$vocab_size \
		  --character_coverage 1.0 \
		  --model_type=bpe \
		  --shuffle_input_sentence=True 	  
		  
# create nematus vocabulary files
python3 $script_dir/convert_spm_vocab.py $data_dir/spm.joint.vocab
mv $data_dir/spm.joint.vocab.json $data_dir/vocab.joint.json

# encode all data

spm_encode --model=$data_dir/spm.joint.model < $data_dir/train.src.raw > $data_dir/train.src
spm_encode --model=$data_dir/spm.joint.model < $data_dir/dev.src.raw > $data_dir/dev.src
spm_encode --model=$data_dir/spm.joint.model < $data_dir/test.src.raw > $data_dir/test.src

spm_encode --model=$data_dir/spm.joint.model < $data_dir/train.trg.raw > $data_dir/train.trg
spm_encode --model=$data_dir/spm.joint.model < $data_dir/dev.trg.raw > $data_dir/dev.trg
spm_encode --model=$data_dir/spm.joint.model < $data_dir/test.trg.raw > $data_dir/test.trg
