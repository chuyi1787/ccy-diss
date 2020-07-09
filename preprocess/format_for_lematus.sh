#!/bin/bash

UD_directory=selectedUDT-v2.1 #change for other versions
languages="English" # list of languages to process

mkdir -p ../data

N=( 20 ) # N - left and N-right sentence characters to extract 

for n in "${N[@]}"
do
    for lang in ${languages}
    do
        targetDir=../data/${lang}-${N}-char-context
        mkdir -p ${targetDir}

        python3 format_for_lematus.py $UD_directory/UD_${lang}/dev ${lang} dev ${n}
        mv dev-* ${targetDir}/.

        python3 format_for_lematus.py $UD_directory/UD_${lang}/train ${lang} train ${n}
        mv train-* ${targetDir}/.

        python3 format_for_lematus.py $UD_directory/UD_${lang}/test ${lang} test ${n}
        mv test-* ${targetDir}/.
    done
done
