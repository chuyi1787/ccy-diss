#!/bin/bash

UD_directory=selectedUDT-v2.1 #change for other versions
languages="English Arabic Turkish Spanish" # list of languages to process
merge_N=500
n_context=20

mkdir -p ../data

for lang in ${languages}
do
    targetDir=../data/${lang}-${merge_N}-bpe-${n_context}-context
    mkdir -p ${targetDir}

    python3 ccypp_for_lematus.py $UD_directory/UD_${lang}/dev ${lang} dev ${merge_N} ${n_context}
    mv dev-* ${targetDir}/.

    python3 ccypp_for_lematus.py $UD_directory/UD_${lang}/train ${lang} train ${merge_N} ${n_context}
    mv train-* ${targetDir}/.

    python3 ccypp_for_lematus.py $UD_directory/UD_${lang}/test ${lang} test ${merge_N} ${n_context}
    mv test-* ${targetDir}/.
done

