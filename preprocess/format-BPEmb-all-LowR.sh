#!/bin/bash

merge_N=$1 #500
n_context=$2 #20
train_token_Nk=10
dev_token_Nk=3

UD_directory=selectedUDT-v2.1 # origianl data sources
languages="English Arabic Turkish Spanish" # list of languages to process


mkdir -p ../data-lowresource

for lang in ${languages}
do
    targetDir=../data-lowresource/${lang}-${merge_N}-BPEmb-all-${n_context}-context-lowR
    mkdir -p ${targetDir}

    python3 format-BPEmb-all.py $UD_directory/UD_${lang}/dev ${lang} dev ${merge_N} ${n_context} ${dev_token_Nk}
    mv dev-* ${targetDir}/.

    python3 format-BPEmb-all.py $UD_directory/UD_${lang}/train ${lang} train ${merge_N} ${n_context} ${train_token_Nk}
    mv train-* ${targetDir}/.

    python3 format-BPEmb-all.py $UD_directory/UD_${lang}/test ${lang} test ${merge_N} ${n_context}
    mv test-* ${targetDir}/.
done

