#!/bin/sh
#removing bpe splits

data_dir="/home/user/gasser/norm" # path to data directory

# spm_decode --model=$data_dir/spm.src.model
spm_decode --model=$data_dir/spm.joint.model
