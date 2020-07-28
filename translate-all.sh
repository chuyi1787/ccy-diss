#!bin/sh

models=$1 # models / models-10k/ models-char

for dir in ${models}/*  #dir -  the dir name under models/
do
  echo "++++++++"${dir}
  # model used to translate
  model=$(find $dir -type f -name '*.pt')

  # get corresponding dev-source, dev-target
  datadir=data/${dir##*/}

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


