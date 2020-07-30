#!/bin/bash

N=( $1 ) # N - left and N-right sentence characters to extract
train_token_Nk=10
dev_token_Nk=3

UD_directory=selectedUDT-v2.1 #change for other versions
languages="English Arabic Turkish Spanish" # list of languages to process

mkdir -p ../data-lowresource



for n in "${N[@]}"
do
    for lang in ${languages}
    do
        targetDir=../data-lowresource/${lang}-${N}-char-context-lowR
        mkdir -p ${targetDir}

        python3 format-char.py $UD_directory/UD_${lang}/dev ${lang} dev ${n} ${dev_token_Nk}
        mv dev-* ${targetDir}

        python3 format-char.py $UD_directory/UD_${lang}/train ${lang} train ${n} ${train_token_Nk}
        mv train-* ${targetDir}

        python3 format-char.py $UD_directory/UD_${lang}/test ${lang} test ${n}
        mv test-* ${targetDir}
    done
done
