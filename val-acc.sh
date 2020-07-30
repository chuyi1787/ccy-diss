#!bin/sh

models=$1 # models / models-10k/ models-char

rm val-acc-${models}.res

for dir in ${models}/*  #dir -  the dir name under models/
do
  refPath=data/${dir##*/}/dev-targets
  echo "++++++++"${dir} >> val-acc-${models}.res
  python3 accuracy.py $refPath ${dir}/dev_pred.txt >> val-acc-${models}.res

done