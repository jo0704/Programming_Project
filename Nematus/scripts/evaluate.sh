#!/bin/sh

gpu_id=$1

script_dir=/home/user/gasser/scripts_copy
data_dir=/home/user/gasser/norm
working_dir=$data_dir/norm
nematus_home=/home/user/gasser/anaconda3/nematus

batchsize=100
beamsize=4
strategy=beam_search
model=model.best-valid-script

CUDA_VISIBLE_DEVICES=$gpu_id python3 $nematus_home/nematus/translate.py -m $working_dir/$model -i $data_dir/dev.src -o $data_dir/dev.out --translation_strategy $strategy  --translation_maxlen 200 -k $beamsize -n 0.6 -b $batchsize 
bash $script_dir/postprocess.sh < $data_dir/dev.out > $data_dir/dev.post

#uncomment to generate test translations
# CUDA_VISIBLE_DEVICES=$gpu_id python3 $nematus_home/nematus/translate.py -m $working_dir/$model -i $data_dir/test.src -o $data_dir/test.out --translation_strategy $strategy  --translation_maxlen 200 -k $beamsize -n 0.6 -b $batchsize 
# bash $script_dir/postprocess.sh < $data_dir/test.out > $data_dir/test.post