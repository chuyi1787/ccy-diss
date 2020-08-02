#!bin/sh

models=$1 # models / models-lR / models-char
datapath=$2 # data-lowresource

rm val-acc-${models}.res

for dir in ${models}/*  #dir, e.g, Arabic-100-BPEmb-all-15-context
do
  refPath=${datapath}/${dir##*/}/dev-targets #data-bpeall/Arabic-100-BPEmb-all-15-context/dev-targets
  echo "++++++++"${dir} >> val-acc-${models}.res
  python3 tools/accuracy.py $refPath ${dir}/dev_pred.txt >> result/val-acc-${models}.res
  echo "val finish"
done
