#!/bin/bash

type=$1 #500-BPEmb-20-context char-20-context(-lite) trigram-15-context
mode=$2 #"lite"
datadir=data-${mode}
echo $datadir
languages="English Arabic Turkish Spanish Indonesian"

for lang in ${languages}
do
echo ${lang}-${type}
mkdir -p ${datadir}/${lang}-${type}/data-pp/


echo "Starting dp"
onmt_preprocess \
  -train_src ${datadir}/${lang}-${type}/train-sources\
  -train_tgt ${datadir}/${lang}-${type}/train-targets \
  -valid_src ${datadir}/${lang}-${type}/dev-sources \
  -valid_tgt ${datadir}/${lang}-${type}/dev-targets \
  -src_seq_length 75 \
  -tgt_seq_length 75 \
  -save_data ${datadir}/${lang}-${type}/data-pp/${lang}-${type}
echo "End of dp"

done
