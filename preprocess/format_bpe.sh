#!/bin/bash

merge_N=$1 #500
n_context=$2 #20

UD_directory=selectedUDT-v2.1 #change for other versions
languages="English Arabic Turkish Spanish" # list of languages to process


mkdir -p ../data

for lang in ${languages}
do
    targetDir=../data/${lang}-${merge_N}-bpe-${n_context}-context
    mkdir -p ${targetDir}

    python3 bpe-format.py $UD_directory/UD_${lang}/dev ${lang} dev ${merge_N} ${n_context}
    mv dev-* ${targetDir}/.

    python3 bpe-format.py $UD_directory/UD_${lang}/train ${lang} train ${merge_N} ${n_context}
    mv train-* ${targetDir}/.

    python3 bpe-format.py $UD_directory/UD_${lang}/test ${lang} test ${merge_N} ${n_context}
    mv test-* ${targetDir}/.
done

