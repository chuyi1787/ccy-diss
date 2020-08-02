models=$1 # models-lR / models-bpe/ models-char
datatype=$2 # data-bpeall

for dir in ${models}/*  #dir -  the dir name under models/
do
  echo "++++++++"${dir}
  # model used to translate
  model=$(find $dir -type f -name '*.pt')

  # get corresponding dev-source, dev-target
  datadir=${datatype}/${dir##*/}

  rm ${dir}/dev_pred.txt
  echo "Begin translate by model: "${model}
  onmt_translate \
  --model ${model}\
  --src ${datadir}/dev-sources\
  --output ${dir}/dev_pred.txt\
  --replace_unk\
  --beam_size 12
  echo "End of translate"
done


########
#move all data-pp to correspoding data dir
########
#for dir in models/*
#do
#  targetdir=data/${dir##*/}
#  for item in $dir/*
#  do
#    echo $item
#    if test -d $item
#    then
#      if [ "$item" = "${dir}/data-pp" ]
#      then
#        mv $item $targetdir
#        echo "move"
#        echo $targetdir
#      fi
#    fi
#  done
#done


