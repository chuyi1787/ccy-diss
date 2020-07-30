#!/bin/bash

type=$1 #500-BPEmb-20-context #20-char-context
languages="English Arabic Turkish Spanish"

mkdir -p ./models
for lang in ${languages}
do
echo ${lang}-${type}
mkdir -p data/${lang}-${type}/data-pp/


echo "Starting dp"
onmt_preprocess \
  -train_src data-lowresource/${lang}-${type}/train-sources\
  -train_tgt data-lowresource/${lang}-${type}/train-targets \
  -valid_src data-lowresource/${lang}-${type}/dev-sources \
  -valid_tgt data-lowresource/${lang}-${type}/dev-targets \
  -src_seq_length 75 \
  -tgt_seq_length 75 \
  -save_data data-lowresource/${lang}-${type}/data-pp/${lang}-${type}
echo "End of dp"

done
