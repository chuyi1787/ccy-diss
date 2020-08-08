n_context=$1 #20

UD_directory=selectedUDT-v2.1 # origianl data sources
languages="English Arabic Turkish Spanish Indonesian" # list of languages to process

for lang in ${languages}
do
    echo $lang
    targetDir=../data-full/${lang}-morfessor-${n_context}-context
    mkdir -p ${targetDir}

    python3 format-morfessor.py $UD_directory/UD_${lang}/train ${lang} train  ${n_context}
    mv train-* ${targetDir}/.

    python3 format-morfessor.py $UD_directory/UD_${lang}/dev ${lang} dev  ${n_context}
    mv dev-* ${targetDir}/.

    python3 format-morfessor.py $UD_directory/UD_${lang}/test ${lang} test  ${n_context}
    mv test-* ${targetDir}/.

    # for lite
    targetDir2=../data-lite/${lang}-morfessor-${n_context}-context-lite
    mkdir -p ${targetDir2}

    python3 format-morfessor.py $UD_directory/UD_${lang}/train ${lang} train  ${n_context} 10
    mv train-* ${targetDir2}/.

    python3 format-morfessor.py $UD_directory/UD_${lang}/dev ${lang} dev  ${n_context} 3
    mv dev-* ${targetDir2}/.

    python3 format-morfessor.py $UD_directory/UD_${lang}/test ${lang} test  ${n_context}
    mv test-* ${targetDir2}/.
done

