#!bin/sh

models=$1 # models / models-10k/ models-char

for dir in ${models}/*  #dir -  the dir name under models/
do
  refPath=data/${dir##*/}/dev-targets
  echo "++++++++"${dir}
  python3 accuracy.py $refPath ${dir}/dev_pred.txt
done