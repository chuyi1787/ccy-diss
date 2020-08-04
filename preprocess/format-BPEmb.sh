merge_N=$1 #500
n_context=$2 #20

UD_directory=selectedUDT-v2.1 # origianl data sources
languages="English Arabic Turkish Spanish" # list of languages to process

for lang in ${languages}
do
    targetDir=../data-lite/${lang}-${merge_N}-BPEmb-${n_context}-context-lite
    mkdir -p ${targetDir}

    python3 format-BPEmb.py $UD_directory/UD_${lang}/train ${lang} train ${merge_N} ${n_context} 10
    mv train-* ${targetDir}/.

    python3 format-BPEmb.py $UD_directory/UD_${lang}/dev ${lang} dev ${merge_N} ${n_context} 3
    mv dev-* ${targetDir}/.

    python3 format-BPEmb.py $UD_directory/UD_${lang}/test ${lang} test ${merge_N} ${n_context}
    mv test-* ${targetDir}/.
done

