models=$1 # models / models-lR / models-char
datapath=$2 # data-lowresource
valtype=$3 # unseen-, ambiguous-

resFilePath=../result/${valtype}${models}.res
rm ${resFilePath}

for dir in ../model/${models}/*  #dir, e.g, Arabic-100-BPEmb-all-15-context
do
  datadir=../data/${datapath}/${dir##*/}
  echo "++++++++Begin translate by model: "${dir}

  rm ${dir}/${valtype}dev_pred.txt
  # get corresponding dev-source, dev-target
  model=$(find $dir -type f -name '*.pt')
  onmt_translate \
  --model ${model}\
  --src ${datadir}/dev-${valtype}sources\
  --output ${dir}/${valtype}dev_pred.txt\
  --replace_unk\
  --beam_size 12
  echo "End of translate"

  refPath=${datadir}/dev-${valtype}targets #data-bpeall/Arabic-100-BPEmb-all-15-context/dev-targets
  echo "++++++++"${dir} >> ${resFilePath}
  python3 accuracy.py ${refPath} ${dir}/${valtype}dev_pred.txt >> ${resFilePath}

done

echo "Finish!!!!"
