#type=20-char-context
type=500-BPEmb-20-context
#type=500-bpe-20-context
languages=$1 #"English Arabic Turkish Spanish"
model_n=$2

for lang in ${languages}
do
  datadir=${lang}-${type}
  echo "Lemmatizing test set "
  echo ${lang}-${type}
  onmt_translate \
    --model models/${lang}-${type}/${lang}-${type}_step_${model_n}.pt\
    --src data/${lang}-${type}/test-sources\
    --output models/${lang}-${type}/${lang}-${type}_step_${model_n}_pred.txt\
    --replace_unk\
    --beam_size 12
  echo "Done"
  echo "test acc:"
  python3 accuracy.py ${lang} ${type} ${model_n}


done













