#!/bin/bash

merge_N=$1 #500
n_context=$2 #20

UD_directory=selectedUDT-v2.1 # origianl data sources
languages="English Arabic Turkish Spanish" # list of languages to process


mkdir -p ../data

for lang in ${languages}
do
    targetDir=../data/${lang}-${merge_N}-BPEmb-all-${n_context}-context
    mkdir -p ${targetDir}

    python3 format-BPEmb-all.py $UD_directory/UD_${lang}/dev ${lang} dev ${merge_N} ${n_context} ${MAX_token_Nk}
    mv dev-* ${targetDir}/.

    python3 format-BPEmb-all.py $UD_directory/UD_${lang}/train ${lang} train ${merge_N} ${n_context} ${MAX_token_Nk}
    mv train-* ${targetDir}/.

    python3 format-BPEmb-all.py $UD_directory/UD_${lang}/test ${lang} test ${merge_N} ${n_context} ${MAX_token_Nk}
    mv test-* ${targetDir}/.
done

