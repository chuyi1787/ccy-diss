export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7

type=$1 #25-char-context-10k
languages=$2

batch_size=60
burn_in_for_n_epochs=10
patience=10 # early_stopping_n_epochs
val_every_n_epochs=1


for lang in ${languages}
do
datadir=${lang}-${type}
mkdir -p models/${lang}-${type}/

steps_of_an_epoch=($(wc -l ./data/${datadir}/train-sources))
#use the first 10 epochs as a burn-in period
validBurnIn=$((steps_of_an_epoch *${burn_in_for_n_epochs} / ${batch_size}))
# early stopping with patience 10
early_stopping_steps=$((steps_of_an_epoch *${patience} / ${batch_size}))
# validate every epoch
val_steps=$((steps_of_an_epoch *${val_every_n_epochs}/ ${batch_size}))

echo "Sarting training, steps_of_an_epoch:"
echo ${val_steps}

onmt_train -data data/${datadir}/data-pp/${datadir}\
  --save_model models/${datadir}/${lang}-${type}\
  --save_checkpoint_steps ${steps_of_an_epoch}\
  --keep_checkpoint 3\
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
  --valid_steps ${val_steps}\
  --warmup_steps ${validBurnIn}\
  --train_steps 3000000\
  --report_every ${val_steps} \
  --gpu_ranks 0 2>&1 | tee models/${datadir}/train-gpu.txt
echo "End of training"


done












