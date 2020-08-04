#!/bin/bash

UD_directory=selectedUDT-v2.1 #change for other versions
languages="English Arabic Turkish Spanish" # list of languages to process


N=( $1 ) # N context

for n in "${N[@]}"
do
    for lang in ${languages}
    do
        targetDir=../data-lite/${lang}-${N}-char-context-lite
        mkdir -p ${targetDir}

        python3 format-char.py $UD_directory/UD_${lang}/train ${lang} train ${n} 10
        mv train-* ${targetDir}/.

        python3 format-char.py $UD_directory/UD_${lang}/dev ${lang} dev ${n} 3
        mv dev-* ${targetDir}/.

        python3 format-char.py $UD_directory/UD_${lang}/test ${lang} test ${n}
        mv test-* ${targetDir}/.
    done
done
