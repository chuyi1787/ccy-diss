export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7

modelDir=$1 # given the dictionary name of model, likes "models-char"
type=$2 #models type, 500-BPEmb-20-context (don't need to add lite)
languages=$3


batch_size=60
burn_in_for_n_epochs=10
patience=10 # early_stopping_n_epochs
val_every_n_epochs=1


for lang in ${languages}
do
datadir=${lang}-${type}-lite
mkdir -p ${modelDir}/${lang}-${type}/

steps_of_an_epoch=($(wc -l ./data-lite/${datadir}/train-sources))
#use the first 10 epochs as a burn-in period
validBurnIn=$((steps_of_an_epoch *${burn_in_for_n_epochs} / ${batch_size}))
# early stopping with patience 10
early_stopping_steps=$((steps_of_an_epoch *${patience} / ${batch_size}))
# validate every epoch
val_steps=$((steps_of_an_epoch *${val_every_n_epochs}/ ${batch_size}))

echo "Sarting training, steps_of_an_epoch:"
echo ${val_steps}
echo "validBurnIn steps"
echo ${validBurnIn}


onmt_train -data data-lite/${datadir}/data-pp/${datadir}\
  --save_model ${modelDir}/${datadir}/${datadir}\
  --save_checkpoint_steps ${val_steps}\
  --encoder_type brnn\
  --decoder_type rnn\
  --enc_layers 2\
  --dec_layers 2\
  --rnn_type GRU\
  --batch_size 60\
  --src_word_vec_size 300\
  --tgt_word_vec_size 300\
  --rnn_size 100\
  --optim "adadelta" \
  --dropout 0.2\
  --early_stopping 10\
  --early_stopping_criteria accuracy\
  --valid_steps ${val_steps}\
  --warmup_steps ${validBurnIn}\
  --train_steps 3000000\
  --report_every ${val_steps} \
  --gpu_ranks 0 2>&1 | tee ${modelDir}/${datadir}/train-log-${datadir}.txt
echo "End of training"


done


