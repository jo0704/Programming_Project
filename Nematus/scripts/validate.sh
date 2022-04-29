#!/bin/sh

translations=$1

nematus_home="/home/user/gasser/anaconda3/nematus" # path to nematus directory
script_dir="/home/user/gasser/scripts_copy" # path to scripts directory
data_dir="/home/user/gasser/norm" # path to data directory

# ref="dev.ref"
ref="test.trg.raw"

#compute chrF score
$script_dir/postprocess.sh < $translations | sacrebleu --force -q -w 2 -m chrf -b $data_dir/$ref
#compute BLEU score
# $script_dir/postprocess.sh < $translations | sacrebleu --force -q -w 2 -b $data_dir/$ref