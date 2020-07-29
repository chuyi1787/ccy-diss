#!/bin/bash

N=( $1 ) # N - left and N-right sentence characters to extract
MAX_token_Nk=$2 #10

UD_directory=selectedUDT-v2.1 #change for other versions
languages="English Arabic Turkish Spanish" # list of languages to process

mkdir -p ../data



for n in "${N[@]}"
do
    for lang in ${languages}
    do
        targetDir=../data/${lang}-${N}-char-context-${MAX_token_Nk}k
        mkdir -p ${targetDir}

        python3 format-char.py $UD_directory/UD_${lang}/dev ${lang} dev ${n} ${MAX_token_Nk}
        mv dev-* ${targetDir}/.

        python3 format-char.py $UD_directory/UD_${lang}/train ${lang} train ${n} ${MAX_token_Nk}
        mv train-* ${targetDir}/.

        python3 format-char.py $UD_directory/UD_${lang}/test ${lang} test ${n} ${MAX_token_Nk}
        mv test-* ${targetDir}/.
    done
done
